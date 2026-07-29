from __future__ import annotations

import unittest
from datetime import datetime, timezone

from stalem_showcase.domain import EventState, Region
from stalem_showcase.infrastructure import DemoEventProvider, InMemoryStateRepository
from stalem_showcase.services import RegionMonitor, StatusService


class MonitorTests(unittest.IsolatedAsyncioTestCase):
    async def test_one_region_failure_does_not_cancel_others(self) -> None:
        now = datetime.now(timezone.utc)
        state = EventState(None, now, now, now)
        provider = DemoEventProvider(
            {Region.RU: state, Region.EU: state},
            failing_regions={Region.EU},
        )
        monitor = RegionMonitor(StatusService(provider, InMemoryStateRepository()))

        results = await monitor.poll([Region.RU, Region.EU])

        self.assertTrue(results[Region.RU].is_success)
        self.assertFalse(results[Region.EU].is_success)
        self.assertIsInstance(results[Region.EU].error, ConnectionError)


if __name__ == "__main__":
    unittest.main()
