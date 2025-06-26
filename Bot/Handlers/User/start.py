from aiogram.types import Message


async def start_cmd(message: Message) -> Message:
    return await message.answer(text="Hello World!")
