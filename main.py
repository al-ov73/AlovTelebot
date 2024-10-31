import asyncio
import fastapi
import logging
import sys
from os import getenv

from unicorn import Unicorn

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = '6914939892:AAHxAsWcHIEIcaEz0qgtLGY6XA0Fz64n95A'

dp = Dispatcher()

app = fastapi.FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


def run_server():
    unicorn = Unicorn(worker_class='sync', config={
        'bind': '127.0.0.1:8000',
        'worker_processes': 4,
        'timeout': 60
    })
    unicorn.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run_server()
    asyncio.run(main())
