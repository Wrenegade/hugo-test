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


@app.get("/health")
async def health():
    return {"status": "ok"}
