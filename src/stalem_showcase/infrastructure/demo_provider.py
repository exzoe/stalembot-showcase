from __future__ import annotations

import asyncio
from collections.abc import Mapping

from ..domain import EventState, Region


class DemoEventProvider:
    """Deterministic provider with synthetic data only.

    It deliberately contains no production URL, authentication method,
    response schema, retry policy, or game-specific timing algorithm.
    """

    def __init__(
        self,
        states: Mapping[Region, EventState],
        *,
        failing_regions: set[Region] | None = None,
        latency_seconds: float = 0.01,
    ) -> None:
        self._states = dict(states)
        self._failing_regions = failing_regions or set()
        self._latency_seconds = max(0.0, latency_seconds)

    async def fetch(self, region: Region) -> EventState:
        await asyncio.sleep(self._latency_seconds)
        if region in self._failing_regions:
            raise ConnectionError(f"Synthetic provider failure for {region.value}")
        try:
            return self._states[region]
        except KeyError as exc:
            raise LookupError(f"No demo state configured for {region.value}") from exc
