# bot.py — обновлённый для aiogram 3.7+

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from xynth_scoring import get_top_tokens_with_scores

# === ТВОИ ДАННЫЕ ===
BOT_TOKEN = "7833598614:AAFgdqV2LNVZmlUg-3V0b16D4zD3zSZRHgs"
ADMIN_ID = 520861  # ← Вставь свой Telegram ID

# === ИНИЦИАЛИЗАЦИЯ ===
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# === КОМАНДА /start ===
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("🤖 Xynth Crypto Alert активирован! Я пришлю сигнал, если найду токен с высоким скором.")

# === АЛЕРТ-ФУНКЦИЯ ===
async def check_and_alert():
    while True:
        tokens = get_top_tokens_with_scores()
        for token in tokens:
            if token["score"] >= 70:
                message = (
                    f"🔥 <b>[Xynth Alert]</b>\n"
                    f"<b>Токен:</b> ${token['symbol']}\n"
                    f"<b>Общий скор:</b> {token['score']} / 100\n"
                    f"Сентимент: {token['sentiment']}\n"
                    f"Ончейн: {token['onchain']}\n"
                    f"Финансы: {token['finance']}\n"
                    f"Dev активность: {token['dev']}"
                )
                await bot.send_message(ADMIN_ID, message)
        await asyncio.sleep(86400)

# === ЗАПУСК ===
async def main():
    asyncio.create_task(check_and_alert())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
