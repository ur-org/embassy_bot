from typing import List
from io import BytesIO

from aiogram import Router
from aiogram.types import (
    Message,
    BufferedInputFile,
)
from aiogram.filters import Command
from sqlalchemy import select, insert
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession
import plotly.graph_objects as go

from app.logger import logger
from app.database.orm import (
    UserModel,
    UrlUpdateModel,
    UserUrlModel,
)
from app.services.embassy import get_image
from bot.const.phrases import phrase_for_start_first_greeting
from bot.markups import user_main_menu_markup

# from bot.background_tasks import send_message_task

commands_router = Router()


@commands_router.message(Command(commands=["start"]))
async def start(message: Message, session: AsyncSession) -> None:
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
            insert(UserModel).values(
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


@commands_router.message(Command(commands=["stat"]))
async def stat(message: Message, session: AsyncSession) -> None:
    args = message.text.split(" ")[1:]
    limit = args[0] if args else 10

    subq = (
        select(UrlUpdateModel.id)
        .filter(UrlUpdateModel.url_id == UserUrlModel.id)
        .order_by(UrlUpdateModel.created_at.desc(), UrlUpdateModel.id)
        .limit(limit)
        .correlate(UserUrlModel)
        .subquery()
    )

    user_info: List[UrlUpdateModel] = (
        (
            await session.execute(
                select(UserModel)
                .where(UserModel.tg_id == message.from_user.id)
                .outerjoin(UserModel.urls)
                .outerjoin(UrlUpdateModel, UrlUpdateModel.id.in_(subq))
                .options(
                    contains_eager(
                        UserModel.urls,
                        UserUrlModel.statuses,
                    )
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )

    urls = user_info.urls

    for url in urls:
        ids = []
        dates = []
        results = []
        for update in url.statuses:
            ids.append(update.id)
            dates.append(update.created_at.strftime("%Y-%m-%d %H:%M:%S"))

            status = update.status
            if update.is_error:
                status = "Error"
            results.append(status)

        logger.info(f"TEST: {dates} - {results}")

        (margin_left, margin_right) = (1, 1)
        layout = go.Layout(
            autosize=False,
            margin=dict(
                l=margin_left,
                r=margin_right,
                t=1,
                b=1,
            ),
            width=350,
            height=(
                30 * (len(url.statuses) + 1) + margin_left + margin_right
            ),  # heights of header and rows + top and bottom margins
        )
        fig = go.Figure(
            layout=layout,
            data=[
                go.Table(
                    columnwidth=[10, 60, 30],
                    header=dict(
                        values=["id", "date", "result"],
                        align=["center", "center"],
                        fill_color="#E5D1FA",
                        height=30,
                        font=dict(
                            color="#303841",
                            size=10,
                        ),
                    ),
                    cells=dict(
                        values=[
                            ids,
                            dates,
                            results,
                        ],
                        align=["center", "center"],
                        fill_color="#ECF2FF",
                        height=30,
                        font=dict(
                            color="#303841",
                            size=10,
                        ),
                    ),
                )
            ],
        )

        await message.answer_photo(
            photo=BufferedInputFile(file=fig.to_image(scale=2), filename="image.png"),
            caption=url.url,
        )


@commands_router.message(Command(commands=["out"]))
async def stat(message: Message, session: AsyncSession) -> None:
    args = message.text.split(" ")[1:]
    update_id = int(args[0] if args else 10)

    update = (
        await session.execute(
            select(UrlUpdateModel).where(UrlUpdateModel.id == update_id)
        )
    ).scalar_one_or_none()

    await message.answer_photo(
        photo=BufferedInputFile(
            file=get_image(tg_id=message.from_user.id, timestamp=update.timestamp),
            filename="image.png",
        ),
        caption=f"Output image for update #{update_id}",
    )
