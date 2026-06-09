import asyncio
import sqlite3
import sys
import time
from pathlib import Path

import goodwe
from gridnet import GridNet

INVERTER_IP = "192.168.68.110"
METER_IP = "192.168.68.101"
DB_PATH = Path(__file__).parent / "solarpanel.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS readings (
    ts INTEGER PRIMARY KEY,
    pv_w INTEGER,
    grid_w INTEGER,
    pv_total_kwh REAL,
    grid_imp_kwh REAL,
    grid_exp_kwh REAL
);
CREATE INDEX IF NOT EXISTS idx_ts ON readings(ts);
"""


async def read_inverter(ip: str):
    try:
        inverter = await goodwe.connect(ip)
        data = await inverter.read_runtime_data()
        pv_w = data.get("total_inverter_power")
        e_total = data.get("e_total")
        return (
            int(pv_w) if pv_w is not None else None,
            float(e_total) if e_total is not None else None,
        )
    except Exception as e:
        print(f"inverter read failed: {e}", file=sys.stderr)
        return None, None


async def read_meter(ip: str):
    try:
        async with GridNet(host=ip) as client:
            sb = await client.smartbridge()
            return (
                int(sb.power_flow),
                float(sb.energy_consumption_total),
                float(sb.energy_production_total),
            )
    except Exception as e:
        print(f"meter read failed: {e}", file=sys.stderr)
        return None, None, None


async def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    try:
        ts = int(time.time())
        inverter_result, meter_result = await asyncio.gather(
            read_inverter(INVERTER_IP),
            read_meter(METER_IP),
        )
        pv_w, pv_total = inverter_result
        grid_w, grid_imp, grid_exp = meter_result

        conn.execute(
            "INSERT OR REPLACE INTO readings "
            "(ts, pv_w, grid_w, pv_total_kwh, grid_imp_kwh, grid_exp_kwh) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (ts, pv_w, grid_w, pv_total, grid_imp, grid_exp),
        )
        conn.commit()
        print(
            f"{ts} pv_w={pv_w} grid_w={grid_w} "
            f"pv_total={pv_total} grid_imp={grid_imp} grid_exp={grid_exp}",
            flush=True,
        )
    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(main())
