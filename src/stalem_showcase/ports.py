from __future__ import annotations

from datetime import datetime
from typing import Protocol

from .domain import EventState, NotificationKind, Region


class EventProvider(Protocol):
    async def fetch(self, region: Region) -> EventState:
        """Fetch a normalized state for one region."""


class StateRepository(Protocol):
    async def save(self, region: Region, state: EventState) -> None:
        """Persist the latest successful state."""

    async def load(self, region: Region) -> EventState | None:
        """Return the latest persisted state, if available."""


class DeliveryRepository(Protocol):
    async def was_delivered(
        self,
        region: Region,
        kind: NotificationKind,
        event_time: datetime,
        recipient_id: int,
    ) -> bool:
        """Check whether an idempotent notification was already delivered."""

    async def mark_delivered(
        self,
        region: Region,
        kind: NotificationKind,
        event_time: datetime,
        recipient_id: int,
    ) -> None:
        """Record a successful delivery."""


class Notifier(Protocol):
    async def send(self, recipient_id: int, text: str) -> None:
        """Deliver a message through an external channel."""
