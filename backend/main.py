import os
import re
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

DATABASE_URL = os.environ["DATABASE_URL"]
EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

pool: asyncpg.Pool = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
    await pool.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id          SERIAL PRIMARY KEY,
            post_slug   TEXT NOT NULL,
            author_name TEXT NOT NULL,
            comment_text TEXT NOT NULL,
            parent_id   INTEGER REFERENCES comments(id),
            ip_address  TEXT,
            user_agent  TEXT,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    await pool.execute("""
        CREATE INDEX IF NOT EXISTS idx_comments_post_slug ON comments(post_slug)
    """)
    yield
    await pool.close()


def _get_ip(request: Request) -> str:
    return (
        request.headers.get("cf-connecting-ip")
        or (request.headers.get("x-forwarded-for") or "").split(",")[0].strip()
        or request.headers.get("x-real-ip")
        or request.client.host
    )


limiter = Limiter(key_func=_get_ip)
app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Too many requests"})


@app.post("/api/newsletter", status_code=201)
@limiter.limit("10/hour")
async def subscribe(request: Request):
    body = await request.json()
    email = (body.get("email") or "").strip()
    name = (body.get("name") or "").strip() or None

    if not email:
        return JSONResponse(status_code=400, content={"error": "Email is required"})
    if not EMAIL_REGEX.match(email):
        return JSONResponse(status_code=400, content={"error": "Invalid email format"})
    if len(email) > 255:
        return JSONResponse(status_code=400, content={"error": "Email is too long"})
    if name and len(name) > 255:
        return JSONResponse(status_code=400, content={"error": "Name is too long"})

    existing = await pool.fetchrow(
        "SELECT id FROM newsletter_subscriptions WHERE email = $1", email
    )
    if existing:
        return JSONResponse(status_code=400, content={"error": "Email already subscribed"})

    row = await pool.fetchrow(
        "INSERT INTO newsletter_subscriptions (email, name) VALUES ($1, $2) RETURNING *",
        email, name,
    )
    return {
        "id": row["id"],
        "email": row["email"],
        "name": row["name"],
        "subscribed_at": row["subscribed_at"].isoformat(),
    }


@app.post("/api/page-views", status_code=201)
async def record_page_view(request: Request):
    body = await request.json()
    path = body.get("path")

    if not path:
        return JSONResponse(status_code=400, content={"error": "Path is required"})

    ip_address = _get_ip(request)
    user_agent = request.headers.get("user-agent")
    referer = request.headers.get("referer")
    country = request.headers.get("cf-ipcountry")
    city = request.headers.get("cf-ipcity")

    await pool.execute(
        """INSERT INTO page_views (path, ip_address, user_agent, referer, country, city)
           VALUES ($1, $2, $3, $4, $5, $6)""",
        path, ip_address, user_agent, referer, country, city,
    )
    return {"success": True}


@app.get("/api/comments/{slug:path}")
async def get_comments(slug: str):
    rows = await pool.fetch(
        """SELECT id, post_slug, author_name, comment_text, parent_id,
                  created_at
           FROM comments
           WHERE post_slug = $1
           ORDER BY created_at ASC""",
        slug,
    )
    return [
        {
            "id": r["id"],
            "post_slug": r["post_slug"],
            "author_name": r["author_name"],
            "comment_text": r["comment_text"],
            "parent_id": r["parent_id"],
            "created_at": r["created_at"].isoformat(),
        }
        for r in rows
    ]


@app.post("/api/comments", status_code=201)
@limiter.limit("10/hour")
async def post_comment(request: Request):
    body = await request.json()
    post_slug = (body.get("post_slug") or "").strip()
    author_name = (body.get("author_name") or "").strip()
    comment_text = (body.get("comment_text") or "").strip()
    parent_id = body.get("parent_id")

    if not post_slug:
        return JSONResponse(status_code=400, content={"error": "post_slug is required"})
    if not author_name:
        return JSONResponse(status_code=400, content={"error": "Name is required"})
    if len(author_name) > 100:
        return JSONResponse(status_code=400, content={"error": "Name is too long"})
    if not comment_text:
        return JSONResponse(status_code=400, content={"error": "Comment is required"})
    if len(comment_text) > 5000:
        return JSONResponse(status_code=400, content={"error": "Comment is too long (max 5000 chars)"})

    if parent_id is not None:
        parent = await pool.fetchrow("SELECT id FROM comments WHERE id = $1", int(parent_id))
        if not parent:
            return JSONResponse(status_code=400, content={"error": "Parent comment not found"})

    ip_address = _get_ip(request)
    user_agent = request.headers.get("user-agent")

    row = await pool.fetchrow(
        """INSERT INTO comments (post_slug, author_name, comment_text, parent_id, ip_address, user_agent)
           VALUES ($1, $2, $3, $4, $5, $6)
           RETURNING id, post_slug, author_name, comment_text, parent_id, created_at""",
        post_slug, author_name, comment_text,
        int(parent_id) if parent_id is not None else None,
        ip_address, user_agent,
    )
    return {
        "id": row["id"],
        "post_slug": row["post_slug"],
        "author_name": row["author_name"],
        "comment_text": row["comment_text"],
        "parent_id": row["parent_id"],
        "created_at": row["created_at"].isoformat(),
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
