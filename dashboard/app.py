import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = Path(__file__).parent / "solarpanel.db"

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
    pv = row["pv_w"]
    grid = row["grid_w"]
    consumption = (pv + grid) if pv is not None and grid is not None else None
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
                AVG(pv_w)   AS pv_w,
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
