import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "8688224741:AAEd2BRTAc5Ccm0Olgn23BcIVubVD-hquyY")
OWNER = "miyrat11"  # Buyurtmalar keladigan Telegram username

# Mahsulotlar
mahsulotlar = [
    {"id": 1,  "nomi": "Ikat atlas",              "tur": "mato",    "narx": 35000,  "tarkib": "Paxta",    "eni": "1.5 m",  "tag": "new"},
    {"id": 2,  "nomi": "Qizil gul ipak",           "tur": "mato",    "narx": 40000,  "tarkib": "Ipak",     "eni": "1.5 m",  "tag": ""},
    {"id": 3,  "nomi": "Anor naqsh baxmal",        "tur": "mato",    "narx": 40000,  "tarkib": "Baxmal",   "eni": "1.5 m",  "tag": "new"},
    {"id": 4,  "nomi": "Limon print",              "tur": "mato",    "narx": 30000,  "tarkib": "Krep",     "eni": "1.5 m",  "tag": "sale"},
    {"id": 5,  "nomi": "Qora kostyum (klassik)",   "tur": "kostyum", "narx": 65000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": ""},
    {"id": 6,  "nomi": "Qora kostyum Classic",     "tur": "kostyum", "narx": 50000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": ""},
    {"id": 7,  "nomi": "Qora kostyum yaltiroq",    "tur": "kostyum", "narx": 50000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": ""},
    {"id": 8,  "nomi": "Ko'k kostyum",             "tur": "kostyum", "narx": 55000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": "new"},
    {"id": 9,  "nomi": "Qora kurtka (mo'ynali)",   "tur": "kurtka",  "narx": 120000, "tarkib": "Sintetik", "eni": "S-XXL",  "tag": "new"},
    {"id": 10, "nomi": "Qora kurtka (yengil)",     "tur": "kurtka",  "narx": 90000,  "tarkib": "Sintetik", "eni": "S-XXL",  "tag": ""},
    {"id": 11, "nomi": "Demix kurtka",             "tur": "kurtka",  "narx": 100000, "tarkib": "Sintetik", "eni": "S-XXL",  "tag": ""},
    {"id": 12, "nomi": "Kurtka (qo'shimcha)",      "tur": "kurtka",  "narx": 60000,  "tarkib": "Sintetik", "eni": "S-XXL",  "tag": "sale"},
    {"id": 13, "nomi": "Oq gul ro'mol",            "tur": "romol",   "narx": 15000,  "tarkib": "Shifon",   "eni": "90x90",  "tag": ""},
    {"id": 14, "nomi": "Gulли ro'mol (mix)",        "tur": "romol",   "narx": 15000,  "tarkib": "Shifon",   "eni": "90x90",  "tag": ""},
    {"id": 15, "nomi": "Qizil gul ro'mol",         "tur": "romol",   "narx": 10000,  "tarkib": "Shol",     "eni": "90x90",  "tag": "sale"},
    {"id": 16, "nomi": "Naqshli ro'mol",           "tur": "romol",   "narx": 10000,  "tarkib": "Shol",     "eni": "90x90",  "tag": "sale"},
    {"id": 17, "nomi": "Qora jempir (baxmal)",     "tur": "jempir",  "narx": 120000, "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 18, "nomi": "Oq jempir (Turkzar)",      "tur": "jempir",  "narx": 90000,  "tarkib": "Trikotaj", "eni": "S-XXL",  "tag": ""},
    {"id": 19, "nomi": "Qora chopon (zardo'zi)",   "tur": "chopon",  "narx": 40000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 20, "nomi": "Zangori chopon (zardo'zi)","tur": "chopon",  "narx": 45000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 21, "nomi": "Ko'k chopon (naqshli)",    "tur": "chopon",  "narx": 40000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 22, "nomi": "Qora jaket (naqshli)",     "tur": "jaket",   "narx": 120000, "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 23, "nomi": "Qora jaket (yengsiz)",     "tur": "jaket",   "narx": 90000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 24, "nomi": "Qiz jaketi (qizil)",       "tur": "jaket",   "narx": 90000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
]

# Conversation states
SELECTING_TUR, SELECTING_MAHSULOT, ENTERING_MIQDOR, ENTERING_ISM, ENTERING_TEL = range(5)

user_orders = {}  # Vaqtinchalik buyurtma saqlash

def get_turlar():
    return list(dict.fromkeys([m["tur"] for m in mahsulotlar]))

def tag_emoji(tag):
    if tag == "new": return " 🆕"
    if tag == "sale": return " 🔖"
    return ""

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    turlar = get_turlar()
    keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
    keyboard.append([InlineKeyboardButton("🛍️ Barchasi", callback_data="tur:barchasi")])
    await update.message.reply_text(
        "👋 Xush kelibsiz!\n\n🛍️ *Do'kon katalogi*\n\nQaysi toifani ko'rmoqchisiz?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_TUR

# Tur tanlandi
async def tur_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tur = query.data.split(":")[1]
    context.user_data["tur"] = tur

    if tur == "barchasi":
        list_ = mahsulotlar
    else:
        list_ = [m for m in mahsulotlar if m["tur"] == tur]

    keyboard = []
    for m in list_:
        label = f"{m['nomi']}{tag_emoji(m['tag'])} — {m['narx']:,} so'm"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"m:{m['id']}")])
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back:start")])

    await query.edit_message_text(
        f"📋 *{tur.capitalize()}* mahsulotlari:\n\nBirini tanlang:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_MAHSULOT

# Mahsulot tanlandi
async def mahsulot_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mid = int(query.data.split(":")[1])
    m = next((x for x in mahsulotlar if x["id"] == mid), None)
    if not m:
        return

    context.user_data["mahsulot"] = m
    tag_text = {"new": "🆕 Yangi", "sale": "🔖 Chegirma", "": ""}.get(m["tag"], "")

    text = (
        f"✅ *{m['nomi']}*\n\n"
        f"📁 Turi: {m['tur'].capitalize()}\n"
        f"🧵 Tarkib: {m['tarkib']}\n"
        f"📏 O'lchov: {m['eni']}\n"
        f"💰 Narxi: *{m['narx']:,} so'm*\n"
        + (f"🏷️ {tag_text}\n" if tag_text else "") +
        f"\nNecha dona/metr kerak?"
    )
    keyboard = [
        [InlineKeyboardButton("1", callback_data="miqdor:1"),
         InlineKeyboardButton("2", callback_data="miqdor:2"),
         InlineKeyboardButton("3", callback_data="miqdor:3")],
        [InlineKeyboardButton("4", callback_data="miqdor:4"),
         InlineKeyboardButton("5", callback_data="miqdor:5"),
         InlineKeyboardButton("Boshqa (yozing)", callback_data="miqdor:custom")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back:tur")]
    ]
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    return ENTERING_MIQDOR

# Miqdor
async def miqdor_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    val = query.data.split(":")[1]
    if val == "custom":
        await query.edit_message_text("✏️ Miqdorni yozing (raqam):")
        return ENTERING_MIQDOR
    context.user_data["miqdor"] = int(val)
    await query.edit_message_text("👤 Ismingizni yozing:")
    return ENTERING_ISM

async def miqdor_matn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        miqdor = float(update.message.text.strip())
        context.user_data["miqdor"] = miqdor
        await update.message.reply_text("👤 Ismingizni yozing:")
        return ENTERING_ISM
    except:
        await update.message.reply_text("❗ Iltimos, faqat raqam yozing:")
        return ENTERING_MIQDOR

# Ism
async def ism_kiritildi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text.strip()
    await update.message.reply_text("📞 Telefon raqamingizni yozing:")
    return ENTERING_TEL

# Telefon
async def tel_kiritildi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tel = update.message.text.strip()
    context.user_data["tel"] = tel
    m = context.user_data["mahsulot"]
    miqdor = context.user_data["miqdor"]
    ism = context.user_data["ism"]
    jami = m["narx"] * miqdor

    # Mijozga tasdiqlash
    await update.message.reply_text(
        f"✅ *Buyurtmangiz qabul qilindi!*\n\n"
        f"📦 {m['nomi']}\n"
        f"🔢 Miqdor: {miqdor}\n"
        f"💰 Jami: *{jami:,.0f} so'm*\n"
        f"👤 Ism: {ism}\n"
        f"📞 Tel: {tel}\n\n"
        f"Tez orada @{OWNER} siz bilan bog'lanadi! 🙏",
        parse_mode="Markdown"
    )

    # Do'konga xabar yuborish
    owner_text = (
        f"🔔 *Yangi buyurtma!*\n\n"
        f"📦 Mahsulot: {m['nomi']}\n"
        f"📁 Turi: {m['tur']}\n"
        f"🔢 Miqdor: {miqdor}\n"
        f"💰 Jami: {jami:,.0f} so'm\n"
        f"👤 Mijoz: {ism}\n"
        f"📞 Tel: {tel}\n"
        f"🆔 Telegram: @{update.effective_user.username or 'username yoq'}"
    )
    try:
        await context.bot.send_message(
            chat_id=f"@{OWNER}",
            text=owner_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Owner ga xabar yuborishda xato: {e}")

    # Yana buyurtma?
    keyboard = [[InlineKeyboardButton("🛍️ Yana buyurtma", callback_data="restart")]]
    await update.message.reply_text(
        "Yana buyurtma bermoqchimisiz?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ConversationHandler.END

# Orqaga
async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dest = query.data.split(":")[1]
    if dest == "start":
        turlar = get_turlar()
        keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
        keyboard.append([InlineKeyboardButton("🛍️ Barchasi", callback_data="tur:barchasi")])
        await query.edit_message_text(
            "🛍️ *Do'kon katalogi*\n\nQaysi toifani ko'rmoqchisiz?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SELECTING_TUR
    elif dest == "tur":
        tur = context.user_data.get("tur", "barchasi")
        if tur == "barchasi":
            list_ = mahsulotlar
        else:
            list_ = [m for m in mahsulotlar if m["tur"] == tur]
        keyboard = []
        for m in list_:
            label = f"{m['nomi']}{tag_emoji(m['tag'])} — {m['narx']:,} so'm"
            keyboard.append([InlineKeyboardButton(label, callback_data=f"m:{m['id']}")])
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back:start")])
        await query.edit_message_text(
            f"📋 Mahsulotlar:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SELECTING_MAHSULOT

# Restart
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    turlar = get_turlar()
    keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
    keyboard.append([InlineKeyboardButton("🛍️ Barchasi", callback_data="tur:barchasi")])
    await query.edit_message_text(
        "🛍️ *Do'kon katalogi*\n\nQaysi toifani ko'rmoqchisiz?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_TUR

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi. /start — qayta boshlash")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(restart, pattern="^restart$"),
        ],
        states={
            SELECTING_TUR: [
                CallbackQueryHandler(tur_tanlandi, pattern="^tur:"),
            ],
            SELECTING_MAHSULOT: [
                CallbackQueryHandler(mahsulot_tanlandi, pattern="^m:"),
                CallbackQueryHandler(back_handler, pattern="^back:"),
            ],
            ENTERING_MIQDOR: [
                CallbackQueryHandler(miqdor_tanlandi, pattern="^miqdor:"),
                CallbackQueryHandler(back_handler, pattern="^back:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, miqdor_matn),
            ],
            ENTERING_ISM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ism_kiritildi),
            ],
            ENTERING_TEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, tel_kiritildi),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    print("Bot ishga tushdi! ✅")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
