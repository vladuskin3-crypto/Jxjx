import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ======= КОНФИГ =======
BOT_TOKEN = "8901120783:AAHxSXhhpPk-BAsYRqiPAMKCdbICR9cCBzo"
ADMIN_IDS = [8562897889]  # Ваш Telegram ID
# ======================

logging.basicConfig(level=logging.INFO)

# === КОМАНДЫ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Рассылка", callback_data='broadcast')],
        [InlineKeyboardButton("👤 Мой ID", callback_data='myid')],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🍋 LEMON BOT ACTIVATED!\nВыбери действие:",
        reply_markup=reply_markup
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'myid':
        await query.edit_message_text(f"🆔 Твой ID: `{query.from_user.id}`", parse_mode='Markdown')
    elif data == 'help':
        await query.edit_message_text(
            "📖 Команды:\n"
            "/start - меню\n"
            "/echo <текст> - повторить\n"
            "/broadcast <текст> - рассылка (только админ)"
        )
    elif data == 'broadcast':
        if query.from_user.id not in ADMIN_IDS:
            await query.edit_message_text("⛔ Доступ только для админа!")
            return
        context.user_data['broadcast_mode'] = True
        await query.edit_message_text("📨 Введи текст для рассылки:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # === ЭХО ===
    if text.startswith('/echo '):
        await update.message.reply_text(text[6:])
        return

    # === РАССЫЛКА ===
    if context.user_data.get('broadcast_mode') and user.id in ADMIN_IDS:
        # Здесь логика рассылки по всем юзерам (хранить в БД)
        await update.message.reply_text("✅ Рассылка запущена (добавь свою БД)")
        context.user_data['broadcast_mode'] = False
        return

    # === ЭХО ДЛЯ ВСЕХ ОСТАЛЬНЫХ ===
    await update.message.reply_text(f"🔁 Эхо: {text}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🍋 LEMON BOT ЗАПУЩЕН!")
    app.run_polling()

if __name__ == "__main__":
    main()
