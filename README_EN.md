<div align="center">

# STALEM Bot — public showcase

**Architecture showcase for a production Telegram game-event monitoring bot**

[Русская версия](README.md) · [Case study](docs/CASE_STUDY.md) · [Architecture](docs/ARCHITECTURE.md) · [Security boundary](docs/SECURITY_BOUNDARY.md)

</div>

> [!IMPORTANT]
> This is not the production source code. The repository was rebuilt as a
> portfolio artifact and excludes the private API contract, forecasting
> algorithms, user data, and deployment infrastructure.

## Project

STALEM is a Telegram service that monitors game events across regional servers,
shows current status, and sends personalized notifications. The production bot
is used by **200+ players**.

- Telegram: [@stalembot](https://t.me/stalembot)
- Developer: [@exzoe](https://github.com/exzoe)

## What this repository demonstrates

- asynchronous application services;
- domain / ports / infrastructure separation;
- typed `Protocol` interfaces;
- concurrent regional polling with `asyncio.gather`;
- per-region fault isolation;
- last-known-good fallback;
- idempotent notification delivery;
- synthetic provider instead of the real API;
- unit tests, GitHub Actions, and a local secret scanner.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
stalem-showcase
python scripts/check.py
```

## Intentionally excluded

- production API URL, authentication, and response schema;
- forecasting formulas and timing parameters;
- production SQLite schema and migrations;
- administrative broadcast queue;
- user data, logs, backups, and VPS configuration;
- working tokens or credentials.

Production code can be shown privately during a technical interview when
appropriate.

## Production stack

`Python` · `aiogram 3` · `asyncio` · `aiohttp` · `SQLite/WAL` · `pytest` · `systemd`

STALEM is an unofficial third-party service. All names and trademarks belong to
their respective owners.
