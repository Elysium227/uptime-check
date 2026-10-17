# uptime-check

A small Python script that checks whether hosts and services are reachable over TCP, logs the results to a CSV file, and exits with an error code if anything is down.

No dependencies, just Python 3.8+.

## Usage

```bash
python3 uptime_check.py
```

Options:

| Flag | Default | What it does |
|------|---------|--------------|
| `-c`, `--config` | `hosts.json` | File listing the targets |
| `-l`, `--log` | `results.csv` | CSV file results are appended to |
| `-t`, `--timeout` | `3.0` | Seconds to wait per connection |

Example output:

```
GitHub               github.com:443    UP    41.3 ms
Cloudflare DNS       1.1.1.1:53        UP    18.7 ms
Example web          example.com:443   UP    62.9 ms

3/3 up
```

## Adding targets

Edit `hosts.json`:

```json
[
  {"name": "My server", "host": "192.168.1.10", "port": 22}
]
```

## Running it on a schedule

Check every 5 minutes with cron:

```
*/5 * * * * cd /path/to/uptime-check && python3 uptime_check.py >> cron.log 2>&1
```

Since the script returns exit code 1 when a target is down, you can also chain it with an alert command:

```bash
python3 uptime_check.py || echo "Something is down" | mail -s "Alert" you@example.com
```
