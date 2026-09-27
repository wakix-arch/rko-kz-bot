import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from dotenv import load_dotenv

# Загружаем переменные из .env (для локального тестирования)
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Ошибка: Переменная BOT_TOKEN не найдена!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Главное меню (Главное меню с кнопками снизу)
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💼 Подбор РКО и Регистрация бизнеса (РФ)")],
        [KeyboardButton(text="ℹ️ О сервисе")],
    ],
    resize_keyboard=True,
)


# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        f"👋 Здравствуйте, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в сервис подбора банковских услуг для бизнеса в РФ.\n\n"
        "Мы помогаем бесплатно зарегистрировать ИП/ООО без походов в налоговую, "
        "а также подобрать выгодные условия расчетно-кассового обслуживания (РКО).\n\n"
        "Нажмите кнопку ниже, чтобы посмотреть предложения от ведущих банков!"
    )
    await message.answer(welcome_text, reply_markup=main_kb)


# Хэндлер на кнопку подбора банков
@router.message(F.text == "💼 Подбор РКО и Регистрация бизнеса (РФ)")
async def show_banks(message: Message):
    # Динамически получаем ссылки из переменных окружения
    url_vtb = os.getenv("URL_VTB_REG", "#")
    url_alfa = os.getenv("URL_ALFA_REG", "#")
    url_tbank = os.getenv("URL_TBANK", "#")

    # Инлайн-клавиатура со ссылками на банки
    banks_inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔵 ВТБ — Регистрация ИП/ООО + Переводы 0 ₽", url=url_vtb
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 Альфа-Банк — Регистрация бизнеса + 300к бонусов",
                    url=url_alfa,
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟡 Т-Банк — РКО (до 4 мес. 0 ₽ и бухгалтер)", url=url_tbank
                )
            ],
        ]
    )

    info_text = (
        "📊 **Топовые предложения от банков РФ для бизнеса:**\n\n"
        "🔵 **ВТБ (Регистрация бизнеса + РКО):**\n"
        "• 0 ₽ за регистрацию ИП/ООО без госпошлины и визитов в ФНС\n"
        "• **Для ИП:** Переводы на свою карту физлица — **без лимитов и комиссий!**\n"
        "• Обслуживание счета — до 12 месяцев за 0 ₽\n"
        "• Бесплатная КЭП (электронная подпись) при открытии\n\n"
        "🔴 **Альфа-Банк (Регистрация бизнеса + РКО):**\n"
        "• Онлайн-подача за 15 минут, без юристов и госпошлин\n"
        "• Бесплатное открытие счета + онлайн-бухгалтерия\n"
        "• До 300 000 ₽ бонусов от партнеров на развитие бизнеса\n\n"
        "🟡 **Т-Банк Бизнес (РКО для действующего бизнеса):**\n"
        "• До 4 месяцев бесплатного обслуживания\n"
        "• Бесплатная онлайн-бухгалтерия и выводы на карты физлица до 1 000 000 ₽\n\n"
        "👇 **Выберите банк для быстрого оформления заявки:**"
    )

    await message.answer(info_text, reply_markup=banks_inline_kb, parse_mode="Markdown")


# Хэндлер на кнопку "О сервисе"
@router.message(F.text == "ℹ️ О сервисе")
async def show_about(message: Message):
    about_text = (
        "ℹ️ **О нашем сервисе:**\n\n"
        "Наш бот — независимый бесплатный агрегатор банковских продуктов для предпринимателей.\n\n"
        "Все заявки подаются напрямую на официальных защищенных сайтах лицензированных банков РФ. "
        "Мы не собираем и не храним ваши персональные данные."
    )
    await message.answer(about_text)


# Запуск бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
