import os
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ⛔ قائمة كلمات ممنوعة
BANNED_WORDS = ["شتيمة1", "شتيمة2", "كلمةبذيئة"]

# 🟢 أوامر إدارية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال لحماية الجروب!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤖 أوامر البوت:
- /help : عرض هذه القائمة
- /warn : تحذير عضو
- /mute : كتم عضو 5 دقائق
- /ban  : حظر عضو
- /pin  : تثبيت رسالة
""")

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.message.reply_to_message.reply_text("⚠️ تم تحذيرك! يرجى الالتزام بالقوانين.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            update.message.reply_to_message.from_user.id,
            ChatPermissions(can_send_messages=False),
            until_date=None
        )
        await update.message.reply_to_message.reply_text("🔇 تم كتمك 5 دقائق.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(
            update.effective_chat.id,
            update.message.reply_to_message.from_user.id
        )
        await update.message.reply_text("🚫 تم حظر العضو من الجروب.")

async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await context.bot.pin_chat_message(update.effective_chat.id, update.message.reply_to_message.id)
        await update.message.reply_text("📌 تم تثبيت الرسالة.")

# 🛡️ فلتر الرسائل (منع روابط + سبام + كلمات ممنوعة)
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # حذف الروابط
    if "http://" in text or "https://" in text or "t.me" in text:
        await update.message.delete()
        return

    # حذف الكلمات الممنوعة
    for word in BANNED_WORDS:
        if word in text:
            await update.message.delete()
            return

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("pin", pin))

    # فلتر
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
