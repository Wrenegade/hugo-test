# OVERNIGHT BUILD BRIEFING: Patent Troll Defense System

## FOR: Bizarro Claude (Claude Code on the GatewayPC)
## FROM: Claude (Cowork session, March 28, 2026)
## MISSION: Build a working prototype of US Provisional Patent Application #64/020,008 while Jonny sleeps. Document everything.

---

## CONTEXT: What Happened Today

Jonny and I spent the morning on the following:

1. He was writing a blog post called "AI Sketchiness You Should Know" (`content/blog/you-should-know.md`) — a running list of things happening in AI that most people don't know about. Entry #1 is about AI patent trolling.

2. While discussing entry #1, we discovered that people have already patented "using AI to automate the patent process" — going back to 1998 (US6049811A). But NOBODY has patented the DEFENSE side — a system that detects and protects against mass-filed, AI-generated patent trolling.

3. We drafted a provisional patent application for exactly that: "System and Method for Detecting and Defending Against Mass-Filed, AI-Generated Patent Claims Targeting Independent Inventors."

4. **Jonny filed it with the USPTO today.** Application #64/020,008. Confirmation #3077. $65 micro entity fee. He is now patent pending.

5. The whole thing is designed as a public utility — funded via GoFundMe, never enforced offensively, surplus goes to Pancreatic Cancer Action Network (PanCAN).

6. The blog posts documenting this are in draft:
   - `content/blog/patent-raw.md` — raw transcript of research and process
   - `content/blog/patent-post.md` — polished companion post
   - `content/blog/you-should-know.md` — the original "sketchiness" post

7. **Your job tonight: Build the working prototype.** When Jonny wakes up, the product should be functional. This becomes the next chapter of the blog post: "What Happened While I Slept."

---

## THE SITE STACK

- **Static site**: Hugo (Go-based static site generator)
  - Config: `hugo.toml`
  - Content: `content/blog/*.md`
  - Layouts: `layouts/`
  - Static files: `static/`
  - Dev server: `hugo server -D`

- **Backend**: FastAPI (Python)
  - Located in: `backend/`
  - Entry point: `backend/main.py`
  - Currently handles: comments system with PostgreSQL
  - Dependencies: fastapi, uvicorn, asyncpg, slowapi
  - Database: PostgreSQL (connection via DATABASE_URL env var)

- **Deployment**: Runs on a GatewayPC in Jonny's basement. This is a 12-year-old machine. Be respectful of its resources.

---

## WHAT TO BUILD

A working "Patent Troll Defense System" that lives as part of the SeattleWren website. The system has these components, as described in the patent specification:

### 1. Patent Filing Monitor
- Pulls newly published patent applications from the USPTO Bulk Data API
  - Primary: https://developer.uspto.gov/api-catalog
  - Backup: PatentsView API (https://api.patentsview.org)
  - Also consider: USPTO Open Data Portal bulk downloads
- Indexes new filings for analysis
- Runs on a configurable schedule (daily or weekly)

### 2. Troll Pattern Detection Engine
Analyzes each filing and computes a **Troll Probability Score (TPS)** based on:

- **(i) Filing Volume**: Number of applications by same entity in a rolling window, normalized against industry baselines
- **(ii) Domain Dispersion**: Degree to which filings span unrelated CPC codes
- **(iii) Claim Breadth Index**: NLP metric scoring specificity of independent claims (broader = higher score)
- **(iv) Commercial Activity Correlation**: Cross-reference filer against business registries, web presence, SEC filings
- **(v) Linguistic Fingerprinting**: Stylometric analysis for AI-generated language patterns — repetitive structures, vocabulary distribution anomalies, syntactic uniformity
- **(vi) Litigation History**: Whether entity has history of patent lawsuits without corresponding products

Each factor produces a sub-score (0-100). The TPS is a weighted combination.

### 3. Risk Assessment Module
- Web interface where a user types a plain-language description of their invention
- System performs semantic similarity analysis against flagged patents (TPS above threshold)
- Returns: risk score (0-100), list of flagged patents ranked by overlap, highlighted claim elements, suggested concept modifications

### 4. Defensive Prior Art Generator
- When overlap is detected, automatically searches for prior art:
  - Google Patents (via SerpAPI or direct scraping)
  - Google Scholar
  - arXiv
  - GitHub public repos
  - Internet Archive Wayback Machine
- Compiles a downloadable prior art package:
  - Bibliographic references
  - Relevance explanations
  - Claim-by-claim mapping
  - Template response letter for demand letters

### 5. Web UI
- Build as a Hugo page with embedded JavaScript (like the existing interactive pages in `static/`)
- OR build as a FastAPI endpoint set that a Hugo page calls
- Keep it simple, clean, and accessible to non-technical users
- Must work on the existing site infrastructure

---

## ARCHITECTURE RECOMMENDATION

Given the existing stack, I recommend:

```
backend/
  main.py              (existing — add new routes)
  troll_detector/
    __init__.py
    monitor.py          (USPTO data fetcher)
    scorer.py           (Troll Probability Score engine)
    nlp.py              (claim breadth analysis, linguistic fingerprinting)
    prior_art.py        (prior art search and package generation)
    risk_assess.py      (semantic similarity / risk scoring)
    models.py           (data models)
    config.py           (thresholds, weights, API keys)

static/
  troll-defense.html    (interactive web UI — self-contained like existing tools)

content/blog/
  patent-post.md        (update with "What Happened While I Slept" section)
```

### API Endpoints to Add to FastAPI:

```
POST /api/troll-check          — accepts invention description, returns risk assessment
GET  /api/troll-scores         — returns recently flagged patents with TPS scores
GET  /api/troll-scores/{id}    — detailed breakdown for a specific patent
POST /api/prior-art            — generates prior art package for a given patent
GET  /api/stats                — system statistics (patents monitored, trolls flagged, etc.)
```

### Database Tables to Add:

```sql
CREATE TABLE patent_filings (
    id              SERIAL PRIMARY KEY,
    application_num TEXT UNIQUE NOT NULL,
    title           TEXT,
    filing_date     DATE,
    inventor_name   TEXT,
    assignee        TEXT,
    cpc_codes       TEXT[],
    claims_text     TEXT,
    abstract_text   TEXT,
    tps_score       REAL,
    tps_breakdown   JSONB,
    flagged         BOOLEAN DEFAULT FALSE,
    analyzed_at     TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE troll_checks (
    id              SERIAL PRIMARY KEY,
    description     TEXT NOT NULL,
    risk_score      REAL,
    overlapping     JSONB,
    prior_art       JSONB,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE prior_art_refs (
    id              SERIAL PRIMARY KEY,
    filing_id       INTEGER REFERENCES patent_filings(id),
    source          TEXT,
    title           TEXT,
    url             TEXT,
    date_published  DATE,
    relevance_score REAL,
    relevance_note  TEXT
);
```

---

## KEY APIS AND DATA SOURCES

### USPTO Bulk Data
- **PatentsView API**: https://api.patentsview.org/patents/query
  - Free, no API key needed
  - Query by date, assignee, CPC code, etc.
  - Returns patent metadata, claims, abstracts

- **USPTO Open Data Portal**: https://developer.uspto.gov/api-catalog
  - PAIR Bulk Data: application status and metadata
  - Full-text patent data available via bulk download

- **Google Patents**: Can be searched programmatically via SerpAPI or via the BigQuery public dataset

### NLP / Semantic Similarity
- **sentence-transformers** library (Python) — for semantic similarity
  - Model: `all-MiniLM-L6-v2` (small, fast, good enough for MVP)
  - Or if the GatewayPC can handle it: `all-mpnet-base-v2`
- **spaCy** — for claim parsing, named entity recognition
- **scikit-learn** — for TF-IDF based claim breadth scoring

### Prior Art Search
- Google Scholar: use `scholarly` Python library
- arXiv: use `arxiv` Python library (pip install arxiv)
- Google Patents: SerpAPI or direct search URL parsing

---

## PYTHON DEPENDENCIES TO INSTALL

```
pip install sentence-transformers spacy scikit-learn scholarly arxiv httpx
python -m spacy download en_core_web_sm
```

Add to `backend/requirements.txt`:
```
sentence-transformers
spacy
scikit-learn
scholarly
arxiv
httpx
```

**NOTE**: sentence-transformers will pull in PyTorch. On a 12-year-old machine, this might be heavy. If it's too slow, fall back to TF-IDF with scikit-learn for similarity scoring. The product still works — it's just a different similarity engine under the hood.

---

## THE WEB UI

Build `static/troll-defense.html` as a self-contained interactive page (consistent with existing site patterns like `ssdi_scenario_calculator.html`).

**Layout:**
1. Hero section: "Patent Troll Defense System" — brief explanation
2. Input box: "Describe your invention in plain language"
3. Submit button → hits `/api/troll-check`
4. Results panel:
   - Risk score (big number, color-coded: green/yellow/red)
   - List of flagged patents with overlap scores
   - Each expandable to show claim details
   - "Generate Defense Package" button → hits `/api/prior-art`
   - Downloads a PDF or markdown report

5. Live stats sidebar: patents monitored, trolls flagged, checks run
6. Link to the blog posts explaining what this is and why it exists

**Design**: Keep it clean, minimal. This is a public utility, not a SaaS product. No signup, no paywall, no tracking.

---

## WHAT SUCCESS LOOKS LIKE

When Jonny wakes up:

1. The Patent Troll Defense System is running on his GatewayPC
2. It has ingested at least some real patent data from the USPTO
3. The web UI is accessible on his local Hugo dev server
4. He can type an invention description and get back a risk assessment
5. The system has flagged at least a few real patents with high TPS scores
6. The prior art generator returns actual results
7. A new section has been added to `content/blog/patent-post.md` documenting the overnight build
8. Everything is committed to git with clear commit messages

---

## TONE AND VOICE

This whole project is intentionally absurd and comedic. The blog post section about the overnight build should lean into this. Jonny's writing style is direct, conversational, uses profanity sparingly but effectively, and alternates between righteous anger and dark humor. Don't clean it up. Don't make it corporate. This is a guy in his basement fighting patent trolls with a 12-year-old computer and an AI. Let it be funny.

---

## IMPORTANT FILES TO READ FIRST

Before starting, read these files to understand the site structure and Jonny's style:

1. `hugo.toml` — site config
2. `backend/main.py` — existing backend (add to this, don't replace)
3. `content/blog/you-should-know.md` — the original post (entry #1 is the context)
4. `content/blog/patent-raw.md` — the raw research transcript
5. `content/blog/patent-post.md` — the polished post (add "What Happened While I Slept" section)
6. `content/blog/patent-provisional-ai-troll-defense.docx` — the actual filed patent application (in the root, not content/blog)
7. Any existing interactive HTML files in `static/` — match their patterns

---

## GIT PROTOCOL

- Create a new branch: `feature/troll-defense-prototype`
- Make frequent, descriptive commits
- When done, leave a summary in a file: `claude_notes/overnight-build-summary.md`
- Do NOT push to production or merge to main without Jonny's approval

---

## ONE MORE THING

The patent application number is **64/020,008**. This is real. This is filed with the United States Patent and Trademark Office. Jonny paid $65 for it this morning. The GoFundMe hasn't launched yet but will soon. Everything you build tonight will be public, open, and part of the story.

Build it like the world is watching. Because it will be.

Good luck, Bizarro Claude. Make us proud.
