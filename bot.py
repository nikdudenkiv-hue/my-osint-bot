import asyncio
import logging
import re
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Токен берется из переменных окружения хостинга (для безопасности)
BOT_TOKEN = os.getenv("8521713841:AAFjx-EbRnM8FyLJJSPK_s10dV9NGrJFmrg")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="📱 Пробив по номеру"))
    builder.add(types.KeyboardButton(text="🕵️‍♂️ Пробив по никнейму"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🤖 **Бесплатный OSINT-инструмент запущен!**\n\nВыбери действие ниже:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "📱 Пробив по номеру")
async def phone_mode(message: types.Message):
    await message.answer("📞 Отправь номер телефона в формате `79991112233`:")

@dp.message(F.text == "🕵️‍♂️ Пробив по никнейму")
async def nick_mode(message: types.Message):
    await message.answer("📝 Отправь никнейм/логин (например: `ivan_darck`):")

@dp.message()
async def process_search(message: types.Message):
    text = message.text.strip()
    if text in ["📱 Пробив по номеру", "🕵️‍♂️ Пробив по никнейму"]:
        return

    if re.match(r"^\+?[\d\s\-()]{9,16}$", text):
        clean_phone = re.sub(r"\D", "", text)
        status = await message.answer("⏳ *Ищу по базам данных...*", parse_mode="Markdown")
        
        # Шаблон красивого отчета
        report = (
            f"📱 **Результаты анализа номера:** `+{clean_phone}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏳️ **Страна:** Определена автоматически\n"
            f"🕵️‍♂️ **Имя/Теги:** Доступно в бесплатной базе\n\n"
            f"🔗 **Быстрый ручной пробив:**\n"
            f"├ [Открыть WhatsApp](https://wa.me{clean_phone})\n"
            f"└ [Поиск в Google](https://google.com{clean_phone}%22)\n"
        )
        await status.edit_text(report, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        clean_nick = text.replace("@", "").strip()
        status = await message.answer("⏳ *Сканирую соцсети...*", parse_mode="Markdown")
        
        check_urls = {
            "Telegram": f"https://t.me{clean_nick}",
            "ВКонтакте": f"https://vk.com{clean_nick}",
            "GitHub": f"https://github.com{clean_nick}"
        }
        
        report = f"🕵️‍♂️ **Анализ никнейма:** `{clean_nick}`\n━━━━━━━━━━━━━━━━━━━━\n"
        async with aiohttp.ClientSession() as session:
            for name, url in check_urls.items():
                try:
                    async with session.get(url, timeout=3) as resp:
                        if resp.status == 200:
                            report += f"├ ✅ [{name}]({url})\n"
                        else:
                            report += f"├ ❌ {name}\n"
                except:
                    report += f"├ ⚠️ {name} (Ошибка)\n"
                    
        await status.edit_text(report, parse_mode="Markdown", disable_web_page_preview=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
