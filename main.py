from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome!\n\n"
        "यह Basic Test Bot है.\n"
        "जल्द ही इसमें टेस्ट जोड़े जाएंगे।"
    )

app = Application.builder().token("YOUR_BOT_TOKEN").build()

app.add_handler(CommandHandler("start", start))

print("Bot Started...")
app.run_polling()
