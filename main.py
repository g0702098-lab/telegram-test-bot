uimport os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# क्विज़ के प्रश्न और विकल्प
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
        await send_question(query, context)

    elif query.data.startswith("ans_"):
        choice = int(query.data.split("_")[1])
        
        # सुरक्षा के लिए चेक करें कि यूजर डिक्शनरी में है या नहीं
        if uid not in users:
            await query.edit_message_text("❌ सत्र (Session) समाप्त हो गया है। कृपया /start टाइप करें।")
            return

        data = users[uid]
        q = questions[data["index"]]

        if choice == q["answer"]:
            data["score"] += 1

        data["index"] += 1

        if data["index"] >= len(questions):
            await query.edit_message_text(
                f"✅ Test Complete!\n\nआपका स्कोर: {data['score']}/{len(questions)}"
            )
            # टेस्ट खत्म होने पर यूजर को डेटा से हटा सकते हैं
            del users[uid]
        else:
            await send_question(query, context)

async def send_question(query, context):
    uid = query.from_user.id
    data = users[uid]
    q = questions[data["index"]]

    keyboard = []
    for i, option in enumerate(q["options"]):
        keyboard.append(
            [InlineKeyboardButton(option, callback_data=f"ans_{i}")]
        )

    await query.edit_message_text(
        text=q["question"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

def main():
    # अपना बोट टोकन यहाँ डायरेक्ट भी डाल सकते हैं अगर एनवायरनमेंट वेरिएबल सेट नहीं है
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable not set!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
