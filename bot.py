import asyncio
import logging
import re
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = "8521713841:AAFjx-EbRnM8FyLJJSPK_s10dV9NGrJFmrg"  # Вставь сюда свой токен прямо в кавычках

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="📱 Пробить номер телефона"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🕵️‍♂️ **OSINT-Анализатор запущен.**\n\n"
        "Этот бот ищет информацию по открытым цифровым следам и архивам интернета.",
        reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "📱 Пробить номер телефона")
async def phone_mode(message: types.Message):
    await message.answer("📞 Отправь номер телефона (например: `79774637127`):", parse_mode="Markdown")

@dp.message()
async def process_phone_osint(message: types.Message):
    text = message.text.strip()
    if text == "📱 Пробить номер телефона": return

    # Очистка номера
    clean_phone = re.sub(r"\D", "", text)
    if len(clean_phone) < 10:
        await message.answer("❌ Неверный формат номера. Введи минимум 10 цифр.")
        return

    status = await message.answer("🔍 *Сканирую открытые источники и цифровые следы...*", parse_mode="Markdown")

    # Форматирование для разных поисковых систем
    formatted_dash = f"{clean_phone[0]}-{clean_phone[1:4]}-{clean_phone[4:7]}-{clean_phone[7:9]}-{clean_phone[9:]}" # 7-977-463-71-27
    
    # Собираем досье из бесплатных OSINT-линков
    report = (
        f"📱 **Досье на номер:** `+{clean_phone}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🚩 **Базовый анализ:**\n"
        f"├ Страна: Россия/СНГ\n"
        f"└ Мессенджеры: [Проверить WhatsApp](https://wa.me{clean_phone}), [Проверить Viber](viber://chat?number=%2B{clean_phone})\n\n"
        f"⚙️ **Поиск слитых адресов и объявлений (Бесплатно):**\n"
        f"Платные боты берут данные отсюда. Проверь эти ссылки вручную, чтобы увидеть объявления, старые профили и кэш сайтов, где человек мог оставить адрес:\n\n"
        f"├ [Google (Точное совпадение)](https://google.com{clean_phone}%22)\n"
        f"├ [Яндекс (Поиск по кэшу объявлений)](https://yandex.ru{clean_phone}%22)\n"
        f"├ [Поиск формата с дефисами]({f'https://google.com{formatted_dash}%22'})\n"
        f"├ [Проверка в базе честных людей](https://mysmsbox.ru{clean_phone})\n"
        f"└ [Анализ тегов и отзывов](https://zvonili.com{clean_phone})\n\n"
        f"💡 *Совет:* Если номер был слит в базах доставки еды или объявлений, Google и Яндекс покажут сохраненную копию страницы со старым адресом абсолютно бесплатно."
    )

    await status.edit_text(report, parse_mode="Markdown", disable_web_page_preview=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
