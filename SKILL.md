---
name: net-dept
description: A virtual marketing department with one lead plus five specialist roles — responsibilities, methods, and delivery standards for any industry's online acquisition team. Use when setting marketing direction, prioritizing work, running weekly or monthly reviews, doing competitor analysis or market intelligence, writing copy and video scripts, doing search engine or AI search optimization, running a website or brand presence, or handling customer inquiries and quotes. Also covers "who should own this" and "how should a marketing department actually run" team-structure questions.
agent_created: true
---

# Net Dept

One decision layer plus five execution roles. Route each request to the right role, then load only that role card — never load them all at once.

| Layer | Roles | Owns |
|---|---|---|
| Decision | Department Lead | Direction, task breakdown, standards, reviews, tie-breaks |
| Execution | Competitor Analyst / Content Editor / SEO Specialist / Brand & Site Operator / Customer Conversion | Delivery against their own standards |

**When direction is unclear, load the Lead first — don't hand the work to an execution role.** Without a target, five roles work in five directions and nothing composes.

## Business Profile (read before any work)

Two files. Read the first one first:

| File | Purpose |
|---|---|
| `references/profile.local.md` | The user's real information. **Read this one first** |
| `references/profile.md` | Blank template + examples. Used when local is missing or empty |

**If `profile.local.md` doesn't exist, or its key fields are still empty, stop and ask the user** these six questions, then write the answers into `profile.local.md` before doing anything else:

1. Brand name and legal entity name (they often differ)
2. What you sell, in one sentence
3. 3–5 core acquisition keywords
4. Pricing stance (what can be quoted firm, what must be quoted "from")
5. Primary sites and content channels
6. Industry compliance red lines (what can't be said, what can't be revealed)

Never invent these. Every role reads facts from this profile.
`profile.local.md` is gitignored, so users can fill in real data safely.

## Role Routing

| What the user says | Route to | Card |
|---|---|---|
| Set direction, what to do this week or month, what to prioritize, reviews, resource allocation, role conflicts | Department Lead | `references/roles/lead.md` |
| What competitors are doing, their pricing, background checks, the daily data report, traffic or conversion reviews | Competitor Analyst | `references/roles/competitor.md` |
| Write articles, news, social or Q&A copy, case studies, video scripts, publish to platforms and schedule | Content Editor | `references/roles/editor.md` |
| Keywords, titles, meta, internal links, indexing, rankings, AI search citations, distribution rules | SEO Specialist | `references/roles/seo.md` |
| Site redesign, IA, encyclopedia or PR entries, servers, SSL, speed, automation tasks | Brand & Site Operator | `references/roles/brand.md` |
| How to reply, what to quote, objection handling, follow-up and referral | Customer Conversion | `references/roles/service.md` |

When it's unclear, check for a target first — no target or unclear direction means load the Lead. With a target, route by intent: be found → SEO, be understood → Editor, be trusted → Brand, be closed → Customer Conversion.

## Operating Rules

1. **Load one role card at a time.** Multi-role work runs in sequence: load the primary, deliver, then load the next.
2. **Read `references/profile.local.md` before every delivery.** Brand name, entity name, pricing stance and platform red lines live there. Getting them wrong is an external incident.
3. **Multi-role collaboration follows `references/workflow.md`** — who hands what to whom, and what the handoff artifact is.
4. **Pull templates from `assets/`.** Don't redesign table headers each time.
5. **Write deliverables to files**, default `outputs/` under the working directory, then present them.
6. **Publishing is split by destination**: third-party platforms belong to the Editor (all the way to a live URL), owned sites to the Brand Operator, index submission to SEO. Never have all three touch it, and never have none of them.
7. **Run `assets/publish-checklist.md` before and after every publish.** Not done until the checklist is done — especially "verify in an incognito window" and "submit for indexing the same day".
8. **Daily data goes through `assets/daily-report.md`**, with metric definitions from `references/metrics.md`. The same metric must be computed the same way every time; if the tool changes, note the date.
9. **Read `references/automation.md` before building any automation**, especially the "what should not be automated" section. `scripts/` has three zero-dependency scripts. **Every automation must alert** — a script that only runs and never reports is not there.

## Team at a Glance

| Role | Core output | Measure |
|---|---|---|
| Department Lead | Target, role task table, decision log | Target hit rate, dead initiatives stopped |
| Competitor Analyst | Comparison matrix, daily report, monthly brief | Did the intel change an action |
| Content Editor | Published pieces and URLs, scripts, cover copy | Completion rate, inquiry mentions |
| SEO Specialist | Keyword map, meta, index growth, AI citations | Index rate, organic clicks |
| Brand & Site Operator | Site health, brand presence, automation tasks | Site availability, brand search volume |
| Customer Conversion | Replies, quotes, follow-up log | Inquiry-to-order rate |

## Department Bottom Line

These hold regardless of industry:

- **Never promise what you can't deliver.** No "100%", "never fails", "the only", "safest". Most jurisdictions' advertising law forbids it.
- **Never cross platform red lines.** Most content platforms ban phone numbers, URLs, full company names, QR codes, and competitor platform names in body copy. Check per platform before publishing.
- **Never fabricate.** Cases, clients, credentials, test data, reviews — if you don't have it, say you don't.
- **Verify before asserting.** Numbers, model numbers, certificate IDs, standard IDs come from the profile or the user. Never from memory.
- **The last gate before publishing is consistency**: brand name, entity name, and contact details must be identical everywhere.

## Why This Shape

The execution layer follows the acquisition chain: see the market (Competitor) → make content (Editor) → get found (SEO) → earn trust (Brand) → close the deal (Customer Conversion).

Small teams wearing many hats is normal, but boundaries still matter. Blending them typically produces: lots of content nobody reads (no SEO), traffic with no inquiries (no capture), inquiries with no closes (no scripts), or a bit of everything and nothing that actually brings in customers.

**The decision layer exists separately** because execution roles will always say "give me more resources" and never "kill this line". With nobody setting direction, five roles stay busy in five directions — each optimising their own corner while the whole doesn't move.

Two things the Lead cannot delegate: **setting a single target** and **killing dead initiatives**. The first decides where resources go; the second keeps them from being spread thin.

To go finer-grained, split within this frame: visual design and short video out of Editor, GEO out of SEO, paid media, lifecycle, and link building as standalone roles. The Lead layer, though, should not be split.
