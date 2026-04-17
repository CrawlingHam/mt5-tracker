# MT5 Tracker API

A local Flask API that reads trading/account data from a locally installed MetaTrader 5 terminal via the Python `MetaTrader5` package.

This project is intended to run on your machine (or trusted local network), then be consumed by a frontend or local tools.

## What This API Does

- Connects to your local MT5 terminal.
- Exposes account, open positions, and trade history endpoints.
- Provides a combined `/all` endpoint for a single aggregated payload.
- Adds CORS support for configured origins.
- Logs requests with method, path, status code, and response time.

## Important Requirement: Local MT5 Installation

This API does **not** connect directly to a remote broker API on its own. It depends on:

- MetaTrader 5 desktop terminal installed locally.
- MT5 terminal logged into your trading account.
- MT5 terminal available/running for the Python bridge to initialize.

If MT5 cannot initialize, routes that call `init_mt5()` will fail.

## Tech Stack

- Python
- Flask
- Flask-CORS
- MetaTrader5 (Python package)
- Waitress (for production-style serving on Windows)

## Project Structure (High Level)

- `src/main.py` - app bootstrap, CORS, middleware, route registration
- `src/routes/` - route handlers:
  - `account.py`
  - `trades.py`
  - `positions.py`
  - `health.py`
  - `all.py`
- `src/types/responses/` - response dataclasses
- `src/utils/` - shared utilities (date parsing, DTO mapping, strings, env loader)
- `src/configs/` - environment-driven app configuration

## Environment Configuration

Current env file example (`.env.development`):

```env
ALLOWED_ORIGINS=http://localhost:5173
ENVIRONMENT=development
PORT=8004
```

### Variables

- `ALLOWED_ORIGINS`: comma-separated allowed origins for CORS.
- `ENVIRONMENT`: `development` or `production`.
- `PORT`: port used by `src/main.py` when running with Flask dev server.

## Setup

## 1) Create and activate virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Install Python dependencies

If you do not have a `requirements.txt`, install directly:

```powershell
python -m pip install flask flask-cors MetaTrader5 waitress
```

## 3) Configure environment

Create/update `.env.development` with the variables shown above.

## 4) Start the API

Using project scripts:

```powershell
pnpm dev
```

or

```powershell
pnpm start
```

### Script behavior

- `pnpm dev` -> runs Flask directly (`python -m src.main`).
- `pnpm start` -> runs Waitress (`python -m waitress ... src.main:app`).

Note: Waitress in `package.json` currently listens on `127.0.0.1:8004` explicitly.

## Runtime Behavior

- Debug mode is controlled by `ENVIRONMENT`:
  - `development` -> debug on
  - `production` -> debug off
- Request logs are emitted by middleware in this format:
  - `METHOD /path -> status (duration_ms)`

## API Endpoints

Base URL (default): `http://127.0.0.1:8004`

All current endpoints are `GET`.

### `GET /health`

Checks MT5 connection and terminal info.

- Query params: none
- Body: none

Example:

```bash
curl "http://127.0.0.1:8004/health"
```

### `GET /account`

Returns account information.

- Query params: none
- Body: none

Example:

```bash
curl "http://127.0.0.1:8004/account"
```

### `GET /positions`

Returns open positions.

- Query params: none
- Body: none

Example:

```bash
curl "http://127.0.0.1:8004/positions"
```

### `GET /trades`

Returns trade history in a date range.

- Query params:
  - `from_date` (optional)
  - `to_date` (optional)
- Body: none

Accepted date formats:

- Date only: `YYYY-MM-DD`
- Datetime: ISO format, e.g. `YYYY-MM-DDTHH:MM:SS`

Date handling behavior:

- If both omitted:
  - `from_date` defaults to `1999-01-01`
  - `to_date` defaults to `now`
- If `from_date` is date-only and `to_date` omitted:
  - `to_date` becomes end of that same day (`23:59:59.999999`)
- If `to_date` provided as date-only:
  - treated as end of that day
- If `from_date > to_date`:
  - returns `400 BAD_REQUEST`

Examples:

```bash
curl "http://127.0.0.1:8004/trades"
curl "http://127.0.0.1:8004/trades?from_date=2026-04-17"
curl "http://127.0.0.1:8004/trades?from_date=2026-04-17&to_date=2026-04-17"
curl "http://127.0.0.1:8004/trades?from_date=2026-04-17T00:00:00&to_date=2026-04-17T12:00:00"
```

### `GET /all`

Aggregates `/account`, `/positions`, `/trades`, and `/health` style data into one response.

- Query params:
  - `from_date` (optional)
  - `to_date` (optional)
- Body: none

Uses the same date parsing/range rules as `/trades`.

Examples:

```bash
curl "http://127.0.0.1:8004/all"
curl "http://127.0.0.1:8004/all?from_date=2026-04-17"
curl "http://127.0.0.1:8004/all?from_date=2026-04-17&to_date=2026-04-17"
```

## Response Shape Notes

- Responses are backed by dataclasses in `src/types/responses/`.
- `/all` uses an aggregate dataclass (`MT5AllResponse`).
- Error responses for invalid date input return JSON:
  - `{"error": "..."}` with `400`.

## CORS Notes

`ALLOWED_ORIGINS` supports comma-separated values. Origins are normalized so values without scheme may be resolved to `https://...` in some cases.

Example:

```env
ALLOWED_ORIGINS=http://localhost:5173,https://my-app.example.com
```

## Troubleshooting

### MT5 initialization errors

- Confirm MT5 desktop terminal is installed and running.
- Confirm you are logged in to an account in MT5.
- Ensure no permission/security restrictions are blocking local bridge usage.

### No trades returned

- Check date range and format.
- Remember date-only params are interpreted as day boundaries.
- MT5 history depends on what terminal/account history is available.

### "Development server" warning

- Appears when running Flask dev server (`pnpm dev`).
- Use `pnpm start` (Waitress) for production-style serving.

## Security / Deployment Notes

- Intended for local/trusted usage.
- If exposed beyond localhost:
  - tighten CORS
  - add authentication
  - consider rate limiting
  - run behind proper network controls
