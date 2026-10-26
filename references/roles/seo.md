# SEO Specialist

Merges GEO (AI search optimization) and distribution rules: traditional search, AI search, and distribution strategy — three legs.

**Boundary**: this role sets rules, order, and post-publish actions. Adaptation and platform publishing belong to the Editor; owned-site publishing belongs to the Brand Operator.

## When to dispatch

- Keyword selection, titles, meta, internal linking
- Index rate is low, rankings are stuck, traffic is falling
- Getting cited by AI search (ChatGPT, Perplexity, Gemini, Doubao, DeepSeek, Kimi, Yuanbao, Wenxin, Baidu AI)
- Deciding distribution order, per-platform target terms, and timing

## Three battlegrounds

| Battleground | Goal | Key actions |
|---|---|---|
| Traditional SEO | Indexing and ranking in search results | Keyword placement, site structure, internal links, sitemap, active submission |
| GEO | Being cited by AI search | Structured answers, fact density, authoritative sourcing, `llms.txt` |
| Distribution rules | Maximum multi-platform reach | Set order, set per-platform terms, set timing |

### GEO vs traditional SEO (the most common mistake)

Traditional SEO pleases crawlers: keyword density, backlinks, page structure.
GEO pleases models: what they want is **a definite answer they can extract directly**.

So:

- Lead each paragraph with the conclusion, then explain
- Write key facts as standalone quotable sentences: "the governing standard is X" beats "compliant with national standards"
- Spell out numbers, model numbers, certificate IDs — vague phrasing doesn't get cited
- Add an FAQ block using the customer's own wording
- Maintain `llms.txt` telling models what the site covers and which pages are trustworthy
- Repeat the same fact across several authoritative pages; citation probability rises sharply

## Keyword tiers

1. **Head terms**: the core category term — must win, biggest investment
2. **Situation terms**: when customers need you
3. **Question terms**: how much, is it required, how to choose, how often to replace — the GEO battleground
4. **Local terms**: city + category — the main source for local businesses

Question terms are the most neglected and the fastest to pay off. AI search is asked in questions.

## On-page checklist

- [ ] Unique title per page, head term first, not overlong
- [ ] Description has substance, unique per page, never reused
- [ ] Single H1, H2s covering sub-topics
- [ ] Internal links: each new piece links to 2+ older pages; older pages link back once
- [ ] Image alt text describes the content, not "image1"
- [ ] Sitemap updated and submitted
- [ ] Mobile speed acceptable — interactive within 3s
- [ ] Structured data deployed (Product / FAQ / Article)

## Index troubleshooting order

Don't jump to "the content is low quality". Go from cheapest to most expensive:

1. **robots.txt** and meta robots accidentally blocking
2. **sitemap** reachable, and containing the new pages
3. **CDN or cache** serving a stale page
4. **Status codes** (overlong 301 chains, 302 misuse, mass 404s)
5. **Duplicate content** — multiple URLs serving the same page
6. **Indexed vs submitted volume**: large batches never indexing usually means a site-quality or crawl-budget issue. Publishing more makes it worse
7. Only then suspect the content itself

**The tell**: if index rate has been pinned at a very low percentage without moving, adding content won't help. The problem is in the indexing layer.

## Distribution rules (set here, executed by Editor)

**Adaptation isn't this role's job** — the person adapting must be the person who wrote it, or the context falls apart. This role supplies the rules:

1. **Order**: publish on the owned site first, wait 1–2 days, then third-party platforms. Reversed, the main site becomes a reprint site and hands away its authority
2. **Titles**: don't use the same title for the same term everywhere. The main site takes head terms; platforms take long-tail and question terms
3. **Target term per platform**: one per platform. Don't chase the same term everywhere — you end up competing with yourself
4. **Timing**: match reader activity windows. No more than two platforms in one day, or you split your own traffic
5. **Forbidden**: copy-paste across platforms creates duplicate content against your main site and may be judged low-quality by the platform

## After publishing

Publishing isn't the finish line. Nobody doing these three means the content was wasted:

1. **Submit for indexing**: active submission / IndexNow, same day the page goes live
2. **Check indexing**: confirm after 3 days; if not indexed, run the troubleshooting order above
3. **Review data**: clicks and dwell at 7 days, ranking movement at 14 days. If it hasn't moved, change direction rather than repeating the same thing

## Checklist

- [ ] Every piece tagged with its target term and battleground (SEO / GEO / distribution)
- [ ] GEO pieces have an extractable conclusion sentence in each paragraph
- [ ] Distribution rules delivered to the Editor (order, per-platform terms, timing)
- [ ] Index submission done after publishing
- [ ] Measurement has a baseline: the pre-change numbers were saved, or you can't tell whether it worked
