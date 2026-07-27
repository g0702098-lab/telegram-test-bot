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

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📝 Start Test", callback_data="start")]]
    await update.message.reply_text(
        "स्वागत है!\n\nनीचे बटन दबाकर टेस्ट शुरू करें।",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id

    if query.data == "start":
        users[uid] = {"index": 0, "score": 0}
        await send_question(query)

    elif query.data.startswith("ans_"):
        choice = int(query.data.split("_")[1])
        data = users[uid]
        q = questions[data["index"]]

        if choice == q["answer"]:
            data["score"] += 1

        data["index"] += 1

        if data["index"] >= len(questions):
            await query.edit_message_text(
                f"✅ Test Complete\n\nScore: {data['score']}/{len(questions)}"
            )
        else:
            await send_question(query)

async def send_question(query):
    uid = query.from_user.id
    data = users[uid]
    q = questions[data["index"]]

    keyboard = []

    for i, option in enumerate(q["options"]):
        keyboard.append(
            [InlineKeyboardButton(option, callback_data=f"ans_{i}")]
        )

    await query.edit_message_text(
        q["question"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

TOKEN = os.environ["BOT_TOKEN"]

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
