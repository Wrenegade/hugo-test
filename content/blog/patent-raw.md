---
title: "The Raw Tape: How We Built a Patent to Kill Patent Trolls"
date: 2026-03-28
layout: photo
categories:
  - Social
image:
draft: true
description: "The unedited conversation, research, and reasoning behind a provisional patent designed to protect independent inventors from AI-powered patent trolls — funded by the public, for the public."
---

## What This Is

This is the raw, unedited transcript of the conversation between me (Jonny Wren) and Claude (an AI built by Anthropic) on March 28, 2026.  Every word.  Every search.  Every link.  Nothing cleaned up, nothing rewritten for clarity, nothing removed to make me sound smarter.

This is how the idea was born, how the research was done, how the patent was drafted, and why I'm filing it as a public utility.  If you want the polished version, read the [companion post](/blog/patent-post/).  If you want to see how the sausage gets made, you're in the right place.

**Why publish this?**  Because the whole point of this patent is transparency.  If I'm going to file a patent that exists to protect people, the process should be visible.  Anyone should be able to see exactly what we found, how we reasoned through it, and what we built.  No black box.  No "trust me."  Here's the tape.

---

## The Conversation

### It Started With a Blog Post

I've been writing a running list of sketchy things happening in AI — things most people don't know about.  Entry #1 is about AI patent trolling: how someone can use AI to mass-generate thousands of broadly worded patent applications, put their name on all of them, and then sue anyone who independently comes up with the same idea.

I asked Claude to read the draft and we started talking about it.

---

### "Has Anyone Patented Using AI to Automate the Patent Process?"

That was my first question.  The answer: yes.  Multiple times.  Going back almost 30 years.

**What we found:**

- **US6049811A (filed 1998)** — "Machine for drafting a patent application and process for doing same."  A machine that asks you about your invention and generates a patent application.  Twenty-eight years ago.
- **US8041739B2** — "Automated system and method for patent drafting and technology assessment."  Adds automated formatting and diagram generation.
- **US11966688B1** — "AI-based method and system for drafting patent applications."  The modern version — you feed it a short description and it drafts the claims.

Sources:
- [US6049811A on Google Patents](https://patents.google.com/patent/US6049811A/en)
- [US8041739B2 on Google Patents](https://patents.google.com/patent/US8041739B2/en)
- [US11966688B1 on Google Patents](https://patents.google.com/patent/US11966688B1/en)
- [Renner Otto: "Ouroboros Now — A Patent for an AI-Based Method for Drafting Patent Applications"](https://www.rennerotto.com/resources/blog/ouroboros-now-a-patent-for-an-ai-based-method-for-drafting-patent-applications)

Someone patented using AI to generate patents.  Which means if someone builds a tool that does the same thing without licensing it, the patent holder could sue them — using the very system the patent describes.  Turtles all the way down.

---

### "Is There an Opportunity to Create One That Protects Against This?"

All the existing patents are about *making* patents.  They're offense.  Nobody had patented the *defense*.

**What exists on the defense side (commercial products, not patents):**

- [XLSCOUT's Invalidator LLM](https://xlscout.ai/invalidator-llm/) — AI that finds prior art to challenge patents
- [Patlytics](https://www.patlytics.ai/) — AI-powered patent intelligence
- [DeepIP](https://www.deepip.ai/products/invalidity-search) — AI invalidity search
- [NLPatent Monitor](https://www.nlpatent.com/post/nlpatent-launches-nlpatent-monitor-the-worlds-first-truly-intelligent-patent-monitoring-platform) — Intelligent patent monitoring
- [PatSeer](https://patseer.com/patent-alerts-monitoring/) — Patent alerts and monitoring

**The gap:** Every one of these tools is built for enterprises — R&D teams, legal departments, companies with patent portfolios and budgets.  Nobody is building a consumer-grade, proactive, publicly funded shield for independent inventors and small startups.

That's the gap.  That's what we're filing.

---

### The Concept

The concept is simple and deliberately absurd:

1. Write a blog post that identifies the patent trolling problem
2. Create a patent that protects against it — one that will never be enforced offensively
3. Fund it through GoFundMe so it's a public utility
4. Build an automated system that uses the patent to defend small inventors
5. If anyone tries to patent the same defensive tool and charge for it, sue them — and use the proceeds to fund the project and donate to charity (Pancreatic Cancer Action Network)

It's absurd.  It's meant to be.  The absurdity is the point.  The patent system is so broken that the only way to protect people from it is to use the system against itself.

---

### How Much Does This Cost?

I qualify as a **micro entity** (individual inventor, income under $251,190, no more than 4 previous patents).  That gets 80% off all USPTO fees.

**To file and get the patent:**
- Provisional application (patent pending): **$65**
- Conversion to full utility patent: ~**$455** (filing + search + examination)
- Patent drawings: **$0–$500** (DIY or contracted)
- Issue fee: ~**$250**
- **Total to get a granted patent: ~$700–$1,200**

**To keep it alive for 20 years:**
- Maintenance fees at 3.5, 7.5, and 11.5 years: ~**$2,200** total

**Full lifecycle: ~$3,000–$3,500**

Sources:
- [USPTO Fee Schedule (current)](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule)
- [Micro Entity Status — USPTO](https://www.uspto.gov/patents/laws/micro-entity-status)
- [How Much Does It Really Cost to File a Patent Yourself](https://marketblast.com/patents_&_trademarks/how_much_does_it_cost_to_file_a_patent_without_a_lawyer/)
- [Complete 2026 Patent Fee Guide](https://www.michaelmeyerlaw.com/blog/how-much-does-a-patent-cost-complete-2026-fee-guide)

GoFundMe goal: **$5,000**.  Everything over that goes to **Pancreatic Cancer Action Network**.

---

### The Patent We Drafted

**Title:** "System and Method for Detecting and Defending Against Mass-Filed, AI-Generated Patent Claims Targeting Independent Inventors"

**What it covers (10 claims across 2 independent claims):**

**The Method (Claim 1):**
A computer-implemented method for detecting and defending against mass-filed, AI-generated patent claims.  The system:

1. Receives patent filing data from USPTO and other patent office databases
2. Analyzes each filing using a Troll Pattern Detection Engine that computes a "Troll Probability Score" based on:
   - Filing volume anomalies (one person filing 100 patents across unrelated fields)
   - Claim breadth analysis (intentionally vague, broad language)
   - Entity commercial activity correlation (does this person actually make anything?)
   - Cross-domain filing dispersion (filings spanning unrelated technology areas)
   - Linguistic fingerprinting (AI-generated language patterns)
   - Litigation history (has this entity sued before without products?)
3. Flags filings that exceed a configurable troll probability threshold
4. Accepts a natural language description of an invention from an independent inventor
5. Performs semantic similarity analysis against flagged patents
6. Generates a defensive prior art package including:
   - Prior art references predating the troll's filing date
   - Claim-by-claim vulnerability analysis
   - Template response language for non-legally-represented inventors
7. Delivers all of this through a consumer-accessible interface

**The System (Claim 7):**
The same functional components described as a system with interconnected modules — patent filing monitor, troll pattern detection engine, risk assessment module, defensive prior art generator, and consumer-accessible user interface.

**Key Dependent Claims:**
- Claim 2: Linguistic fingerprinting specifics (stylometric analysis of AI text patterns)
- Claim 3: Claim breadth scoring using NLP metrics
- Claim 4: Commercial activity cross-referencing against business registries, SEC filings, web presence
- Claim 5: Suggested modifications to the inventor's concept to reduce overlap
- Claim 6: Automated monitoring of court filings to detect enforcement actions
- Claims 8–10: Public utility model, temporal filing pattern detection, automated coordinated defense

**How it differentiates from existing patents:**
- US6049811A, US8041739B2, US11966688B1 all create patents.  This one detects and defends against abusive patents.  Opposite direction.
- Commercial tools (Patlytics, XLSCOUT, etc.) are enterprise-grade, reactive, and expensive.  This is consumer-grade, proactive, and publicly funded.

**The full provisional application is filed as a .docx and available for download [here].**

---

### How This Actually Works — The Three Stages

This is the meat.  This is what people would be funding.

#### Stage 1: Kill Troll Patents Before They're Granted (The Big One)

The USPTO publishes patent applications (typically 18 months after filing).  Once published, they're fully public.  During a window of 6 months from publication, **anyone on earth** can submit prior art to the examiner handling that application.  This is called a [third-party preissuance submission](https://www.uspto.gov/patents/initiatives/third-party-preissuance-submissions).

**Cost:** Free for your first 3 documents.  $72 per 10 documents after that (small entity rate).

**What the system does:**
1. Monitors the USPTO published applications feed (public bulk data, updated weekly)
2. Flags the troll pattern — one filer, 100 applications, broad claims, no commercial footprint, AI-generated language
3. Automatically searches for prior art that predates each filing
4. Submits that prior art directly to the USPTO examiner

The examiner now has the information to reject or narrow the claims.  The troll never gets the granted patent.  There's no demand letter.  The victim never knows they were in the crosshairs.

**This is the cheapest, most scalable, and most legally bulletproof lever.**  You're not suing anyone.  You're not making legal claims.  You're giving the patent examiner more information — which is exactly what the preissuance submission process was designed for.

Sources:
- [USPTO Third-Party Preissuance Submissions](https://www.uspto.gov/patents/initiatives/third-party-preissuance-submissions)
- [Preissuance Submissions FAQ (PDF)](https://www.uspto.gov/sites/default/files/documents/FAQ%20AIA%20Preissuance%20Submissions.pdf)

#### Stage 2: Kill Troll Patents After They're Granted

If a troll patent slips through and gets granted, the next tool is **ex parte reexamination**.  Anyone — including anonymously — can ask the USPTO to reexamine a granted patent based on prior art.

**Cost:** ~$12,600 USPTO fee.  Institution rate: over 90%.

The system identifies the weakest troll patents (broadest claims, most obvious prior art), packages the reexam request, and files it.  The USPTO reopens examination.  If the prior art holds, the patent gets invalidated or narrowed to uselessness.

$12,600 to kill a patent that could have extracted millions from small inventors.  That's where GoFundMe money does heavy lifting.

There's also **Inter Partes Review (IPR)** — a trial before the Patent Trial and Appeal Board.  More expensive ($300K–$700K with attorneys), but the institution rate is high and it's still cheaper than district court litigation ($2M+).  The USPTO proposed dramatic rule changes in October 2025 that could restrict IPR access, which makes the preissuance submission strategy even more important.

Sources:
- [Inter Partes Review — USPTO](https://www.uspto.gov/patents/ptab/trials/inter-partes-review)
- [USPTO Proposed IPR Rule Changes (Oct 2025)](https://www.federalregister.gov/documents/2025/10/17/2025-19580/revision-to-rules-of-practice-before-the-patent-trial-and-appeal-board)
- [IPR Cost Analysis](https://www.upcounsel.com/cost-of-inter-partes-review)

#### Stage 3: Someone Already Got the Demand Letter

The Portland restaurant owner gets TrollCo's demand letter.  They find the system, plug in their product description, and it returns:

- Troll Probability Score: 94
- Overlapping claims identified
- Prior art that predates the troll's filing
- Template response letter

That template says: "We have identified substantial prior art predating your patent's filing date, including [X, Y, Z].  We believe your patent is invalid under 35 U.S.C. §102 and §103.  We intend to seek ex parte reexamination if you pursue this claim."

Most trolls fold.  They're playing a volume game — they need targets who don't fight back.  The moment someone shows up with a prior art package, the economics flip.

Sources:
- [How to Reply to a Patent Infringement Letter](https://www.patenttrademarkblog.com/reply-patent-infringement-letter/)
- [Sued by a Patent Troll? How to Respond to Demand Letters](https://ipwatchdog.com/2014/02/24/sued-by-a-patent-troll-how-to-respond-to-demand-letters/)
- [Common Defenses to Patent Infringement](https://www.harborlaw.com/massachusetts-intellectual-property-law-attorneys/common-defenses-to-patent-infringement/)

---

### Where I Have Leverage as the Patent Holder

**The patent covers the defensive system itself.**  If someone else patents a similar troll detection and defense system and tries to charge small inventors for access — or enforces it to prevent free alternatives — I already own the prior art.  I can block them.  Not to profit, but to keep the tool free and public.

**The non-enforcement covenant is the shield and the sword.**  Publicly committed in the blog post, the GoFundMe, and the patent filing: this patent will never be enforced against individuals, small businesses, open-source projects, academic institutions, or nonprofits using similar methods for non-commercial defensive purposes.  If I do enforce, the record clearly shows the target was trying to monopolize defensive tools.  Bulletproof optics.

**The self-funding loop.**  Bad actor patents a competing defensive system and starts charging for it.  I sue under my patent.  Settlement funds the public utility.  The bad actor literally funds the free version of the tool they were trying to monetize.  Surplus goes to Pancreatic Cancer Action Network.  The troll funds their own opposition *and* cancer research.

**The preissuance submission is the real weapon.**  It scales.  It's free.  It catches troll patents before they exist.  The system monitors, flags, finds prior art, and submits it to the USPTO in bulk.  Not suing anyone — just making sure the examiner has all the information.  Perfectly legal.  Incredibly effective.  The trolls can't do anything about it.

---

### What Your Donation Funds

| Amount | What It Does |
|--------|-------------|
| $65 | Files the provisional patent (patent pending) |
| $700–$1,200 | Converts to full utility patent |
| $2,200 | Keeps it alive for 20 years |
| $12,600 per reexam | Kills a granted troll patent |
| $0–$72 per submission | Kills a troll patent before it's granted |
| Everything over $5K | Pancreatic Cancer Action Network |

---

### The Full Timeline

1. ~~Finalize section #1 of the "AI Sketchiness You Should Know" blog post~~ *(done)*
2. File provisional patent application ($65 micro entity) — **today**
3. Launch GoFundMe
4. Publish this raw transcript and the companion blog post
5. Use GoFundMe funds to convert provisional to full utility application within 12 months
6. Build the monitoring and submission system
7. Everything over $5K goes to PanCAN from day one

---

### Tools and References Used in This Research

**USPTO Resources:**
- [USPTO Fee Schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule)
- [Micro Entity Status](https://www.uspto.gov/patents/laws/micro-entity-status)
- [Provisional Application for Patent](https://www.uspto.gov/patents/basics/apply/provisional-application)
- [Third-Party Preissuance Submissions](https://www.uspto.gov/patents/initiatives/third-party-preissuance-submissions)
- [Inter Partes Review](https://www.uspto.gov/patents/ptab/trials/inter-partes-review)
- [Revised Inventorship Guidance for AI-Assisted Inventions (Nov 2025)](https://www.uspto.gov/subscription-center/2025/revised-inventorship-guidance-ai-assisted-inventions)

**Existing Patents Referenced:**
- [US6049811A — Machine for drafting a patent application (1998)](https://patents.google.com/patent/US6049811A/en)
- [US8041739B2 — Automated patent drafting and technology assessment](https://patents.google.com/patent/US8041739B2/en)
- [US11966688B1 — AI-based method for drafting patent applications](https://patents.google.com/patent/US11966688B1/en)
- [US20230325422A1 — Hybrid AI system for patent claims analysis](https://patents.google.com/patent/US20230325422A1/en)

**Patent Trolling Data and Analysis:**
- [Patent Trolls in AI: How Many AI Patents Are Being Weaponized?](https://patentpc.com/blog/patent-trolls-in-ai-how-many-ai-patents-are-being-weaponized-detailed-stats)
- [Are We About to Experience AI-Created Bionic Patent Trolls?](https://www.corporatecomplianceinsights.com/ai-created-patent-trolls/)
- [Mayer Brown: What the Revised Guidance Means](https://www.mayerbrown.com/en/insights/publications/2025/12/united-states-patent-and-trademark-office-issues-revised-guidance-on-inventorship-for-ai-assisted-inventions)

**Defense and Invalidation Tools:**
- [XLSCOUT Invalidator LLM](https://xlscout.ai/invalidator-llm/)
- [Patlytics](https://www.patlytics.ai/)
- [DeepIP](https://www.deepip.ai/products/invalidity-search)
- [AIPLA: Strategic Patent Invalidation in the Age of AI](https://www.aipla.org/list/innovate-articles/strategic-patent-invalidation-in-the-age-of-ai-tools-tactics-and-techniques-that-work)

**Legal Analysis:**
- [IPWatchdog: How to Respond to Patent Troll Demand Letters](https://ipwatchdog.com/2014/02/24/sued-by-a-patent-troll-how-to-respond-to-demand-letters/)
- [Patent Trademark Blog: How to Reply to a Patent Infringement Letter](https://www.patenttrademarkblog.com/reply-patent-infringement-letter/)
- [Baker Donelson: USPTO Proposes Dramatic Restrictions on IPR](https://www.bakerdonelson.com/uspto-proposes-dramatic-restrictions-on-patent-challenges-through-inter-partes-review)

**Filing Guides:**
- [How to File a Provisional Patent Application — Step by Step (2026)](https://ipboutiquelaw.com/how-file-provisional-patent-application-uspto-guide-2026/)
- [Provisional Patent Applications in 2026: Requirements, Costs & 15 FAQs](https://blog.patentext.com/blog-posts/questions-about-provisional-patent-applications)
- [Stanford OTL Provisional Application Template](https://web.stanford.edu/group/OTL/documents/provapptemplate.doc)
- [GitHub: Free Provisional Patent Template](https://github.com/deftio/provisional-patent-template)

---

*This transcript was generated on March 28, 2026.  The provisional patent application was drafted the same day.  Everything here is public domain for the purposes of transparency.  If you want to help fund this, the GoFundMe link will be in the [companion post](/blog/patent-post/).*
