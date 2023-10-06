from typing import Any

from aiogram import Router, F
from aiogram.types import (
    Message,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm import UserModel, UserUrlModel
from app.logger import logger
from bot.filters import ButtonFilter
from bot.buttons import (
    MainMenuButtons,
    ReturnToMainMenuButtons,
)
from bot.markups import (
    return_to_main_menu_markup,
    user_main_menu_markup,
)


class AddUrlStates(StatesGroup):
    enter_url = State()


url_router = Router()


@url_router.message(ButtonFilter(MainMenuButtons.ADD_URL))
async def handle_add_url_button(
    message: Message, state: FSMContext, session: AsyncSession
) -> Any:
    user_info = (
        await session.execute(
            select(UserModel)
            .where(UserModel.tg_id == message.from_user.id)
            .options(selectinload(UserModel.urls))
        )
    ).scalar_one()

    urls = user_info.urls
    text: str = (
        "Please send your url"
        if len(urls) == 0
        else f"You already have one url to check:\n**{urls[0].url}** \nTo update it send a new one"
    )

    await state.set_state(AddUrlStates.enter_url)
    await state.update_data(update=(len(urls) != 0))

    await message.answer(
        text=text,
        reply_markup=return_to_main_menu_markup(),
    )


@url_router.message(
    AddUrlStates.enter_url, ButtonFilter(ReturnToMainMenuButtons.RETURN)
)
async def handle_return_to_main_menu(message: Message, state: FSMContext) -> Any:
    await state.clear()
    await message.answer(
        text="Main menu",
        reply_markup=user_main_menu_markup(),
    )


@url_router.message(AddUrlStates.enter_url, ~F.text.contains("https://"))
async def handle_incorrect_url(message: Message, state: FSMContext) -> Any:
    await state.set_state(AddUrlStates.enter_url)
    await message.answer(
        text="Incorrect url, please try again",
        reply_markup=return_to_main_menu_markup(),
    )


@url_router.message(AddUrlStates.enter_url, F.text.contains("https://"))
async def handle_url_save(
    message: Message, state: FSMContext, session: AsyncSession
) -> Any:
    url: str = message.text.strip()
    data = await state.get_data()

    user_id = (
        select(UserModel.id)
        .where(UserModel.tg_id == message.from_user.id)
        .scalar_subquery()
    )

    if data["update"]:
        text = "Url updated successfully"
        await session.execute(
            update(UserUrlModel)
            .where(UserUrlModel.user_id == user_id)
            .values(
                {
                    UserUrlModel.url: url,
                }
            )
        )
    else:
        text = "Url added successfully"
        await session.execute(
            insert(UserUrlModel).values(
                {
                    UserUrlModel.url: url,
                    UserUrlModel.user_id: user_id,
                }
            )
        )

    await state.clear()

    await message.answer(
        text=text,
        reply_markup=user_main_menu_markup(),
    )
