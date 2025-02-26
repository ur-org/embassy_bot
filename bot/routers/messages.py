from aiogram import Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import CustomMessageFilter


messages_router = Router()


# using custom filters
@messages_router.message(CustomMessageFilter(text="wow"))
async def start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        text="yeah"
    )


# using magic filters
# https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/magic_filters.html
@messages_router.message(F.is_("lol"))
async def start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        text="lmao"
    )


@messages_router.message(F.contains("yes"))
async def start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        text="Of course!"
    )


@messages_router.message()
async def start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        text=message.text
    )
