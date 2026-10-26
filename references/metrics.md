# Metric Definitions

The biggest killer in data work isn't failing to collect numbers — it's **computing the same metric differently each time**. This file fixes the definitions so everyone gets the same answer.

## 1. Traffic

| Metric | Definition | Where people get it wrong |
|---|---|---|
| **Users (UV)** | Deduplicated visitors in the period | Same person switching device or clearing cookies counts twice; dedup logic differs between tools |
| **Pageviews (PV)** | Total page opens | Refreshes count twice; a double-installed tracking tag inflates PV absurdly |
| **Unique IPs** | Deduplicated source IPs | Office and campus networks share one egress IP — badly undercounts |
| **New visitor share** | First-time visitors ÷ total visitors | Naturally low for repeat-purchase businesses; that's not a problem |
| **Avg. session duration** | Total time ÷ sessions | Single-page bounces usually record as 0s and drag the average down |
| **Bounce rate** | Sessions leaving after one page | High bounce is normal for content pages — don't treat it as a fault |

**Which to use**: UV for reporting and trends, duration and bounce for judging content appeal. Never use PV as a proxy for people.

## 2. Indexing

| Metric | Definition |
|---|---|
| Indexed pages | Pages a search engine has added to its index |
| Submitted pages | URLs pushed via sitemap or active submission |
| Index rate | Indexed ÷ submitted |
| Indexing lag | Days from publication to being indexed |

**Always state** which search engine and when you checked. Baidu and Google numbers are not comparable.

**Indexing lag is normal.** New pages taking 3–7 days to index is within range. Concluding "not indexed" the day after publishing is a misdiagnosis.

**Over 7 days** is when you investigate — sequence in `references/roles/seo.md`.

**The denominator matters**: if you can't get the true page count, estimate from sitemap entries and **label it as an estimate**. This is the number most often inflated in reporting.

## 3. Keywords

| Metric | Definition | Note |
|---|---|---|
| Impressions | Times a page appeared in results | Third-party tools diverge wildly from official consoles — **use official data only** |
| Clicks | Clicks from search results | — |
| CTR | Clicks ÷ impressions | High impressions + low CTR = title problem. High CTR + low impressions = ranking problem |
| Average position | Mean position across keywords | Meaningless — look at **head term positions individually** |
| Keyword coverage | Total keywords with any impressions | More informative about content volume than any single ranking |

**Priority**: head term position > keyword coverage > average position.
Average position is the least useful metric here — averaging a #1 and a #80 gives you 40, which tells you nothing.

## 4. Conversion

| Metric | Definition |
|---|---|
| Inquiries | Valid inbound contacts (deduplicated, spam and competitors excluded) |
| Cost per inquiry | Spend ÷ inquiries |
| Inquiry-to-order rate | Orders ÷ inquiries |
| Average order value | Revenue ÷ orders |

**Define "valid"** or your weekly numbers will never reconcile. Write the definition into the business profile.

## 5. Where to Collect

| Data | Source |
|---|---|
| Index count, impressions, clicks, positions | Search engine webmaster / resource consoles |
| Site traffic | Your own analytics |
| Per-platform reads and reach | Platform creator dashboards |
| Inquiries | CRM or form backend |
| Competitor data | Third-party tools + manual verification |

**Third-party numbers are for relative comparison only, never for external reporting.** Official consoles and third-party tools can differ by a factor of several on impressions — mixing them produces confidently wrong conclusions.

## 6. Consistency (most important)

1. **Don't switch tools mid-stream.** If you do, note the exact date, or the trend line will show an unexplained jump.
2. **Don't switch methodology.** Changing the index-rate denominator from page count to sitemap count is a different metric — recompute history.
3. **Never judge a trend from one day.** Use a 7-day average first; single-day moves are noise.
4. **Treat weekends and holidays separately.** B2B traffic drops naturally on weekends; calling it an anomaly leads to repeated false alarms.
5. **Prefer period-over-period over day-over-day.** Last week vs. the week before beats yesterday vs. the day before.

## 7. Common Misdiagnoses

| Symptom | Don't conclude | Check first |
|---|---|---|
| Traffic spiked | Content went viral | Duplicate tracking tag; bot traffic |
| Traffic dropped | Penalised | Weekend; analytics outage |
| Index count fell | Content deleted | Site redesign changed URLs |
| High impressions, no clicks | Bad title | Also: ranking on page 2 — seen, not clicked |
| High ranking, no traffic | Wrong keyword | Also: the term has almost no volume |
| Inquiries fell | Traffic problem | Also: slow response, broken form |

**Default assumption should be "we got something wrong", not "the platform is out to get us".** That ordering saves a lot of wasted investigation.
