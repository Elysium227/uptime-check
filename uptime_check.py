#!/usr/bin/env python3
"""Simple host and service checker.

Reads targets from a JSON file, tests TCP connectivity,
appends the results to a CSV log, and prints a short summary.
Exits with code 1 if any target is down, so it can be used in cron or CI.
"""

import argparse
import csv
import json
import socket
import time
from datetime import datetime
from pathlib import Path

HEADER = ["timestamp", "name", "host", "port", "status", "latency_ms"]


def check(host, port, timeout):
    """Try a TCP connection. Returns (status, latency in ms or None)."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "UP", round((time.perf_counter() - start) * 1000, 1)
    except OSError:
        return "DOWN", None


def main():
    parser = argparse.ArgumentParser(description="Check TCP reachability of hosts.")
    parser.add_argument("-c", "--config", default="hosts.json", help="targets file")
    parser.add_argument("-l", "--log", default="results.csv", help="CSV log file")
    parser.add_argument("-t", "--timeout", type=float, default=3.0, help="seconds")
    args = parser.parse_args()

    targets = json.loads(Path(args.config).read_text())
    now = datetime.now().isoformat(timespec="seconds")
    rows = []

    for t in targets:
        name = t.get("name", t["host"])
        status, ms = check(t["host"], t["port"], args.timeout)
        rows.append([now, name, t["host"], t["port"], status, "" if ms is None else ms])
        latency = "-" if ms is None else f"{ms} ms"
        print(f"{name:<20} {t['host']}:{t['port']:<6} {status:<5} {latency}")

    log = Path(args.log)
    is_new = not log.exists()
    with log.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(HEADER)
        writer.writerows(rows)

    down = sum(1 for r in rows if r[4] == "DOWN")
    print(f"\n{len(rows) - down}/{len(rows)} up")
    return 1 if down else 0


if __name__ == "__main__":
    raise SystemExit(main())
