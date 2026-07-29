from __future__ import annotations

import unittest
from datetime import datetime, timezone

from stalem_showcase.domain import NotificationKind, Region
from stalem_showcase.infrastructure import InMemoryDeliveryRepository
from stalem_showcase.services import NotificationService


class RecordingNotifier:
    def __init__(self) -> None:
        self.messages: list[tuple[int, str]] = []

    async def send(self, recipient_id: int, text: str) -> None:
        self.messages.append((recipient_id, text))


class NotificationTests(unittest.IsolatedAsyncioTestCase):
    async def test_same_delivery_is_sent_only_once(self) -> None:
        notifier = RecordingNotifier()
        service = NotificationService(InMemoryDeliveryRepository(), notifier)
        event_time = datetime.now(timezone.utc)
        arguments = {
            "recipient_id": 42,
            "region": Region.RU,
            "kind": NotificationKind.EVENT_STARTED,
            "event_time": event_time,
            "text": "Synthetic event notification",
        }

        first = await service.send_once(**arguments)
        second = await service.send_once(**arguments)

        self.assertTrue(first)
        self.assertFalse(second)
        self.assertEqual(notifier.messages, [(42, "Synthetic event notification")])


if __name__ == "__main__":
    unittest.main()
