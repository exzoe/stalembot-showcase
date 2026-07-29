from __future__ import annotations

import asyncio
from dataclasses import dataclass
from collections.abc import Iterable

from ..domain import Region, StatusSnapshot
from .status import StatusService


@dataclass(frozen=True, slots=True)
class RegionResult:
    region: Region
    snapshot: StatusSnapshot | None
    error: Exception | None

    @property
    def is_success(self) -> bool:
        return self.error is None


class RegionMonitor:
    """Poll regions concurrently while isolating per-region failures."""

    def __init__(self, status_service: StatusService) -> None:
        self._status_service = status_service

    async def poll(self, regions: Iterable[Region]) -> dict[Region, RegionResult]:
        region_list = tuple(regions)
        raw_results = await asyncio.gather(
            *(self._status_service.get_status(region) for region in region_list),
            return_exceptions=True,
        )

        output: dict[Region, RegionResult] = {}
        for region, value in zip(region_list, raw_results, strict=True):
            if isinstance(value, Exception):
                output[region] = RegionResult(region, None, value)
            else:
                output[region] = RegionResult(region, value, None)
        return output
