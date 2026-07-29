from __future__ import annotations

from datetime import datetime, timezone

from ..domain import Region, StatusSnapshot
from ..ports import EventProvider, StateRepository


class StatusService:
    """Read live state and fall back to the last successful snapshot."""

    def __init__(
        self,
        provider: EventProvider,
        repository: StateRepository,
    ) -> None:
        self._provider = provider
        self._repository = repository

    async def get_status(self, region: Region) -> StatusSnapshot:
        try:
            state = await self._provider.fetch(region)
        except Exception:
            cached = await self._repository.load(region)
            if cached is None:
                raise
            return StatusSnapshot(
                region=region,
                state=cached,
                is_fallback=True,
                source="last-known-good",
                updated_at=cached.observed_at,
            )

        await self._repository.save(region, state)
        return StatusSnapshot(
            region=region,
            state=state,
            is_fallback=False,
            source="demo-provider",
            updated_at=datetime.now(timezone.utc),
        )
