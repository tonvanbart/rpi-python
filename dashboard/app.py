import os
import signal
import sqlite3
import subprocess
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = Path(__file__).parent / "solarpanel.db"

# fireplace.py needs sense_hat, which is installed system-wide, not in our venv
FIREPLACE_PYTHON = "/usr/bin/python3"
FIREPLACE_SCRIPT = Path("/home/iot/projects/tonvanbart/rpi-fireplace/fireplace.py")
FIREPLACE_LOG = Path(__file__).parent / "fireplace.log"
# matches our own launch as well as a manual `python3 fireplace.py`
FIREPLACE_PATTERN = r"python3? .*fireplace\.py$"

fireplace_lock = threading.Lock()
fireplace_proc = None

RANGES = {
    "1h":  (3600,    60),
    "6h":  (21600,   300),
    "24h": (86400,   600),
    "7d":  (604800,  3600),
    "30d": (2592000, 14400),
}


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/latest")
def latest():
    with get_conn() as conn:
        row = conn.execute(
            "SELECT ts, pv_w, grid_w FROM readings ORDER BY ts DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return jsonify({"error": "no data yet"}), 404
    # inverter offline (low light) means it produces nothing
    pv = row["pv_w"] if row["pv_w"] is not None else 0
    grid = row["grid_w"]
    consumption = (pv + grid) if grid is not None else None
    return jsonify({
        "ts": row["ts"],
        "pv_w": pv,
        "grid_w": grid,
        "consumption_w": consumption,
    })


@app.route("/api/series")
def series():
    range_key = request.args.get("range", "1h")
    if range_key not in RANGES:
        return jsonify({"error": "invalid range"}), 400
    window, bucket = RANGES[range_key]
    with get_conn() as conn:
        max_ts_row = conn.execute("SELECT MAX(ts) AS m FROM readings").fetchone()
        max_ts = max_ts_row["m"] or 0
        min_ts = max_ts - window
        rows = conn.execute(
            f"""
            SELECT
                (ts / {bucket}) * {bucket} AS bucket,
                AVG(COALESCE(pv_w, 0)) AS pv_w,  -- NULL = inverter offline = 0 W
                AVG(grid_w) AS grid_w
            FROM readings
            WHERE ts >= ?
            GROUP BY bucket
            ORDER BY bucket
            """,
            (min_ts,),
        ).fetchall()
    return jsonify([
        {
            "ts": r["bucket"],
            "pv_w": round(r["pv_w"]) if r["pv_w"] is not None else None,
            "grid_w": round(r["grid_w"]) if r["grid_w"] is not None else None,
            "consumption_w": (
                round(r["pv_w"] + r["grid_w"])
                if r["pv_w"] is not None and r["grid_w"] is not None
                else None
            ),
        }
        for r in rows
    ])


def fireplace_pids() -> list[int]:
    # reap our own child first, so a stopped fireplace doesn't linger as a zombie
    if fireplace_proc is not None:
        fireplace_proc.poll()
    out = subprocess.run(
        ["pgrep", "-f", FIREPLACE_PATTERN], capture_output=True, text=True
    )
    return [int(pid) for pid in out.stdout.split()]


@app.route("/api/fireplace")
def fireplace_status():
    return jsonify({"running": bool(fireplace_pids())})


@app.route("/api/fireplace", methods=["POST"])
def fireplace_switch():
    global fireplace_proc
    on = bool((request.get_json(silent=True) or {}).get("on"))
    with fireplace_lock:
        pids = fireplace_pids()
        if on and not pids:
            with open(FIREPLACE_LOG, "a") as log:
                fireplace_proc = subprocess.Popen(
                    [FIREPLACE_PYTHON, str(FIREPLACE_SCRIPT)],
                    cwd=FIREPLACE_SCRIPT.parent,
                    stdout=log,
                    stderr=log,
                )
        elif not on:
            # SIGTERM lets fireplace.py clear the LEDs before exiting
            for pid in pids:
                os.kill(pid, signal.SIGTERM)
            if fireplace_proc is not None:
                try:
                    fireplace_proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass
        return jsonify({"running": bool(fireplace_pids())})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
