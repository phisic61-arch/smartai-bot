from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import requests
import random

# =========================
# CONFIG PERSONNELLE
# =========================
TOKEN = "8504267456:AAFUuKOfl-Xz_NacvnQDDypHAVRxe9A0mw0"

ADS_LINKS = [
    "https://www.effectivegatecpm.com/cmss63xi?key=3e8a3ba7448ab5cfaa942be32f0b5b87",
    "https://otieu.com/4/10231671"
]

AI_API = "https://api.affiliateplus.xyz/api/chatbot"
# =========================


def get_random_ads():
    return random.choice(ADS_LINKS)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🤖 *SmartAI Bot 2025*\n\n"
    msg += "✅ Français | English | عربي\n"
    msg += "🔥 IA 100% gratuite\n\n"
    msg += "🔓 Clique ici pour activer l’IA :\n"
    msg += get_random_ads()
    await update.message.reply_text(msg, parse_mode="Markdown")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    ads_msg = f"✅ Clique ici pour continuer :\n{get_random_ads()}\n\n"
    await update.message.reply_text(ads_msg)

    r = requests.get(AI_API, params={
        "message": user_text,
        "botname": "SmartAI",
        "ownername": "SmartAI Bot 2025"
    })

    try:
        data = r.json()
        answer = data.get("message", "❌ Erreur IA, réessaie.")
    except:
        answer = "❌ Erreur serveur, réessaie."

    await update.message.reply_text(answer)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
