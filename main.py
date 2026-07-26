
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

questions = [
    {
        "question": "भारत की राजधानी क्या है?",
        "options": ["मुंबई", "दिल्ली", "जयपुर", "कोलकाता"],
        "answer": 1,
    },
    {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": 1,
    },
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📝 Start Test", callback_data="start_test")]]
    await update.message.reply_text(
        "स्वागत है!\nनीचे बटन दबाकर टेस्ट शुरू करें।",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_test":
        user_data[query.from_user.id] = {
            "score": 0,
            "current": 0
        }
        await send_question(query, context)

async def send_question(query, context):
    data = user_data[query.from_user.id]
    q = questions[data["current"]]

    keyboard = []
    for i, option in enumerate(q["options"]):
        keyboard.append(
            [InlineKeyboardButton(option, callback_data=f"ans_{i}")]
        )

    await query.message.reply_text(
        q["question"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = user_data[query.from_user.id]
    q = questions[data["current"]]

    choice = int(query.data.split("_")[1])

    if choice == q["answer"]:
        data["score"] += 1

    data["current"] += 1

    if data["current"] >= len(questions):
        await query.message.reply_text(
            f"✅ Test Complete!\n\nScore: {data['score']}/{len(questions)}"
        )
    else:
        await send_question(query, context)

TOKEN = os.getenv("BOT_TOKEN")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button, pattern="start_test"))
app.add_handler(CallbackQueryHandler(answer, pattern="ans_"))

app.run_polling()
