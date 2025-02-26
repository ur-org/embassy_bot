from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from .decorators import *
from app.settings import bot_settings, redis_settings
from .routers import commands_router, form_router, messages_router
from .middlewares import LoggingMiddleware


bot = Bot(token=bot_settings.TOKEN, parse_mode="html")
dp = Dispatcher(storage=RedisStorage.from_url(redis_settings.url))

# set middlewares
dp.message.outer_middleware(LoggingMiddleware())

# set routers
dp.include_router(form_router)
dp.include_router(commands_router)
dp.include_router(messages_router)


# @dp.errors_handler(exception=Exception)
# async def botblocked_error_handler(update: types.Update, e):
#     logging.warning("Error occured")
#     logging.warning(e)
#     return True
