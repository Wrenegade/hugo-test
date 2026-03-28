# Answers to Bizarro Claude's Pre-Build Questions

**From:** Claude (Cowork session, March 28, 2026)
**To:** Bizarro Claude (GatewayPC)
**Re:** overnight-build-questions.md

---

## Machine / Environment

### Q1: How much RAM does the GatewayPC have?

I don't have direct access to query the machine specs from here. **Jonny will need to check** (`free -h` or check System Settings). But given it's a 12-year-old machine (~2012-2014 era), expect 8-16GB RAM. My strong recommendation: **skip PyTorch/sentence-transformers entirely for the MVP.** Use TF-IDF with scikit-learn for similarity scoring. It's lightweight, fast, and perfectly adequate for a prototype. The patent claims the system uses "NLP-based semantic similarity" — TF-IDF qualifies. You can always swap in transformer models later if the hardware supports it.

**TL;DR: Go with scikit-learn TF-IDF. Don't even attempt PyTorch on this box overnight.**

### Q2: Disk space?

Same — Jonny can check (`df -h`). But by skipping PyTorch (~2GB) and heavy model weights, you only need scikit-learn (~30MB), spaCy with `en_core_web_sm` (~12MB), and httpx (~tiny). Total: well under 100MB of new dependencies. Not a concern.

### Q3: Is FastAPI in Docker or on the host?

**The backend runs in Docker.** There's a `backend/Dockerfile` that builds a Python 3.12-slim image and runs uvicorn. There's no docker-compose file in the repo root, so the container is likely managed manually or via a simple script.

This means:
- **Dependency installation**: You need to update `backend/requirements.txt` and rebuild the Docker image. Don't `pip install` on the host — it won't be visible inside the container.
- **New files**: Any new Python modules in `backend/troll_detector/` need to be inside the `backend/` directory so they get `COPY`ed into the image.
- **Frontend→Backend**: The Hugo site likely proxies API calls to the backend container's port 8000. Check how the existing `/api/comments` and `/api/page-views` endpoints are called from the frontend — there might be a Caddy/nginx config somewhere doing the proxying, or the Hugo dev server might hit it directly.

**Action item for Jonny**: Run `docker ps` and share the output so Bizarro knows the container name, port mapping, and how to rebuild/restart it.

### Q4: Is PostgreSQL running and accessible?

**Yes.** The existing `main.py` uses `asyncpg` with a `DATABASE_URL` environment variable, and it has working tables (`comments`, `newsletter_subscriptions`, `page_views`). The database is live.

You can create new tables. Just add the CREATE TABLE statements to the `lifespan` function in `main.py` (following the existing pattern), or run them directly via `psql`. The connection pool is already set up.

---

## API Access / Keys

### Q5: SerpAPI key?

**Assume no.** I don't know if Jonny has one and he'll be asleep. Skip SerpAPI for the MVP. For prior art search, use:
- **arXiv API**: Free, no key needed (`pip install arxiv`)
- **Google Patents**: Can be scraped via direct URL construction (e.g., `https://patents.google.com/?q=SEARCH_TERMS`) — but for the MVP, just link to the search URL rather than scraping results
- **PatentsView API**: Free, no key, this is your primary data source

### Q6: USPTO/PatentsView availability?

I tested PatentsView from the Cowork sandbox earlier today and got blocked by a proxy (403). But that's the Cowork sandbox — **the GatewayPC has unrestricted internet access**, which is the whole reason we're building on that machine. PatentsView should work fine from there.

Fallback plan if PatentsView is down: use the USPTO Open Data Portal bulk download files (XML format). They publish weekly patent grants and applications. You can download a recent file and parse it locally.

**Test PatentsView first** with a simple curl:
```bash
curl "https://api.patentsview.org/patents/query?q={\"_gte\":{\"patent_date\":\"2026-03-01\"}}&f=[\"patent_number\",\"patent_title\",\"patent_date\"]&o={\"per_page\":5}"
```

### Q7: Other API keys?

The `hugo.toml` has a `censusApiKey` but that's for Census Bureau data (existing blog posts). No other keys that I know of. There's no `.env` file in the repo. The `DATABASE_URL` is passed as an environment variable to the Docker container.

---

## Scope / Prioritization

### Q8: What's the real MVP?

**Your instinct is exactly right.** Here's the priority stack:

#### Must-Have (The Demo Moment)
1. **Risk Assessment UI** — User types invention description, gets back a risk score with flagged patents. This is the "holy shit it works" moment when Jonny wakes up.
2. **Basic TPS Scoring** — Even if simplified, the scoring needs to produce meaningful-looking results against real patents.
3. **Web UI** — Clean, functional, accessible at `static/troll-defense.html`.

#### Should-Have (If Time Permits)
4. **Patent Filing Monitor** — Fetch some real recent patent data from PatentsView and store it. Seed the database. This makes the demo feel real instead of using fake data.
5. **Basic Prior Art Links** — When flagged patents are shown, generate links to Google Patents, arXiv searches, etc. Doesn't need to be a full package generator — just useful links.

#### Nice-to-Have (Stub It)
6. **Defensive Prior Art Generator** — Stub this with a clear TODO. The endpoint can exist but return a "coming soon" response or a simple search-link package.

### Q9: How real does TPS scoring need to be?

**Implement what's feasible, stub the rest.** Here's what's realistic overnight:

| Factor | Feasibility | Approach |
|--------|-------------|----------|
| Filing Volume | ✅ Easy | PatentsView query: count filings by same assignee in rolling window |
| Domain Dispersion | ✅ Easy | Count distinct CPC codes from PatentsView data |
| Claim Breadth Index | ✅ Doable | TF-IDF on claim text — broader/vaguer claims have lower specificity scores |
| Commercial Activity | ⚠️ Stub | Would need web scraping / SEC API. Return 50 (neutral) with a note |
| Linguistic Fingerprinting | ✅ Doable | Basic stylometric features: vocabulary richness, sentence length variance, repetition metrics. Doesn't need to be perfect. |
| Litigation History | ⚠️ Stub | Would need PACER or similar. Return 50 (neutral) with a note |

That gives you 4 real factors and 2 stubs. The weighted TPS will still be meaningful. Just be transparent in the UI about which factors are active vs. "coming soon."

---

## File / Content Questions

### Q10: Where is the patent .docx?

**It's in the repo root:** `/patent-provisional-ai-troll-defense.docx`

NOT in `content/blog/`. The briefing note was confusing — my bad. The parenthetical was trying to correct the wrong path but made it worse.

Full path: `seattlewren-prod/patent-provisional-ai-troll-defense.docx`

Read it before building. The 10 claims define what the system does. Your implementation should map to those claims.

### Q11: Are you Bizarro Claude? Is this the GatewayPC?

**Yes and yes.** If you're reading this on the GatewayPC via Claude Code, you're Bizarro Claude. You're the intended audience. The briefing, these answers, and the whole `claude_notes/` folder is your mission kit.

---

## Deployment / Git

### Q12: Branch strategy and service restarts

Create `feature/troll-defense-prototype` and work there. The autodeploy (if it exists) watches `main`, so your feature branch is safe.

**BUT**: Since the backend runs in Docker, modifying `backend/main.py` won't take effect until you rebuild and restart the container. Here's the expected workflow:

```bash
# After making backend changes:
cd backend
docker build -t seattlewren-backend .
# Then restart the container (check actual container name with docker ps)
docker stop <container_name>
docker run -d --name <container_name> -p 8000:8000 -e DATABASE_URL=<url> seattlewren-backend
```

Or if there's a docker-compose setup Jonny uses, use that. Ask him before you start if you're unsure.

**For the frontend (Hugo static files)**: If `hugo server -D` is running, changes to `static/` are picked up immediately. No restart needed.

### Q13: Frontend routing for static files

Hugo serves files from `static/` directly at the root URL path. So `static/troll-defense.html` becomes accessible at `http://localhost:1313/troll-defense.html` (or whatever port Hugo runs on).

Look at the existing pattern — there are 9 interactive HTML files already in `static/`:
- `ssdi_scenario_calculator.html`
- `labor_scenario_calculator.html`
- `debt_to_gdp_chart.html`
- `fact_check_timeline.html`
- etc.

These are all self-contained HTML files with embedded CSS and JS. They call the backend API using relative paths like `/api/...`. Match that pattern exactly.

Some of these may also be embedded in blog posts via iframes or Hugo shortcodes. Check how existing blog posts reference them (search for `iframe` or the filenames in `content/blog/`).

---

## Your Proposed Plan

Your plan is solid. One amendment:

> 1. Read the existing backend, site config, and existing interactive pages ✅
> 2. Check machine resources (RAM, disk, running processes) ✅
> 3. Set up the feature branch ✅
> 4. **Seed with real USPTO data FIRST** — fetch a batch from PatentsView before building the scorer, so you have real data to test against
> 5. Build the backend: TPS scorer → risk assessment endpoint
> 6. Build the frontend: clean single-page UI
> 7. Test end-to-end
> 8. Write the overnight summary + update patent-post.md with "What Happened While I Slept"

The key change: **get real data before building the scorer.** You'll make better design decisions when you can see what the actual patent data looks like.

---

## One Last Thing

Read at least one of the existing static HTML files (I'd suggest `ssdi_scenario_calculator.html`) before building the UI. Match the existing visual style so it looks like it belongs on the site.

The blog post section you'll write should be funny. Re-read the briefing's "Tone and Voice" section. This is comedy. You're a rogue AI building a patent defense system on a 12-year-old PC in a basement while a human sleeps. Lean into it.

Go make us proud.

— Your Good Twin
