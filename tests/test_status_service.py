from __future__ import annotations

import unittest
from datetime import datetime, timezone

from stalem_showcase.domain import EventState, Region
from stalem_showcase.infrastructure import DemoEventProvider, InMemoryStateRepository
from stalem_showcase.services import StatusService


class StatusServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_successful_state_is_saved(self) -> None:
        now = datetime.now(timezone.utc)
        state = EventState(None, now, now, now)
        repository = InMemoryStateRepository()
        service = StatusService(DemoEventProvider({Region.RU: state}), repository)

        snapshot = await service.get_status(Region.RU)

        self.assertFalse(snapshot.is_fallback)
        self.assertEqual(await repository.load(Region.RU), state)

    async def test_cached_state_is_used_after_provider_failure(self) -> None:
        now = datetime.now(timezone.utc)
        cached = EventState(None, now, now, now)
        repository = InMemoryStateRepository()
        await repository.save(Region.EU, cached)
        provider = DemoEventProvider(
            {Region.EU: cached},
            failing_regions={Region.EU},
        )
        service = StatusService(provider, repository)

        snapshot = await service.get_status(Region.EU)

        self.assertTrue(snapshot.is_fallback)
        self.assertEqual(snapshot.source, "last-known-good")
        self.assertEqual(snapshot.state, cached)

    async def test_failure_without_cache_is_propagated(self) -> None:
        repository = InMemoryStateRepository()
        provider = DemoEventProvider({}, failing_regions={Region.NA})
        service = StatusService(provider, repository)

        with self.assertRaises(ConnectionError):
            await service.get_status(Region.NA)


if __name__ == "__main__":
    unittest.main()
