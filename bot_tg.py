import sys

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from analylics import create_analytics
from bd.bd_querys import get_list_of_subscriptions, subscribe, is_subscribed_to, unsubcribe, register_user, \
    register_company, is_compony_registred
import json

TOKEN = "8063531205:AAE43NNubnQEcMyaU5WWrHtKHca2lAF9X9M"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await register_user(update.effective_chat.id)
    keyboard = [
        ["Подписки"],
        ["Найти компанию"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    print()


async def subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
    ]
    chat_id = update.effective_chat.id
    lst = await get_list_of_subscriptions(chat_id)
    for i, j in lst:
        keyboard.append([InlineKeyboardButton(j, callback_data=f"get_{i}")])

    await update.message.reply_text(
        "Подписки",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    print()


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "kill":
        sys.exit(0)
    if text.lower() == "подписки":
        await subscriptions(update, context)
    elif text.lower() == "найти компанию":
        await update.message.reply_text("Отправьте тикер компании")
    elif await is_compony_registred(text.upper()):
        await send_graphic(update, context, [text])
    else:
        await update.message.reply_text(f"Компания не найдена {text}")
    print()


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print(query)
    method, *parametr = query.data.split("_")
    if method == "get":
        await send_graphic(update, context, parametr)
    elif method == "unsub":
        chat_id, ticker = parametr
        if await unsubcribe(chat_id, ticker):
            await context.bot.send_message(chat_id, "Подписка отменена")
        else:
            await update.message.reply_text("Что-то пошло не так")
    elif method == "sub":
        chat_id, ticker = parametr
        if await subscribe(chat_id, ticker):
            await context.bot.send_message(chat_id, "Подписка успешна")
        else:
            await update.message.reply_text("Что-то пошло не так")
    else:
        await update.message.reply_text("Что-то пошло не так")
    print()


async def send_graphic(update: Update, context: ContextTypes.DEFAULT_TYPE, param):

    chat_id = update.effective_chat.id
    ticker = param[0].upper()
    print(f"Запрос теханализа {ticker}")
    if not await is_subscribed_to(chat_id, ticker):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Подписаться", callback_data=f"sub_{chat_id}_{ticker}")]])
    else:
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Отписаться", callback_data=f"unsub_{chat_id}_{ticker}")]])
    if await is_compony_registred(ticker):
        if create_analytics(ticker):
            with open(f"data/{ticker}/{ticker}_info", encoding="utf-8") as f:
                d = json.load(f)
            text = d.get("analytics", "Ошибка прогноза")
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=open(f"data/{ticker}/{ticker}.png", 'rb'),  # Открываем файл в бинарном режиме
                caption=text,  # Подпись к фото (необязательно)
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text("Случился случай")
    else:
        await update.message.reply_text("Случился случай")
    print()


def setup():
    """Запуск бота"""
    # Создаем Application
    print("setuping bot")
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("Подписки", subscriptions))
    application.add_handler(CallbackQueryHandler(handle_button))
    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("bot started")
    # Запускаем бота
    application.run_polling()
    print()


def main() -> None:
    setup()


if __name__ == '__main__':
    main()
