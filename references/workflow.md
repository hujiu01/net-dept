# Collaboration Chains

When roles hand off to each other, follow these orders. Every link has a required handoff artifact — if it's missing, bounce it back. Don't carry a gap downstream.

## Chain 0: Set direction (start of every cycle)

```
Department Lead ──→ five execution roles
  one target          one task each
```

| Link | Handoff | Acceptance |
|---|---|---|
| Lead → roles | Target + role task table | Exactly one target; exactly one task per role |
| Task table → delivery | Each task has deliverable, deadline, acceptance criteria | All three, or it isn't broken down |

Without this, chains 1–4 still happen — every role stays busy and the direction is scattered. **This is the most common form of waste, and the hardest to notice, because everyone looks busy.**

## Chain 1: Routine content

```
Competitor Analyst → SEO → Content Editor (write→adapt→publish) → SEO → Brand Operator
   pick topics         keywords    draft and publish            submit    sync to owned site
```

| Link | Handoff | Acceptance |
|---|---|---|
| Intel → keywords | This week's real customer questions | Sourced from actual inquiries, not guesswork |
| Keywords → draft | Target term + 3 title options + battleground | Clear whether it's for ranking or for AI citation |
| Draft → publish | Per-platform finals + schedule | Real differences between platforms, red lines cleared |
| Publish → submit | Live URLs + first-day data | Verified on the real URL, not a backend preview |
| Submit → site | Final copy + internal link requirements | Brand Operator publishes per CMS conventions |

**Publishing ownership**: third-party platforms — the Editor publishes them; owned sites — the Brand Operator; index submission — SEO. Don't have all three touch it, and don't have none of them.

**Most common break**: intel delivers a pile of data with no topics, so the Editor has nothing to write about and defaults to product brochures.

## Chain 2: New site or redesign

```
Brand Operator → SEO → Content Editor → Brand Operator
   structure       terms + links    fill content     verify live
```

Before any redesign, three things are mandatory: full backup, old-URL-to-new-URL map, page-by-page verification after launch.
Skip the map and historic indexed pages break en masse — you start over from zero.

## Chain 3: Inquiry handling

```
SEO / content creates traffic → Customer Conversion → Competitor Analyst
        acquisition                close              attribution
```

After closing, route the customer's actual words back to the Analyst as input for the next topic cycle. **The loop is what makes it a review** — without feedback it's a one-off sale.

## Chain 4: Incidents

Site down, index collapsed, account restricted:

```
Brand Operator (technical) → SEO (indexing) → Content Editor (content)
```

Rule out technical causes first, then indexing, then platform rules and content.
Getting the order wrong wastes weeks — e.g. a CDN blocking crawlers while you spend two weeks rewriting copy.

## Cross-role conventions

1. Handoff artifacts are files, never verbal descriptions
2. Every role checks the red lines in `references/profile.local.md` before delivery
3. Anything published externally ends with the Brand Operator confirming consistency (brand name, entity name, contact details)
4. The Competitor Analyst produces all review metrics, so no two roles compute the same number differently
5. One task has one owning role. Collaborating roles provide input; they don't edit the same artifact in parallel.
