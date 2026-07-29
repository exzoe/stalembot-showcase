from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class Region(str, Enum):
    """Regions supported by the production service."""

    RU = "RU"
    EU = "EU"
    NA = "NA"
    SEA = "SEA"

    @classmethod
    def parse(cls, value: str) -> "Region":
        try:
            return cls(value.strip().upper())
        except ValueError as exc:
            supported = ", ".join(item.value for item in cls)
            raise ValueError(f"Unsupported region. Expected one of: {supported}") from exc


class NotificationKind(str, Enum):
    EVENT_STARTED = "event_started"
    EVENT_ENDED = "event_ended"
    STATUS_CHANGED = "status_changed"


@dataclass(frozen=True, slots=True)
class EventState:
    """Normalized state returned by an abstract external provider.

    The public showcase intentionally omits the real API response schema and
    all production forecasting parameters.
    """

    current_start: datetime | None
    previous_start: datetime | None
    previous_end: datetime | None
    observed_at: datetime

    def __post_init__(self) -> None:
        timestamps = (
            self.current_start,
            self.previous_start,
            self.previous_end,
            self.observed_at,
        )
        if any(value is not None and value.tzinfo is None for value in timestamps):
            raise ValueError("All timestamps must be timezone-aware")

    @property
    def is_active(self) -> bool:
        return self.current_start is not None

    @classmethod
    def empty(cls) -> "EventState":
        return cls(
            current_start=None,
            previous_start=None,
            previous_end=None,
            observed_at=datetime.now(timezone.utc),
        )


@dataclass(frozen=True, slots=True)
class StatusSnapshot:
    region: Region
    state: EventState
    is_fallback: bool
    source: str
    updated_at: datetime
