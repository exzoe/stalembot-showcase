from __future__ import annotations

from datetime import datetime

from ..domain import NotificationKind, Region
from ..ports import DeliveryRepository, Notifier


class NotificationService:
    """Send an event notification at most once per recipient.

    Decision rules that choose *when* a notification should be produced are
    intentionally absent from the public repository.
    """

    def __init__(
        self,
        delivery_repository: DeliveryRepository,
        notifier: Notifier,
    ) -> None:
        self._deliveries = delivery_repository
        self._notifier = notifier

    async def send_once(
        self,
        *,
        recipient_id: int,
        region: Region,
        kind: NotificationKind,
        event_time: datetime,
        text: str,
    ) -> bool:
        if await self._deliveries.was_delivered(
            region,
            kind,
            event_time,
            recipient_id,
        ):
            return False

        await self._notifier.send(recipient_id, text)
        await self._deliveries.mark_delivered(
            region,
            kind,
            event_time,
            recipient_id,
        )
        return True
