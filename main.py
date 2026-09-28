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
    KeyboardButton
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
        [KeyboardButton(text="ℹ️ О сервисе")]
    ],
    resize_keyboard=True
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
async def show_banks(message: Message):
    # Берем реферальные ссылки из переменных Railway
    url_alfa = os.getenv("URL_ALFA", "#")
    url_tbank = os.getenv("URL_TBANK", "#")

    banks_inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔴 Альфа-Банк — 6 бесплатных опций + РКО", url=url_alfa)],
            [InlineKeyboardButton(text="🟡 Т-Банк — Вывод до 1 млн ₽ + 4 мес 0 ₽", url=url_tbank)]
        ]
    )

    info_text = (
        "📊 **Топовые банки РФ для открытия счета и регистрации бизнеса:**\n\n"
        "🔴 **Альфа-Банк (6 бесплатных опций):**\n"
        "• **Бесплатная регистрация ИП/ООО:** без госпошлины, юристов и визита в ФНС (100% онлайн)\n"
        "• **Бесплатный расчетный счет:** 0 ₽ обслуживание + круглосуточные платежи\n"
        "• **Бесплатная онлайн-бухгалтерия:** отдельный счет под налоги (+ до 3% на остаток)\n"
        "• **До 300 000 ₽ бонусов:** подарки на рекламу и развитие бизнеса от партнеров\n"
        "• **Кэшбэк до 5%** за бизнес-расходы по карте + Индикатор риска (защита по 115-ФЗ)\n"
        "• **Торговый эквайринг:** бесплатная аренда терминалов\n\n"
        "🟡 **Т-Банк (Тинькофф Бизнес):**\n"
        "• **До 4 месяцев бесплатного обслуживания** с момента открытия счета\n"
        "• **Вывод на личные карты:** до 1 000 000 ₽/мес БЕЗ комиссии (на тарифе «Профессиональный»)\n"
        "• **Платежи и переводы:** 0 ₽ внутри Т-Банка 24/7 и платежи в налоговую бесплатно\n"
        "• **Овердрафт в 1-й день:** возможность получить кредитный лимит сразу после открытия РКО\n"
        "• **Бесплатное сопровождение по 115-ФЗ** + бесплатная онлайн-бухгалтерия\n"
        "• **До 500 000 ₽** на полезные сервисы партнеров\n\n"
        "👇 **Выберите банк для онлайн-подачи заявки:**"
    )

    await message.answer(info_text, reply_markup=banks_inline_kb, parse_mode="Markdown")

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