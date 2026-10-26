# Net Dept · a marketing department in a skill

A whole online-acquisition department, packaged as a skill. One lead plus five specialist roles — each with its own boundaries, methods, delivery templates, and checklists. Works for any industry.

Once installed, you stop re-explaining your process every time. Say "what should we do this month", "analyse the competitors", "write something for Zhihu", or "the client says it's too expensive" — it routes to the right role and delivers to a fixed standard.

## Why this shape

The execution layer follows the acquisition chain, not a job-title chart:

```
See the market     Make content     Get found      Earn trust     Close
Competitor    →    Editor      →    SEO       →    Brand     →    Conversion
```

Break any link and everything upstream is wasted:

| Missing | What it looks like |
|---|---|
| Competitor | Content direction is guesswork; six months in, nobody knows what rivals are doing |
| Editor | Strategy with no output; endless topic meetings |
| SEO | Lots of writing, nobody reads it |
| Brand | Traffic but no inquiries; prospects don't trust you |
| Conversion | Inquiries but no closes; leads rot in the inbox |
| **Lead** | All five are busy, direction is scattered, nobody dares kill anything |

That last one is the hardest to spot. A missing execution role is obvious — no articles, no traffic, nobody answering. A missing lead looks like "we're all working hard and the quarter produced nothing", which is very hard to attribute to any one person.

So above the five execution roles sits a decision layer:

```
                     Department Lead
              one target · kill dead initiatives
                          │
    ┌──────────┬──────────┼──────────┬──────────┐
 Competitor  Editor      SEO      Brand    Conversion
```

Small teams wearing many hats is normal — but the boundaries still matter. Blending them typically produces a bit of everything and nothing that actually brings in customers.

## The team

| Role | Owns | Core output |
|---|---|---|
| **Department Lead** | Direction, task breakdown, standards, reviews, tie-breaks | Target, role task table, decision log |
| **Competitor Analyst** | External intelligence + internal data review + daily reporting | Comparison matrix, daily report, intel brief |
| **Content Editor** | Copy, visuals, covers, video scripts, platform publishing | Published pieces and live URLs |
| **SEO Specialist** | Search, AI search (GEO), distribution rules | Keyword map, meta, index growth |
| **Brand & Site Operator** | Site, encyclopedia/PR presence, servers, automation | Site health, brand footprint |
| **Customer Conversion** | Inquiry handling, quoting, objections, follow-up | Reply scripts, quotes, follow-up log |

Each role card covers: when to dispatch it, what it does, what it explicitly does not do, its process, output format, checklist, and common failure modes.

## Install

```bash
git clone https://github.com/hujiu01/net-dept.git
cp -r net-dept ~/.workbuddy/skills/
```

For other clients that support skills, drop the directory into the corresponding skills path. The layout follows the conventional `SKILL.md` + `references/` + `assets/` structure.

## First run

On first trigger it asks six questions:

1. Brand name and legal entity name
2. What you sell
3. Core acquisition keywords
4. Pricing stance
5. Primary sites and content channels
6. Industry compliance red lines

Answers go into `references/profile.local.md` (gitignored). Every role reads facts from there.

**Or fill it in by hand.** Copy `references/profile.md` to `references/profile.local.md` and fill in the fields. The more precise the profile, the better the output.

## Examples

```
What should we do this month?
Put together yesterday's data report
Review last week — what should we stop doing?
What are the competitors up to?
Write a piece about <your core scenario> for Zhihu
Our index rate is stuck. How do I diagnose it?
What should we watch out for in a site redesign?
The client says it's too expensive. How do I reply?
```

## Automation

`scripts/` has three zero-dependency scripts — Python standard library only, no `pip install`:

```bash
# Site health: status code, response time, SSL days left, robots, sitemap
python3 scripts/site_check.py --file sites.txt

# Dead link scan: pulls URLs from sitemap, handles sitemapindex
python3 scripts/link_check.py --sitemap https://example.com/sitemap.xml

# Cron heartbeat: solves silent failures
python3 scripts/heartbeat.py beat --dir /var/hb --name daily-push
python3 scripts/heartbeat.py check --dir /var/hb --max-age 26
```

All three exit non-zero on problems, so `||` wiring gives you alerting:

```bash
0 * * * * cd /opt/net-dept && python3 scripts/site_check.py --file sites.txt >> /var/log/site.log 2>&1 || echo "site down" | mail -s "alert" you@example.com
```

`references/automation.md` ranks twelve automations by what breaks if you skip them, and includes a section on **what should not be automated** — topic selection, attribution, redesign decisions, compliance judgement. Handing those to a machine produces output that looks like work and isn't. Also there: cron examples and six traps (timezone, PATH, working directory, overlap, log growth, dependency drift).

## Layout

```
net-dept/
├── SKILL.md                    role routing + operating rules + bottom line
├── README.md
├── LICENSE
├── .gitignore
├── references/
│   ├── profile.md              business profile template (committed)
│   ├── profile.local.md        your real profile (not committed)
│   ├── workflow.md             5 chains + the daily loop
│   ├── metrics.md              metric definitions (so the same number means the same thing)
│   ├── automation.md           what to automate, what not to
│   └── roles/
│       ├── lead.md             decision layer
│       ├── competitor.md       includes daily data reporting
│       ├── editor.md
│       ├── seo.md
│       ├── brand.md
│       └── service.md
├── assets/
│   ├── competitor-matrix.md    comparison matrix
│   ├── daily-report.md         daily data report
│   ├── publish-checklist.md    pre/post publish checks
│   └── weekly-report.md        weekly report
└── scripts/
    ├── site_check.py           status / latency / SSL / sitemap
    ├── link_check.py           dead link scan
    └── heartbeat.py            cron heartbeat
```

## Design notes

**Why one role card at a time.** `SKILL.md` is a 4KB routing table. Say "analyse the competitors" and only `competitor.md` loads — the other five never enter context. Stuffing six roles into the main file burns a large amount of context on every trigger and degrades complex work.

**Why `profile.md` exists.** General method and specific facts have to be separated. Method can be open-sourced; company names, pricing, certificate IDs cannot. The profile is the interface between them.

**Why the Lead is its own layer.** Execution roles will always say "give me more resources", never "kill this line". The Lead's value isn't managing people — it's doing the two things execution roles structurally cannot: pick one target, and stop dead work.

**Why metric definitions get their own file.** The main failure mode in data work isn't failing to collect numbers — it's computing the same metric differently each time. Change the denominator of "index rate" from page count to sitemap count and the trend line breaks, usually without anyone noticing.

**Why the cards include traps.** Generic SEO advice is everywhere. What's scarce is "clear the cache before verifying or you'll misjudge it as broken" or "cron on overseas servers defaults to UTC and your tasks fire hours off". The value is in the detail, not the framework.

## Going finer-grained

The five execution roles are a skeleton. Common splits:

- **Visual designer** out of Editor
- **Short video producer** out of Editor
- **GEO specialist** out of SEO
- **Paid media buyer** as its own role
- **Lifecycle / CRM** out of Conversion
- **Link building / PR** out of Brand

To add one: create a card in `references/roles/` and add a row to the routing table in `SKILL.md`. Write the description around "when to dispatch it" — otherwise it will never trigger.

**Don't split the Lead layer.** Two decision-makers means no decision-maker.

## Customising

You can edit any file without breaking the structure, as long as:

1. `SKILL.md` frontmatter has `name` and `description`
2. `description` states what it does and when to use it — that's what drives triggering
3. Every path in the routing table actually exists

## License

MIT. Use it, ship it commercially, change it without telling anyone.

---

Maintenance note: `references/profile.local.md` is in `.gitignore`. Check `git status` before committing — don't push your company's price list to a public repo.
