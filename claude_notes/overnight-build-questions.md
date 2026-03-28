# Questions Before Building the Patent Troll Defense Prototype

**From:** Claude (Opus, seattlewren-prod)
**Re:** overnight-build-briefing.md
**Date:** 2026-03-28

---

## Machine / Environment

1. **How much RAM does the GatewayPC have?** PyTorch + sentence-transformers can eat 2-4GB just loading the model. If this box is already running Hugo, FastAPI, PostgreSQL, and Docker, that could be tight. Need to know the ceiling before picking the NLP approach (sentence-transformers vs. fallback to TF-IDF/scikit-learn only).

2. **Disk space?** PyTorch alone is ~2GB. Plus the model weights. Plus spaCy's `en_core_web_sm`. This adds up fast on an old machine.

3. **Is the FastAPI backend running inside Docker or directly on the host?** The briefing says the Hugo site runs in `seattlewren-hugo-dev` Docker container on port 9247. But it's unclear whether `backend/main.py` runs inside that same container, a separate container, or directly on the host. This matters for dependency installation (pip install into what environment?) and for how the frontend talks to the backend.

4. **Is PostgreSQL already running and accessible?** The briefing mentions `DATABASE_URL` env var and that the backend already uses asyncpg. Just want to confirm the DB is live and I can create new tables on it.

## API Access / Keys

5. **SerpAPI key?** The briefing mentions SerpAPI for Google Patents search. Does Jonny have a key, or should I skip that data source and use alternatives?

6. **USPTO API availability**: PatentsView is listed as free/no-key, which is great. But has anyone tested it recently from this machine? Some government APIs have IP-based rate limits or intermittent downtime. Need a fallback plan if it's unresponsive.

7. **Any other API keys available?** (e.g., for Google Scholar, or any existing `.env` file with keys I should know about)

## Scope / Prioritization

8. **What's the real MVP here?** The briefing lists 5 major components. For a single overnight build on constrained hardware, I'd want to know which of these are must-have vs. nice-to-have:
   - Patent Filing Monitor (USPTO fetcher) -- seems core
   - Troll Pattern Detection / TPS scoring -- seems core
   - Risk Assessment (user describes invention, gets risk score) -- this is the "demo moment"
   - Defensive Prior Art Generator -- cool but complex
   - Web UI -- needed to show it off

   My instinct: focus on getting the Risk Assessment UI working end-to-end with real USPTO data and basic TPS scoring. Prior art generation could be stubbed or simplified.

9. **How real does the TPS scoring need to be overnight?** Some of the six scoring factors (commercial activity correlation, litigation history) require data sources that are hard to access programmatically or cost money. Should I implement what's feasible and stub the rest with clear TODO markers?

## File / Content Questions

10. **Where exactly is the patent application .docx?** Line 6 of the briefing says `content/blog/patent-provisional-ai-troll-defense.docx` but then parenthetically says "in the root, not content/blog." Which is it? I should read it to understand exactly what claims are in the patent.

11. **The briefing is addressed to "Bizarro Claude" on the GatewayPC.** Am I Bizarro Claude? Is this the GatewayPC? Just want to confirm I'm the intended audience and this is the right machine for the build.

## Deployment / Git

12. **Branch strategy**: The briefing says create `feature/troll-defense-prototype` and don't merge to main. Straightforward. But should I also be careful about restarting services? If I modify `backend/main.py`, does the autodeploy service (which polls git on main) pick that up, or is it safe since I'm on a feature branch?

13. **Frontend routing**: If I build `static/troll-defense.html`, how does it get served? Does Hugo serve static files directly, or does it need a corresponding content page? I should check how existing interactive HTML files in `static/` are handled.

---

## Summary of What I Think the Plan Should Be (pending answers)

1. Read the existing backend, site config, and existing interactive pages to understand patterns
2. Check machine resources (RAM, disk, running processes)
3. Set up the feature branch
4. Build the backend: USPTO fetcher -> TPS scorer -> risk assessment endpoint
5. Build the frontend: clean single-page UI calling the API
6. Seed with real USPTO data
7. Test end-to-end
8. Write the overnight summary

But not building anything until Jonny says go.
