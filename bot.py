import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# =========================
TOKEN = "8504267456:AAFUuKOfl-Xz_NacvnQDDypHAVRxe9A0mw0"
OPENROUTER_API_KEY = "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"
PUB_LINK = "https://www.effectivegatecpm.com/cmss63xi?key=3e8a3ba7448ab5cfaa942be32f0b5b87"
# =========================

users_count = {}

# ----- /start -----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔓 Activer l’IA", url=PUB_LINK)],
        [
            InlineKeyboardButton("🇫🇷 Français", callback_data="fr"),
            InlineKeyboardButton("🇬🇧 English", callback_data="en"),
            InlineKeyboardButton("🇸🇦 عربي", callback_data="ar")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🤖 SmartAI Bot 2025\n\n"
        "✅ Français | English | العربية\n"
        "🔥 Intelligence Artificielle réelle\n\n"
        "👇 Active l’IA ici :"
    )

    await update.message.reply_text(text, reply_markup=reply_markup)

# ----- Langue -----
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data

    messages = {
        "fr": "✅ Langue définie en Français.\nPose ta question.",
        "en": "✅ Language set to English.\nAsk your question.",
        "ar": "✅ تم تعيين اللغة العربية.\nاكتب سؤالك."
    }

    context.user_data["lang"] = lang
    await query.edit_message_text(messages[lang])

# ----- Appel IA réel -----
def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=60
    )

    result = r.json()
    return result["choices"][0]["message"]["content"]

# ----- IA + PUB -----
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users_count[user_id] = users_count.get(user_id, 0) + 1
    count = users_count[user_id]

    user_text = update.message.text

    try:
        ai_response = ask_ai(user_text)
    except:
        ai_response = "⚠️ Erreur IA temporaire. Réessaie."

    # Pub toutes les 5 utilisations
    if count % 5 == 0:
        ai_response += f"\n\n🔓 Active toutes les fonctions ici :\n{PUB_LINK}"

    await update.message.reply_text(ai_response)

# ----- LANCEMENT -----
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(set_language))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))

app.run_polling()
