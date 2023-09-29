from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile, MenuButtonWebApp, WebAppInfo
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.database.orm import UserModel
from bot.const.phrases import phrase_for_start_first_greeting
from bot.markups import user_main_menu_markup
# from bot.background_tasks import send_message_task

commands_router = Router()


@commands_router.message(Command(commands=["start"]))
async def start(message: Message, bot: Bot, session: AsyncSession) -> None:
    first_name = message.from_user.first_name
    text = phrase_for_start_first_greeting(data=dict(user_name=first_name))

    # # sending image sticker
    # sticker = FSInputFile("static/hello.webp")
    # await message.answer_sticker(sticker)

    # check if user exists
    user = (
        await session.execute(
            select(UserModel).where(UserModel.tg_id.__eq__(message.from_user.id))
        )
    ).scalar_one_or_none()

    # if not => create
    if not user:
        await session.execute(
            insert(UserModel)
            .values(
                {
                    UserModel.first_name: first_name,
                    UserModel.tg_id: message.from_user.id,
                    UserModel.tg_username: message.from_user.username,
                    UserModel.is_admin: False,
                }
            )
        )
        await session.commit()

    # await bot.set_chat_menu_button(
    #     chat_id=message.chat.id,
    #     menu_button=MenuButtonWebApp(
    #         text="Open Menu",
    #         web_app=WebAppInfo(url=f"{application_settings.APP_HOSTNAME}/menu/"),
    #     ),
    # )

    await message.answer(
        text=text,
        reply_markup=user_main_menu_markup(),
    )


# @commands_router.message(Command(commands=["check"]))
# async def check(message: Message, bot: Bot) -> None:
#     task = send_message_task.apply_async(args=[message.from_user.id])

#     await message.answer(
#         text="Ok",
#     )
