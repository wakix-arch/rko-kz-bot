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

# Загружаем переменные окружения
load_dotenv()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Главная клавиатура под чатом
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💼 Подобрать банк под РКО (РФ)")],
        [KeyboardButton(text="ℹ️ О сервисе")],
    ],
    resize_keyboard=True,
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        f"👋 Здравствуйте, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в независимый ассистент по подбору банковских услуг для бизнеса в РФ.\n\n"
        "Мы помогаем бесплатно зарегистрировать ИП/ООО без похода в налоговую, "
        "а также подобрать выгодные условия расчетно-кассового обслуживания (РКО)."
    )
    await message.answer(welcome_text, reply_markup=main_kb)


@router.message(F.text == "💼 Подобрать банк под РКО (РФ)")
@router.message(F.text == "💼 Подобрать банк под РКО (РФ)")
async def show_banks(message: Message):
    # Если переменная не найдена в Railway, ставим рабочий URL-заглушку вместо '#'
    url_alfa = os.getenv("URL_ALFA") if os.getenv("URL_ALFA") else "https://alfabank.ru"
    url_tbank = os.getenv("URL_TBANK") if os.getenv("URL_TBANK") else "https://tbank.ru"

    banks_inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔴 Альфа-Банк — 6 бесплатных опций + РКО", url=url_alfa
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟡 Т-Банк — Вывод до 1 млн ₽ + 4 мес 0 ₽", url=url_tbank
                )
            ],
        ]
    )

    info_text = (
        "📊 <b>Топовые банки РФ для открытия счета и регистрации бизнеса:</b>\n\n"
        "🔴 <b>Альфа-Банк (6 бесплатных опций):</b>\n"
        "• <b>Бесплатная регистрация ИП/ООО:</b> без госпошлины, юристов и визита в ФНС\n"
        "• <b>Бесплатный расчетный счет:</b> 0 ₽ обслуживание + круглосуточные платежи\n"
        "• <b>Бесплатная онлайн-бухгалтерия:</b> отдельный счет под налоги\n"
        "• <b>До 300 000 ₽ бонусов:</b> подарки на рекламу и развитие бизнеса\n"
        "• <b>Кэшбэк до 5%</b> за бизнес-расходы + Индикатор риска (115-ФЗ)\n"
        "• <b>Торговый эквайринг:</b> бесплатная аренда терминалов\n\n"
        "🟡 <b>Т-Банк (Тинькофф Бизнес):</b>\n"
        "• <b>До 4 месяцев бесплатного обслуживания</b> с момента открытия счета\n"
        "• <b>Вывод на личные карты:</b> до 1 000 000 ₽/мес БЕЗ комиссии\n"
        "• <b>Платежи и переводы:</b> 0 ₽ внутри Т-Банка 24/7\n"
        "• <b>Овердрафт в 1-й день:</b> кредитный лимит сразу после открытия РКО\n"
        "• <b>Бесплатное сопровождение по 115-ФЗ</b> + онлайн-бухгалтерия\n"
        "• <b>До 500 000 ₽</b> на полезные сервисы партнеров\n\n"
        "👇 <b>Выберите банк для онлайн-подачи заявки:</b>"
    )

    await message.answer(info_text, reply_markup=banks_inline_kb, parse_mode="HTML")


@router.message(F.text == "ℹ️ О сервисе")
async def show_about(message: Message):
    about_text = (
        "ℹ️ **О сервисе:**\n\n"
        "Наш бот — бесплатный информационный ассистент по подбору продуктов для бизнеса.\n\n"
        "Сервис не является финансовой организацией, не собирает персональные данные "
        "и перенаправляет пользователей на официальные страницы партнерских программ банков РФ."
    )
    await message.answer(about_text)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
