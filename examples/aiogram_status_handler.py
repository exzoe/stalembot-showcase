"""Illustrative aiogram 3 adapter.

This file is intentionally not wired to a real Telegram token or external API.
Install aiogram separately to experiment with the adapter.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from stalem_showcase.domain import Region
from stalem_showcase.services import StatusService


def build_status_router(service: StatusService) -> Router:
    router = Router(name="public-showcase-status")

    @router.message(Command("status"))
    async def status_handler(message: Message) -> None:
        snapshot = await service.get_status(Region.RU)
        state_label = "event is active" if snapshot.state.is_active else "waiting"
        fallback_label = " (cached)" if snapshot.is_fallback else ""
        await message.answer(f"RU: {state_label}{fallback_label}")

    return router
