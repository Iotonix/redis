# AIT Redis Tester

> Version 1.0.0

Simple, focused example of performing CRUD (create, read, update, delete) operations against Redis using JSON payloads in Python. It provides:

- `redis_tester.py`: Class wrapper (`AitRedisTester`) around redis-py for connection + JSON key-value operations.
- `statistics.py`: Statistics tracker for monitoring Redis operations.
- `main.py`: Demo script exercising a full lifecycle on an `APP_CONFIG` key with statistics tracking.
- `.env.example`: Sample environment configuration (copy to `.env`).
- `requirements.txt`: Dependencies (`redis`, `python-dotenv`).

## 1. Why Redis Here?

Great for ultra-fast lookups of configuration and session-like objects by key. For relational queries or complex joins, pair Redis with a SQL database (PostgreSQL, etc.). Common pattern: SQL = source of truth, Redis = cache.

## 2. Project Structure

| File               | Purpose                                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------------------- |
| `redis_tester.py`  | Defines `AitRedisTester` class with connect/insert/update/search/delete methods using JSON serialization. |
| `statistics.py`    | Tracks operation counts (insert/update/search/delete) and provides runtime statistics.                   |
| `main.py`          | Demonstrates connecting, inserting, verifying, updating, deleting and re-inserting `APP_CONFIG` with stats tracking. |
| `.env.example`     | Template for Redis connection variables.                                                                  |
| `requirements.txt` | Dependency pins.                                                                                          |

## 3. Prerequisites

* Python 3.9+
* Accessible Redis server (local Docker, managed service, etc.)

## 4. Installation (Windows PowerShell)

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Or quick install without a venv:

```powershell
pip install redis python-dotenv
```

## 5. Configuration

Copy `.env.example` to `.env` and edit:

```
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=
```

Then load automatically via `load_dotenv()` (already in the class) or export manually in your shell.

## 6. Class Overview (`AitRedisTester`)

```python
from redis_tester import AitRedisTester

tester = AitRedisTester()
if tester.connect():
    tester.insert("MY_KEY", {"hello": "world"})
    data = tester.search("MY_KEY")
    tester.update("MY_KEY", {"hello": "redis"})  # same as insert
    tester.delete("MY_KEY")
```

Implementation details:

* Uses `redis.Redis(..., decode_responses=True)` so string values are auto-decoded.
* Dicts are stored as JSON strings via `json.dumps` and reconstructed with `json.loads`.
* `update()` is an alias for `insert()` (Redis SET is upsert).

## 7. Running the Demo

```powershell
python main.py
```

The script will:

1. Connect
2. Insert `APP_CONFIG`
3. Search & pretty-print JSON
4. Verify a field
5. Update a color
6. Re-query
7. Delete and confirm absence
8. Re-insert and confirm again
9. Display statistics summary

## 8. API Summary

| Method              | Parameters          | Returns      | Notes                                                  |
| ------------------- | ------------------- | ------------ | ------------------------------------------------------ |
| `connect()`         | none                | bool         | Connects (or verifies injected client) and pings Redis |
| `insert(key, dict)` | key:str, value:dict | bool         | Upsert JSON                                            |
| `update(key, dict)` | key:str, value:dict | bool         | Alias of insert                                        |
| `search(key)`       | key:str             | dict or None | Returns deserialized JSON                              |
| `delete(key)`       | key:str             | bool         | True if key removed                                    |

## 9. Example Raw redis-py Usage

```python
import redis, json
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.set("TEST_KEY", json.dumps({"hello": "world"}))
print(json.loads(r.get("TEST_KEY")))
```

### Dependency injection for tests

`AitRedisTester` accepts an optional `redis_client` so you can inject a test double (e.g., `fakeredis.FakeRedis`).

```python
import fakeredis
from redis_tester import AitRedisTester

fake = fakeredis.FakeRedis(decode_responses=True)
tester = AitRedisTester(redis_client=fake)
assert tester.connect() is True
```

### Logging

The class uses the `logging` module instead of `print`. Configure logging in your app (see `main.py`).

### Statistics Tracking

The `RedisStatistics` class tracks operation counts and runtime metrics.

**Usage:**

```python
from statistics import RedisStatistics

stats = RedisStatistics()

# Record operations as they happen
stats.record_operation("insert")
stats.record_operation("search")
stats.record_operation("update")
stats.record_operation("delete")

# Get current statistics
current_stats = stats.get_statistics()
print(current_stats)  # {'insert': 1, 'update': 1, 'search': 1, 'delete': 1}

# Get total operation count
total = stats.get_total_operations()
print(total)  # 4

# Print formatted summary
stats.print_summary()
```

**Example output:**

```
2026-01-01 12:00:00,123 INFO statistics: === Redis Operations Summary ===
2026-01-01 12:00:00,123 INFO statistics: Runtime: 2.45 seconds
2026-01-01 12:00:00,123 INFO statistics: Total operations: 7
2026-01-01 12:00:00,123 INFO statistics:   insert: 2
2026-01-01 12:00:00,123 INFO statistics:   update: 1
2026-01-01 12:00:00,123 INFO statistics:   search: 3
2026-01-01 12:00:00,123 INFO statistics:   delete: 1
2026-01-01 12:00:00,123 INFO statistics: ==============================
```

**API:**

| Method                      | Returns           | Description                              |
| --------------------------- | ----------------- | ---------------------------------------- |
| `record_operation(type)`    | None              | Record an operation (insert/update/search/delete) |
| `get_statistics()`          | dict              | Get current operation counts             |
| `get_total_operations()`    | int               | Get total number of operations           |
| `print_summary()`           | None              | Print formatted summary to logs          |

## 10. Running tests

You can run unit tests locally without a real Redis server. Tests use `fakeredis`.

```powershell
# 1) (Optional) activate your virtual environment
./.venv/Scripts/Activate.ps1

# 2) Install dev-only dependencies
pip install -r requirements-dev.txt

# 3) Run the tests
pytest -q
```

Notes:

- Tests inject an in-memory `fakeredis.FakeRedis` via `AitRedisTester(redis_client=...)`.
- No network or external services are required.

## 11. Troubleshooting

| Symptom            | Check                           | Fix                                   |
| ------------------ | ------------------------------- | ------------------------------------- |
| ConnectionError    | Host/port/password              | Correct `.env`, ensure server running |
| Empty search       | Key spelled? TTL expired?       | Re-insert or remove TTL elsewhere     |
| Non-UTF8 bytes     | Missing `decode_responses=True` | Use provided class setup              |
| Wrong host in logs | `.env` not loaded               | Ensure file named `.env` & in root    |

## 12. Using Redis CLI

### Installation

**Windows (via Redis for Windows):**

```powershell
# Download from: https://github.com/tporadowski/redis/releases
# Or use Chocolatey:
choco install redis-64

# Or use Windows Subsystem for Linux (WSL)
```

**macOS:**

```bash
brew install redis
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install redis-tools
```

**Docker (no installation needed):**

```powershell
docker run -it --rm redis redis-cli -h host.docker.internal -p 6379
```

### Basic redis-cli Commands

**Connect to Redis:**

```powershell
# Local connection
redis-cli

# Remote connection
redis-cli -h 127.0.0.1 -p 6379

# With password
redis-cli -h 127.0.0.1 -p 6379 -a yourpassword
```

**Common Operations:**

```bash
# Test connection
PING

# Set a key-value pair
SET mykey "Hello World"

# Get a value
GET mykey

# Set JSON (as string)
SET APP_CONFIG '{"app_name":"AIT-WEB","tenant":"AIT"}'

# Get JSON
GET APP_CONFIG

# Check if key exists
EXISTS mykey

# Delete a key
DEL mykey

# List all keys (careful in production!)
KEYS *

# Get key pattern
KEYS APP_*

# View key type
TYPE mykey

# Set expiration (in seconds)
EXPIRE mykey 3600

# Check time to live
TTL mykey

# View all databases
INFO keyspace

# Switch database (0-15)
SELECT 1

# Clear current database
FLUSHDB

# Clear all databases (DANGEROUS!)
FLUSHALL
```

### Monitoring and Debugging

```bash
# Monitor all commands in real-time
MONITOR

# View server info
INFO

# View connected clients
CLIENT LIST

# View memory usage
MEMORY STATS

# View specific key memory
MEMORY USAGE mykey
```

### Redis Insight (GUI Tool)

**Redis Insight** is a free visual tool for managing Redis databases.

**Download:**

- Visit: https://redis.io/insight/
- Available for Windows, macOS, and Linux
- Web-based interface included

**Features:**

- Visual key browser with search and filtering
- Real-time performance monitoring
- Query builder and CLI integration
- Slow log analysis
- Memory analysis and optimization
- Support for Redis modules (JSON, Search, etc.)

**Installation (Windows):**

```powershell
# Download installer from https://redis.io/insight/
# Or use Chocolatey:
choco install redis-insight
```

**Quick Start:**

1. Launch Redis Insight
2. Click "Add Redis Database"
3. Enter host (127.0.0.1), port (6379), and optional password
4. Browse keys, run commands, and monitor performance

**Useful for:**

- Exploring data visually
- Debugging connection issues
- Performance profiling
- Learning Redis commands interactively

## 13. Security Notes

* Do NOT store real API tokens/secrets inside committed code.
* Use environment variables / secret manager.
* Treat `APP_CONFIG_DATA` sample as placeholder only.

## 14. Redis vs SQL (Summary)

* Redis: speed, simple key-value, ephemeral/cache.
* SQL: relational integrity, complex queries, long-term storage.
* Use both: SQL as source of truth; Redis as low-latency cache.
