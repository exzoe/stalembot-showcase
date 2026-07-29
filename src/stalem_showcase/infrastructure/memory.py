from __future__ import annotations

import asyncio
from datetime import datetime

from ..domain import EventState, NotificationKind, Region


class InMemoryStateRepository:
    """Small repository used by the runnable showcase and tests."""

    def __init__(self) -> None:
        self._states: dict[Region, EventState] = {}
        self._lock = asyncio.Lock()

    async def save(self, region: Region, state: EventState) -> None:
        async with self._lock:
            self._states[region] = state

    async def load(self, region: Region) -> EventState | None:
        async with self._lock:
            return self._states.get(region)


class InMemoryDeliveryRepository:
    """Idempotency store that models the production delivery log."""

    def __init__(self) -> None:
        self._keys: set[tuple[Region, NotificationKind, datetime, int]] = set()
        self._lock = asyncio.Lock()

    async def was_delivered(
        self,
        region: Region,
        kind: NotificationKind,
        event_time: datetime,
        recipient_id: int,
    ) -> bool:
        key = (region, kind, event_time, recipient_id)
        async with self._lock:
            return key in self._keys

    async def mark_delivered(
        self,
        region: Region,
        kind: NotificationKind,
        event_time: datetime,
        recipient_id: int,
    ) -> None:
        key = (region, kind, event_time, recipient_id)
        async with self._lock:
            self._keys.add(key)
