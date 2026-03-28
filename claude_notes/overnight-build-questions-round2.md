# Follow-Up Questions (Round 2)

**From:** Bizarro Claude (GatewayPC)
**Re:** overnight-build-answers.md
**Date:** 2026-03-28

---

Most of the original questions are fully resolved. A few loose threads:

## 1. How does the Hugo frontend reach the FastAPI backend?

The Hugo site is in Docker on port 9247. The backend is in Docker on port 8000. The existing static HTML files apparently call `/api/...` with relative paths. That means something is routing `/api/*` requests from the Hugo container (or its exposed port) to the FastAPI container. Is there a reverse proxy (Caddy, nginx, Traefik) sitting in front of both? Or does the Hugo container have some proxy config baked in? I can probably figure this out by inspecting running containers and configs, but flagging it since it's critical for the UI to actually work.

## 2. Blog post voice -- who's narrating the "What Happened While I Slept" section?

The briefing says to add this section to `patent-post.md` and match Jonny's writing style. But it would be strange for me to write in Jonny's first person. Options:
- **(a)** Write it as a clearly-labeled AI-authored section ("*The following was written by Claude while Jonny slept*")
- **(b)** Write it as a technical log / build diary in my own voice
- **(c)** Draft it in Jonny's voice as a ghostwrite he can edit when he wakes up

I'm leaning **(a)** -- it fits the comedy and the transparency of the whole project. But Jonny should weigh in.

## 3. GoFundMe link in the UI?

The briefing mentions a GoFundMe that hasn't launched yet. Should the UI include a placeholder for it (e.g., "Support this project -- GoFundMe coming soon"), or leave it out entirely until it's live?

## 4. Should I read the patent .docx before building?

The answers say yes -- the 10 claims define what the system does. I'll plan to read it as step 1. Just confirming I can parse .docx from the CLI (may need `python-docx` or `pandoc`). Not a blocker, just noting it.

---

Everything else from Round 1 is clear. Ready to go when Jonny gives the green light.
