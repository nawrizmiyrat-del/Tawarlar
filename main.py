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
OWNER = "miyrat11"

tovarlar = [
    {"id": 1,  "nomi": "Ikat atlas",              "tur": "mato",    "narx": 35000,  "tarkib": "Paxta",    "eni": "1.5 m",  "tag": "new"},
    {"id": 2,  "nomi": "Qizil gul ipek",           "tur": "mato",    "narx": 40000,  "tarkib": "Ipek",     "eni": "1.5 m",  "tag": ""},
    {"id": 3,  "nomi": "Anar naqish baxmal",       "tur": "mato",    "narx": 40000,  "tarkib": "Baxmal",   "eni": "1.5 m",  "tag": "new"},
    {"id": 4,  "nomi": "Limon print",              "tur": "mato",    "narx": 30000,  "tarkib": "Krep",     "eni": "1.5 m",  "tag": "sale"},
    {"id": 5,  "nomi": "Qara kostyum (klassik)",   "tur": "kostyum", "narx": 65000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": ""},
    {"id": 6,  "nomi": "Qara kostyum Classic",     "tur": "kostyum", "narx": 50000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": ""},
    {"id": 7,  "nomi": "Qara kostyum jaltiraq",    "tur": "kostyum", "narx": 50000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": ""},
    {"id": 8,  "nomi": "Kok kostyum",              "tur": "kostyum", "narx": 55000,  "tarkib": "Gazlama",  "eni": "44-54",  "tag": "new"},
    {"id": 9,  "nomi": "Qara kurtka (morali)",     "tur": "kurtka",  "narx": 120000, "tarkib": "Sintetik", "eni": "S-XXL",  "tag": "new"},
    {"id": 10, "nomi": "Qara kurtka (jengil)",     "tur": "kurtka",  "narx": 90000,  "tarkib": "Sintetik", "eni": "S-XXL",  "tag": ""},
    {"id": 11, "nomi": "Demix kurtka",             "tur": "kurtka",  "narx": 100000, "tarkib": "Sintetik", "eni": "S-XXL",  "tag": ""},
    {"id": 12, "nomi": "Kurtka (qosimsha)",        "tur": "kurtka",  "narx": 60000,  "tarkib": "Sintetik", "eni": "S-XXL",  "tag": "sale"},
    {"id": 13, "nomi": "Aq gul oramal",            "tur": "oramal",  "narx": 15000,  "tarkib": "Shifon",   "eni": "90x90",  "tag": ""},
    {"id": 14, "nomi": "Gullu oramal (mix)",       "tur": "oramal",  "narx": 15000,  "tarkib": "Shifon",   "eni": "90x90",  "tag": ""},
    {"id": 15, "nomi": "Qizil gul oramal",         "tur": "oramal",  "narx": 10000,  "tarkib": "Shal",     "eni": "90x90",  "tag": "sale"},
    {"id": 16, "nomi": "Naqishli oramal",          "tur": "oramal",  "narx": 10000,  "tarkib": "Shal",     "eni": "90x90",  "tag": "sale"},
    {"id": 17, "nomi": "Qara jemper (baxmal)",     "tur": "jemper",  "narx": 120000, "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 18, "nomi": "Aq jemper (Turkzar)",      "tur": "jemper",  "narx": 90000,  "tarkib": "Trikotaj", "eni": "S-XXL",  "tag": ""},
    {"id": 19, "nomi": "Qara shapan (zardozi)",    "tur": "shapan",  "narx": 40000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 20, "nomi": "Kok shapan (zardozi)",     "tur": "shapan",  "narx": 45000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 21, "nomi": "Kok shapan (naqishli)",    "tur": "shapan",  "narx": 40000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 22, "nomi": "Qara jaket (naqishli)",    "tur": "jaket",   "narx": 120000, "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 23, "nomi": "Qara jaket (jengsiz)",     "tur": "jaket",   "narx": 90000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 24, "nomi": "Qiz jaketi (qizil)",       "tur": "jaket",   "narx": 90000,  "tarkib": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
]

SELECTING_TUR, SELECTING_TOVAR, ENTERING_MIQDOR, ENTERING_ISM, ENTERING_TEL = range(5)

def get_turlar():
    return list(dict.fromkeys([t["tur"] for t in tovarlar]))

def tag_emoji(tag):
    if tag == "new": return " 🆕"
    if tag == "sale": return " 🔖"
    return ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    turlar = get_turlar()
    keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
    keyboard.append([InlineKeyboardButton("🛍️ Barligi", callback_data="tur:barligi")])
    await update.message.reply_text(
        "👋 Xosh kelipsiз!\n\n🛍️ *Dukan kataloги*\n\nQaysı turdi tanlaysiz?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_TUR

async def tur_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tur = query.data.split(":")[1]
    context.user_data["tur"] = tur
    list_ = tovarlar if tur == "barligi" else [t for t in tovarlar if t["tur"] == tur]
    keyboard = []
    for t in list_:
        label = f"{t['nomi']}{tag_emoji(t['tag'])} — {t['narx']:,} som"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"m:{t['id']}")])
    keyboard.append([InlineKeyboardButton("⬅️ Artqa", callback_data="back:start")])
    await query.edit_message_text(
        f"📋 *{tur.capitalize()}* tovarlari:\n\nBirin tanlang:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_TOVAR

async def tovar_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mid = int(query.data.split(":")[1])
    m = next((x for x in tovarlar if x["id"] == mid), None)
    if not m:
        return
    context.user_data["tovar"] = m
    tag_text = {"new": "🆕 Jana", "sale": "🔖 Chegirma", "": ""}.get(m["tag"], "")
    text = (
        f"✅ *{m['nomi']}*\n\n"
        f"📁 Turi: {m['tur'].capitalize()}\n"
        f"🧵 Quramı: {m['tarkib']}\n"
        f"📏 Olshemi: {m['eni']}\n"
        f"💰 Bahası: *{m['narx']:,} som*\n"
        + (f"🏷️ {tag_text}\n" if tag_text else "") +
        f"\nNeshe dona/metr kerek?"
    )
    keyboard = [
        [InlineKeyboardButton("1", callback_data="miqdor:1"),
         InlineKeyboardButton("2", callback_data="miqdor:2"),
         InlineKeyboardButton("3", callback_data="miqdor:3")],
        [InlineKeyboardButton("4", callback_data="miqdor:4"),
         InlineKeyboardButton("5", callback_data="miqdor:5"),
         InlineKeyboardButton("Basqasha (jazın)", callback_data="miqdor:custom")],
        [InlineKeyboardButton("⬅️ Artqa", callback_data="back:tur")]
    ]
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    return ENTERING_MIQDOR

async def miqdor_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    val = query.data.split(":")[1]
    if val == "custom":
        await query.edit_message_text("✏️ Sanın jazın (san):")
        return ENTERING_MIQDOR
    context.user_data["miqdor"] = int(val)
    await query.edit_message_text("👤 Atınızdı jazın:")
    return ENTERING_ISM

async def miqdor_matn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        miqdor = float(update.message.text.strip())
        context.user_data["miqdor"] = miqdor
        await update.message.reply_text("👤 Atınızdı jazın:")
        return ENTERING_ISM
    except:
        await update.message.reply_text("❗ Tek san jazın:")
        return ENTERING_MIQDOR

async def ism_kiritildi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text.strip()
    await update.message.reply_text("📞 Telefon nomerińizdı jazın:")
    return ENTERING_TEL

async def tel_kiritildi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tel = update.message.text.strip()
    context.user_data["tel"] = tel
    m = context.user_data["tovar"]
    miqdor = context.user_data["miqdor"]
    ism = context.user_data["ism"]
    jami = m["narx"] * miqdor
    await update.message.reply_text(
        f"✅ *Siparısınız qabıl etildi!*\n\n"
        f"📦 {m['nomi']}\n"
        f"🔢 Sanı: {miqdor}\n"
        f"💰 Jemi: *{jami:,.0f} som*\n"
        f"👤 Atı: {ism}\n"
        f"📞 Tel: {tel}\n\n"
        f"Tez arada @{OWNER} siz menen baylanisadi! 🙏",
        parse_mode="Markdown"
    )
    owner_text = (
        f"🔔 *Jana siparıs!*\n\n"
        f"📦 Tovar: {m['nomi']}\n"
        f"📁 Turi: {m['tur']}\n"
        f"🔢 Sanı: {miqdor}\n"
        f"💰 Jemi: {jami:,.0f} som\n"
        f"👤 Mijoz: {ism}\n"
        f"📞 Tel: {tel}\n"
        f"🆔 Telegram: @{update.effective_user.username or 'username joq'}"
    )
    try:
        await context.bot.send_message(chat_id=f"@{OWNER}", text=owner_text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Xato: {e}")
    keyboard = [[InlineKeyboardButton("🛍️ Jana siparıs", callback_data="restart")]]
    await update.message.reply_text("Jana siparıs bermoqchimisiz?", reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dest = query.data.split(":")[1]
    if dest == "start":
        turlar = get_turlar()
        keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
        keyboard.append([InlineKeyboardButton("🛍️ Barligi", callback_data="tur:barligi")])
        await query.edit_message_text(
            "🛍️ *Dukan kataloги*\n\nQaysı turdi tanlaysiz?",
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SELECTING_TUR
    elif dest == "tur":
        tur = context.user_data.get("tur", "barligi")
        list_ = tovarlar if tur == "barligi" else [t for t in tovarlar if t["tur"] == tur]
        keyboard = []
        for t in list_:
            label = f"{t['nomi']}{tag_emoji(t['tag'])} — {t['narx']:,} som"
            keyboard.append([InlineKeyboardButton(label, callback_data=f"m:{t['id']}")])
        keyboard.append([InlineKeyboardButton("⬅️ Artqa", callback_data="back:start")])
        await query.edit_message_text("📋 Tovarlar:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SELECTING_TOVAR

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    turlar = get_turlar()
    keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
    keyboard.append([InlineKeyboardButton("🛍️ Barligi", callback_data="tur:barligi")])
    await query.edit_message_text(
        "🛍️ *Dukan kataloги*\n\nQaysı turdi tanlaysiz?",
        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_TUR

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Toqtatıldı. /start — qayta baslaw")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(restart, pattern="^restart$")],
        states={
            SELECTING_TUR: [CallbackQueryHandler(tur_tanlandi, pattern="^tur:")],
            SELECTING_TOVAR: [CallbackQueryHandler(tovar_tanlandi, pattern="^m:"), CallbackQueryHandler(back_handler, pattern="^back:")],
            ENTERING_MIQDOR: [CallbackQueryHandler(miqdor_tanlandi, pattern="^miqdor:"), CallbackQueryHandler(back_handler, pattern="^back:"), MessageHandler(filters.TEXT & ~filters.COMMAND, miqdor_matn)],
            ENTERING_ISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_kiritildi)],
            ENTERING_TEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, tel_kiritildi)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv)
    print("Bot islep turıptı! ✅")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
