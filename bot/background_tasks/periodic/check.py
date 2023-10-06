import asyncio
from typing import List, Dict

from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from app.logger import logger
from app.services.embassy import get_schedule_update
from app.database.orm.core import async_sessionmaker
from app.celery import celery_app
from app.database.orm import UserModel, UrlUpdateModel
from app.database.schema import UserSchema


async def get_users() -> List[UserSchema]:
    async with async_sessionmaker.begin() as session:
        return (
            (
                await session.execute(
                    select(UserModel).options(selectinload(UserModel.urls))
                )
            )
            .scalars()
            .all()
        )


async def add_update_result(
    url_id: int, status: bool, timestamp: int, is_error: bool
) -> None:
    async with async_sessionmaker.begin() as session:
        await session.execute(
            insert(UrlUpdateModel).values(
                {
                    UrlUpdateModel.url_id: url_id,
                    UrlUpdateModel.status: status,
                    UrlUpdateModel.timestamp: timestamp,
                    UrlUpdateModel.is_error: is_error,
                }
            )
        )


@celery_app.task()
def background_task():
    loop = asyncio.get_event_loop()
    users = loop.run_until_complete(get_users())
    logger.info(f"Users found: {len(users)}")

    for user in users:
        for url in user.urls:
            response = get_schedule_update(
                tg_id=user.tg_id,
                url=url.url,
            )

            if response and response.get("result", {}).get("available"):
                from bot import bot_instance

                loop.run_until_complete(
                    bot_instance.send_message(
                        chat_id=user.tg_id,
                        text=f"‼️‼️ There's an available slot, hurry set the appointment right now: {url.url}",
                    )
                )

            loop.run_until_complete(
                add_update_result(
                    url_id=url.id,
                    status=response.get("result", {}).get("available") if response else None,
                    timestamp=response.get("result", {}).get("timestamp") if response else None,
                    is_error=response.get("error") if response else True,
                )
            )
