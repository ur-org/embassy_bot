from aiogram.filters import Filter
from aiogram.types import Message


class ButtonFilter(Filter):
    def __init__(self, text: str) -> None:
        self.text = text

    async def __call__(self, message: Message) -> bool:
        return message.text.lower() == self.text.lower()
