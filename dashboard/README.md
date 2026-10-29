# Solar Dashboard

A small web dashboard for live and historical solar production, household consumption, and grid import/export. Reads two devices on the LAN, writes to SQLite, serves a Flask web UI.

LAN-only by design. No cloud, no external dependencies beyond Chart.js loaded from a CDN.

## What it shows

- **Live tiles**: current PV production, current house consumption, current grid flow (with sign and direction). Auto-refresh every 60 s.
- **Time series chart**: PV production, house consumption, grid flow over a selectable range (1h / 6h / 24h / 7d / 30d). Server-side bucketing keeps every range view ~150–300 points so the chart stays snappy even at 30 days.

## Architecture

```
[Goodwe inverter]  192.168.68.110  (local protocol)
                        │
                        ▼
                  ┌──────────┐         ┌──────────┐
                  │ logger.py│────────▶│ SQLite   │
                  │ (cron)   │         │  .db     │
                  └──────────┘         └────┬─────┘
                        ▲                   │
                        │                   ▼
[Net2Grid SmartBridge]  │              ┌──────────┐
192.168.68.101  ────────┘              │  app.py  │ :5000
(local HTTP)                           │  (Flask) │
                                       └──────────┘
                                            ▲
                                            │
                                       browser on LAN
```

- `logger.py` is invoked by **cron every minute**, polls inverter + meter concurrently, inserts one row into `solarpanel.db`, exits.
- `app.py` runs **continuously under systemd**, reads from the same DB, serves the UI.
- The DB is the only shared state. Either side can fail or restart independently.

## File layout

```
dashboard/
├── README.md                        # this file
├── logger.py                        # cron-invoked poller
├── app.py                           # Flask web server
├── solarpanel.db                    # SQLite (created on first run; not in git)
├── logger.log                       # cron stdout/stderr (created on first run)
├── app.log                          # Flask stdout/stderr (created by systemd)
├── templates/
│   └── index.html                   # single-page UI; Chart.js from CDN
├── deploy/
│   └── solar-dashboard.service      # systemd unit for app.py
└── venv/                            # Python deps (not in git, not rsync'd)
```

## Schema

Single table, one row per minute:

| Column | Type | Notes |
|---|---|---|
| `ts` | INTEGER PRIMARY KEY | UTC epoch seconds |
| `pv_w` | INTEGER | PV production (W); NULL if inverter unreachable (e.g., night) |
| `grid_w` | INTEGER | Grid flow (W); negative = export, positive = import; NULL if meter unreachable |
| `pv_total_kwh` | REAL | Lifetime PV production (kWh), 0.1 kWh resolution |
| `grid_imp_kwh` | REAL | Lifetime grid import (kWh), 0.1 kWh resolution |
| `grid_exp_kwh` | REAL | Lifetime grid export (kWh), 0.1 kWh resolution |

House consumption is **derived** as `pv_w + grid_w` at query time (with `NULL` `pv_w` counted as 0). Not stored.

## Deployment

One-time setup on the Pi.

### 1. Dependencies

```bash
cd ~/projects/rpi-python/dashboard
python3 -m venv venv
. venv/bin/activate
pip install goodwe gridnet flask
```

### 2. Cron entry for the logger

```bash
crontab -e
```
Add:
```
* * * * * /usr/bin/flock -n /tmp/solar-logger.lock /home/iot/projects/rpi-python/dashboard/venv/bin/python /home/iot/projects/rpi-python/dashboard/logger.py >> /home/iot/projects/rpi-python/dashboard/logger.log 2>&1
```
`flock -n` prevents overlapping runs if a poll ever takes longer than 60 s.

### 3. systemd service for the Flask app

```bash
sudo cp deploy/solar-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now solar-dashboard
```
Verify:
```bash
sudo systemctl status solar-dashboard
```

The dashboard is then reachable at `http://r2pi3.local:5000` from any device on the Deco LAN.

## Common operations

### Inspect recent readings
```bash
sqlite3 solarpanel.db "SELECT datetime(ts, 'unixepoch', 'localtime') AS t, pv_w, grid_w FROM readings ORDER BY ts DESC LIMIT 10;"
```

### Tail the cron log
```bash
tail -f logger.log
```

### Tail the app log
```bash
tail -f app.log
```
Or via journald:
```bash
journalctl -u solar-dashboard -f
```

### Restart the dashboard (after editing `app.py`)
```bash
sudo systemctl restart solar-dashboard
```
(Template-only changes don't need a restart — `TEMPLATES_AUTO_RELOAD` is on. Python changes do.)

### Update from laptop
From the laptop project root:
```bash
rsync -avz --exclude venv \
    ~/Projects/tonvanbart/solarpanel-data/dashboard/ \
    r2pi3:~/projects/rpi-python/dashboard/
```
Then restart the service if `app.py` changed.

## Things to remember (the gotchas)

- **Device IPs are pinned via DHCP reservation in the Deco.** Inverter `HF-LPT230` at `192.168.68.110`, SmartBridge `smartbridge-3e12` at `192.168.68.101`. If reservations are ever removed, scripts will break and the IPs must be re-pinned (or `logger.py` updated).
- **The inverter is offline at night.** Its wifi dongle is powered by the inverter itself; when PV drops below the startup threshold after sunset, both shut down. `logger.py` handles this gracefully — writes `NULL` for `pv_w` / `pv_total_kwh` and keeps going with the meter. `app.py` treats a `NULL` `pv_w` as 0 W, so at night PV shows 0 and consumption equals grid import. (A daytime inverter read failure is also shown as 0 W.)
- **Lifetime totals tick at 0.1 kWh resolution.** A few minutes of low production won't visibly bump them. Trust instantaneous values for "right now"; use the cumulative columns for daily/weekly totals via diffing.
- **House consumption is derived, not measured.** It's `pv_w + grid_w`. The inverter has no smart meter wired into it on this install, so its built-in `house_consumption` field is unreliable — don't trust it. The SmartBridge is the source of truth for grid flow.
- **The Net2Grid library exposes electricity only.** No gas, no per-tariff split. If those become needed, would require either bypassing the library to hit raw HTTP endpoints, or replacing the SmartBridge with a HomeWizard P1 Meter.
- **No DB backup.** A corrupted SD card loses all historical data. If the data ever becomes load-bearing, set up an rsync to the laptop or a remote backup target.
- **Pi 3B constraints**: 1 GB RAM, SD card I/O. This stack is comfortable here. Don't try to add Home Assistant or anything memory-heavy to the same host — it will thrash.
- **CDN dependency for Chart.js.** The dashboard works fully on LAN, but the *first load* needs internet to fetch Chart.js + the date adapter. If you ever need true offline use, download both scripts into `static/` and reference them locally.
- **Flask's port 5000 is unauthenticated.** Anyone on the LAN can read it. Fine for a home network; not safe to expose publicly. Don't port-forward this without adding auth and TLS.
- **Cron uses `flock` to prevent overlap.** If you ever see no new rows appearing, check `/tmp/solar-logger.lock` isn't stuck (rare but possible after an ungraceful kill).
- **Template auto-reload is on, code reload is not.** HTML edits show up on refresh; Python edits require `systemctl restart solar-dashboard`.

## Limitations

- **Polling cadence is 1 minute** (cron minimum). Faster cadence would require switching back to a daemon model with internal sleep loop.
- **Historical aggregation is naïve.** `/api/series` uses simple `AVG()` per bucket. For very long ranges (years) a pre-aggregated daily-summary table would be faster.
- **No alerting.** No notification when the inverter or meter goes silent for an extended period.
- **No multi-day comparison view.** Could add (e.g., "today vs same weekday last week") but not currently.

## Related project notes

Living documentation about the broader solarpanel-data tinkering — device identification, network topology, data-access path comparisons (cloud / inverter local / meter local), unit conventions, the Sense Hat visualization plans, and the Pi wifi-stability fixes — lives in Claude Code's project memory under `~/.claude/projects/-home-ton-Projects-tonvanbart-solarpanel-data/memory/`.
