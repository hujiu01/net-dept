# Automation Checklist

Automation does exactly one thing: **it drives the cost of noticing a problem to near zero**. It does not make judgements for you.

The test for whether something should be automated is one sentence: **same action, repeated, fixed criteria** — automate it.
Repeated but requiring judgement each time — make it semi-automatic: the script produces data, a person draws the conclusion.

## 1. What to automate (ranked by return)

### Must-do: things that break quietly and probably aren't set up yet

| Automation | Frequency | If you skip it | How |
|---|---|---|---|
| **Uptime monitoring** | hourly | Site down for days, rankings follow | `scripts/site_check.py` |
| **Cron heartbeat** | daily | Scheduled jobs fail silently; discovered weeks later when there's no output | `scripts/heartbeat.py` |
| **SSL expiry monitoring** | daily | Browser warning on expiry day; visitors leave immediately | included in `site_check.py` |
| **Backups** | daily | No rollback point when it matters | cron + object storage |
| **Backup restore verification** | monthly | Backup files exist but won't restore — which means no backup | restore to staging quarterly |

The first three are covered by the scripts here. No third-party service needed.

### Worth doing: saves time, stabilises cadence

| Automation | Frequency | Why | How |
|---|---|---|---|
| **Dead link scanning** | weekly | Silent ranking drag, impossible to check by hand | `scripts/link_check.py` |
| **Daily report scaffolding** | daily | Saves 20 minutes of table filling | script + `assets/daily-report.md` |
| **Index submission** | daily or per publish | Enters the queue days earlier | webmaster API |
| **Sitemap regeneration and submission** | per publish | New pages don't get missed | CMS plugin or build step |
| **Scheduled publishing** | per calendar | Stable cadence without relying on memory | platform API or queue |
| **Competitor page monitoring** | daily | Catch price changes and new products immediately | fetch + diff |

### Optional: valuable but conditional

| Automation | Prerequisite |
|---|---|
| Bulk keyword rank tracking | Official export, or a paid API (watch rate limits and ToS) |
| hreflang validation | Multi-language sites only |
| Image compression and format conversion | Only worth it at volume |
| Duplicate content detection | Only needed across multiple sites |

## 2. What should not be automated (this section matters more)

| Don't automate | Why |
|---|---|
| **Topic selection** | Requires knowing what customers actually ask. A machine can count keywords; it can't tell which line makes someone stop scrolling |
| **Attribution** | "Dropped 30%" depends on seasonality, competitor moves, platform rule changes, and your own changes. A script finds the anomaly; it can't explain it |
| **Redesign decisions** | Involves trade-offs, and trade-offs involve allocating resources — that's a person's call |
| **Customer scripts** | Every customer's context, budget, and decision chain differ |
| **Compliance judgement** | Platform rules change; what was fine last month isn't this month |
| **Killing a channel** | Sunk cost is a psychological problem, not a technical one |

**Why this section matters more**: a system that only alerts and never judges gets ignored within two weeks. Alert fatigue is more dangerous than no alerts — because you'll believe you have a safety net that was quietly switched off.

## 3. Three implementation rules

1. **Every automation must alert.** A script that runs without reporting is not there. The alert can be as simple as a non-zero exit plus an email.
2. **Alerts must be actionable.** "Job failed" should tell you where to look next. Put the log path and the troubleshooting order in the alert body.
3. **Set thresholds loose, not tight.** Start strict and the false positives will get the whole pipeline switched off. Loosen first, tighten later.

## 4. Wiring it up

### Site list

`sites.txt`, one URL per line, `#` for comments:

```
https://example.com
https://example.org
```

### Site health

```bash
python3 scripts/site_check.py --file sites.txt
```

Outputs one table: status code, latency, SSL days remaining, robots, sitemap. Exits 1 on problems.

### Dead links

```bash
python3 scripts/link_check.py --sitemap https://example.com/sitemap.xml --limit 500
```

Pulls URLs from the sitemap (recursing one level into sitemapindex), checks them concurrently, lists dead and slow pages.

### Heartbeats

At the **successful end** of every scheduled job, add one line:

```bash
python3 scripts/heartbeat.py beat --dir /var/hb --name daily-push
```

Then a single daily job checks them all:

```bash
python3 scripts/heartbeat.py check --dir /var/hb --max-age 26
```

Overdue jobs exit 1 and are listed. For jobs on different cadences, set per-job thresholds:

```bash
python3 scripts/heartbeat.py check --dir /var/hb --expect daily-push=26 --expect backup=50
```

### crontab

```bash
# hourly site health
0 * * * * cd /opt/net-dept && python3 scripts/site_check.py --file sites.txt >> /var/log/site-health.log 2>&1 || echo "site down, see /var/log/site-health.log" | mail -s "site alert" you@example.com

# daily 09:00 heartbeat check
0 9 * * * cd /opt/net-dept && python3 scripts/heartbeat.py check --dir /var/hb >> /var/log/hb.log 2>&1 || echo "job overdue, see /var/log/hb.log" | mail -s "job alert" you@example.com

# weekly dead link scan, Monday 03:00
0 3 * * 1 cd /opt/net-dept && python3 scripts/link_check.py --sitemap https://example.com/sitemap.xml >> /var/log/links.log 2>&1
```

The `||` is the whole point: the second half only fires when the script exits non-zero. A cron line without `||` means "it ran", not "it's monitored".

## 5. Traps you will hit

- **Timezone**: overseas servers default to UTC. Either put `TZ=Asia/Shanghai` (or your zone) at the top of the crontab, or convert manually. Log everything in UTC so you don't miscalculate when reading logs.
- **PATH**: cron's environment is minimal; `python3` may not resolve. Use absolute paths, or set the interpreter path in the shebang.
- **Working directory**: cron doesn't inherit yours. Put the `cd` in the command.
- **Overlap**: a job that runs longer than its interval stacks up. Use a lock file, or lengthen the interval.
- **Log growth**: unrotated logs fill the disk in six months and then every job dies at once. Use logrotate.
- **Dependency drift**: an upstream API change causes silent failure — which is exactly why the heartbeat is mandatory. It catches "ran but produced nothing".

## 6. If you have nothing yet, start with these three

1. **Site health** (hourly) — covers uptime and SSL expiry in one script
2. **Job heartbeat** (daily) — covers silent failure across every existing cron
3. **Index submission** (daily) — directly improves indexing speed

With those three in place, most "we found out too late" incidents go away. Returns diminish after that; add more as needed.
