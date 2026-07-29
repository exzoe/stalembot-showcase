from __future__ import annotations

import unittest
from datetime import datetime, timezone

from stalem_showcase.domain import EventState, Region


class DomainTests(unittest.TestCase):
    def test_region_is_case_insensitive(self) -> None:
        self.assertEqual(Region.parse(" eu "), Region.EU)

    def test_unknown_region_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Region.parse("MARS")

    def test_event_state_requires_aware_timestamps(self) -> None:
        with self.assertRaises(ValueError):
            EventState(None, None, None, datetime.now())

    def test_active_state_is_derived_from_current_start(self) -> None:
        now = datetime.now(timezone.utc)
        state = EventState(now, None, None, now)
        self.assertTrue(state.is_active)


if __name__ == "__main__":
    unittest.main()
