import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
URL_FORTE = os.getenv("URL_FORTE")
URL_JUSAN = os.getenv("URL_JUSAN")
URL_BCC = os.getenv("URL_BCC")

# Проверка, что токен загружен
if not BOT_TOKEN:
    raise ValueError("Ошибочка: BOT_TOKEN не найден! Проверь содержимое файла .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ----------------- Клавиатуры -----------------

# 1. Шаг: Выбор типа бизнеса
kb_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇰🇿 ИП", callback_data="type_ip"),
            InlineKeyboardButton(text="🏢 ТОО", callback_data="type_too"),
        ],
        [
            InlineKeyboardButton(
                text="🚀 Только планирую открыть", callback_data="type_new"
            )
        ],
    ]
)

# 2. Шаг: Нужен ли эквайринг / QR
kb_eq = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📱 Да (Kaspi QR / Терминал)", callback_data="eq_yes"
            )
        ],
        [
            InlineKeyboardButton(
                text="💳 Только безналичные переводы", callback_data="eq_no"
            )
        ],
    ]
)

# ----------------- Хэндлеры -----------------


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Я помогу подобрать идеальный расчетный счет (РКО) для твоего бизнеса в Казахстане "
        f"без лишних комиссий и скрытых платежей.\n\n"
        f"Выбери формат твоего бизнеса:",
        reply_markup=kb_type,
    )


@dp.callback_query(F.data.startswith("type_"))
async def process_type(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Принимаешь ли ты оплату от физлиц (через QR, карты или кассу)?",
        reply_markup=kb_eq,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("eq_"))
async def process_result(callback: types.CallbackQuery):
    # Ссылки берутся из загруженных переменных окружения
    kb_offers = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏛 ForteBank (0₸ обслуживание)", url=URL_FORTE)],
            [
                InlineKeyboardButton(
                    text="⚡ Jusan Business (Быстрый старт)", url=URL_JUSAN
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Банк ЦентрКредит (Лучший ВЭД)", url=URL_BCC
                )
            ],
        ]
    )

    await callback.message.edit_text(
        "📊 **Подходящие банки для твоих условий:**\n\n"
        "1. **ForteBank:** Бесплатное открытие, 0₸ за обслуживание на стартовых тарифах, выгодный эквайринг.\n"
        "2. **Jusan Business:** Открытие счета за 5 минут онлайн без визита в отделение.\n"
        "3. **Банк ЦентрКредит:** Идеально подходит для валютных переводов и работы с зарубежными контрагентами.\n\n"
        "Нажми на нужный банк, чтобы оставить заявку на официальном сайте:",
        parse_mode="Markdown",
        reply_markup=kb_offers,
    )
    await callback.answer()


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
