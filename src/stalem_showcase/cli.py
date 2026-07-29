from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from .domain import EventState, Region
from .infrastructure import DemoEventProvider, InMemoryStateRepository
from .services import RegionMonitor, StatusService


def _demo_states() -> dict[Region, EventState]:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    return {
        Region.RU: EventState(now - timedelta(minutes=8), None, None, now),
        Region.EU: EventState(None, now - timedelta(hours=5), now - timedelta(hours=4), now),
        Region.NA: EventState(None, now - timedelta(hours=3), now - timedelta(hours=2), now),
        Region.SEA: EventState(None, now - timedelta(hours=7), now - timedelta(hours=6), now),
    }


async def _run() -> None:
    repository = InMemoryStateRepository()
    provider = DemoEventProvider(_demo_states())
    monitor = RegionMonitor(StatusService(provider, repository))

    results = await monitor.poll(Region)
    for region, result in results.items():
        if result.error is not None:
            print(f"{region.value}: unavailable ({result.error})")
            continue
        assert result.snapshot is not None
        state = "active" if result.snapshot.state.is_active else "idle"
        print(
            f"{region.value}: {state}; source={result.snapshot.source}; "
            f"fallback={result.snapshot.is_fallback}"
        )


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
