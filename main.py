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

file_ids = {
    "1":  "AgACAgIAAxkBAAMIafcGl-e6WoFqmgABA2woBjX1b87LAAJtFWsbbLi5S7hk8_EhcfpKAQADAgADeQADOwQ",
    "2":  "AgACAgIAAxkBAAMLafcGsGLnOO7HYK2QbW77HT94-3cAAm4VaxtsuLlL1yRfHUJNwa8BAAMCAAN5AAM7BA",
    "3":  "AgACAgIAAxkBAAMOafcGyYhVopk6k88N4qaPFUt55u4AAm8VaxtsuLlLNtk_XOES0mMBAAMCAAN5AAM7BA",
    "4":  "AgACAgIAAxkBAAMRafcG4kHaHQWZAQ7OpNMfgmtMMJcAAnAVaxtsuLlL-NGTmEAT1qMBAAMCAAN5AAM7BA",
    "5":  "AgACAgIAAxkBAAMUafcG9pfFJZXoBwWMOyI1zCeKhNUAAnEVaxtsuLlL0t3iq4_nNkIBAAMCAAN5AAM7BA",
    "6":  "AgACAgIAAxkBAAMXafcHEVYiVa5Avy7IEbYU86Y7yUQAAnIVaxtsuLlLCWyMX9l9G9wBAAMCAAN5AAM7BA",
    "7":  "AgACAgIAAxkBAAMaafcHLNRs-a9yIFn6YyPTF1zNHk8AAnMVaxtsuLlLp1zr9rmXu4YBAAMCAAN5AAM7BA",
    "8":  "AgACAgIAAxkBAAMdafcHSYPMH4jZ-JcWapgw-dP4rr4AAnUVaxtsuLlLGpEEtCoCNbABAAMCAAN5AAM7BA",
    "9":  "AgACAgIAAxkBAAMgafcHa4nqa0Uyiv7qHv56jNEi-lUAAnYVaxtsuLlLkl_OfI8zoRIBAAMCAAN5AAM7BA",
    "10": "AgACAgIAAxkBAAMjafcHhzSLeFrIXnb2GHa9zhJBSY4AAncVaxtsuLlLvgwGq1VFsY0BAAMCAAN5AAM7BA",
    "11": "AgACAgIAAxkBAAMmafcHoRfJOb948-qv2nWEtHoKe0sAAngVaxtsuLlLDEjXcDdFHcsBAAMCAAN5AAM7BA",
    "12": "AgACAgIAAxkBAAMEafcGZmNt8GzGI8at1GVPGadhvWAAAmwVaxtsuLlLM6c3cFe0mjABAAMCAAN5AAM7BA",
    "13": "AgACAgIAAxkBAAMwafcH6C1FywZhEvP3fZ5tGGN7KfsAAnkVaxtsuLlLMuSFFp7l2sYBAAMCAAN5AAM7BA",
    "14": "AgACAgIAAxkBAAMzafcH-6HwMLeR3aaSri-CCJLXvCAAAnoVaxtsuLlLYOpfSFrean8BAAMCAAN5AAM7BA",
    "15": "AgACAgIAAxkBAAM2afcIDnR3Xc2cd3PjjGVRcz5jwhAAAnsVaxtsuLlL9LvA9o1QqjsBAAMCAAN5AAM7BA",
    "16": "AgACAgIAAxkBAAM5afcIHqqGMTpLGeguj93bMimqyYIAAnwVaxtsuLlL4oVE-0O6IJ4BAAMCAAN5AAM7BA",
    "17": "AgACAgIAAxkBAAM8afcIMwLa8Nv0IIl3d3Me6Zh7o48AAn0VaxtsuLlLYGGEy2Y_0vMBAAMCAAN5AAM7BA",
    "18": "AgACAgIAAxkBAAM_afcIS3Z6pGVpf8UNZvTdTPYoeLUAAn4VaxtsuLlLErSEDgvgm4gBAAMCAAN5AAM7BA",
    "19": "AgACAgIAAxkBAANCafcIe0_WcuD5iiCY2_6l_3xpDWMAAoIVaxtsuLlLA8lRWVvgBAwBAAMCAAN5AAM7BA",
    "20": "AgACAgIAAxkBAANFafcIkqwzBQABAbxOJpjDsAABXWqa8QACgxVrG2y4uUtglcz8KyAjuQEAAwIAA3kAAzsE",
    "21": "AgACAgIAAxkBAANIafcIrfmmgJzO_xNbvyWEJaHt_rIAAoQVaxtsuLlLJWfr_e9EdlABAAMCAAN5AAM7BA",
    "22": "AgACAgIAAxkBAANLafcIvqLmE5ppu03mp4pLn04Y7BUAAoYVaxtsuLlL4U2MBbuIAYgBAAMCAAN5AAM7BA",
    "23": "AgACAgIAAxkBAANOafcIzo9byv4715g9VLTjJ7il8IcAAocVaxtsuLlLzMTscLB2jhIBAAMCAAN5AAM7BA",
    "24": "AgACAgIAAxkBAANRafcI3xhNk-Jy6_d6C1LCOAdjeWwAAokVaxtsuLlLURS-ZUeKcfkBAAMCAAN5AAM7BA",
}

tovarlar = [
    {"id": 1,  "Ati": "Qizil atlas",              "tur": "mato",    "Summasi": 35000,  "qurami": "Paxta",    "eni": "1.5 m",  "tag": "new"},
    {"id": 2,  "Ati": "Qizil gul jipek",           "tur": "mato",    "Summasi": 40000,  "qurami": "Jipek",     "eni": "1.5 m",  "tag": ""},
    {"id": 3,  "Ati": "Anar nagis bahali",       "tur": "mato",    "Summasi": 40000,  "qurami": "Baxmal",   "eni": "1.5 m",  "tag": "new"},
    {"id": 4,  "Ati": "Limon print",              "tur": "mato",    "Summasi": 30000,  "qurami": "qatti",     "eni": "1.5 m",  "tag": "sale"},
    {"id": 5,  "Ati": "Qara kostyum (klassik)",   "tur": "kostyum", "Summasi": 65000,  "qurami": "Gezleme",  "eni": "44-54",  "tag": ""},
    {"id": 6,  "Ati": "Qara kostyum (Classic)",     "tur": "kostyum", "Summasi": 50000,  "qurami": "Gezleme",  "eni": "44-54",  "tag": ""},
    {"id": 7,  "Ati": "Qara kostyum jaltiraq",    "tur": "kostyum", "Summasi": 50000,  "qurami": "Gezleme",  "eni": "44-54",  "tag": ""},
    {"id": 8,  "Ati": "Kok kostyum",              "tur": "kostyum", "Summasi": 55000,  "qurami": "Gezleme",  "eni": "44-54",  "tag": "new"},
    {"id": 9,  "Ati": "Qara kurtka (jagali)",     "tur": "kurtka",  "Summasi": 120000, "qurami": "Sintetik", "eni": "S-XXL",  "tag": "new"},
    {"id": 10, "Ati": "Qara kurtka (jengil)",     "tur": "kurtka",  "Summasi": 90000,  "qurami": "Sintetik", "eni": "S-XXL",  "tag": ""},
    {"id": 11, "Ati": "Demix kurtka",             "tur": "kurtka",  "Summasi": 100000, "qurami": "Sintetik", "eni": "S-XXL",  "tag": ""},
    {"id": 12, "Ati": "Kurtka (qosimsha)",        "tur": "kurtka",  "Summasi": 60000,  "qurami": "Sintetik", "eni": "S-XXL",  "tag": "sale"},
    {"id": 13, "Ati": "Aq gul oramal",            "tur": "oramal",  "Summasi": 15000,  "qurami": "Shifon",   "eni": "90x90",  "tag": ""},
    {"id": 14, "Ati": "Gullu oramal (mix)",       "tur": "oramal",  "Summasi": 15000,  "qurami": "Shifon",   "eni": "90x90",  "tag": ""},
    {"id": 15, "Ati": "Qizil gul oramal",         "tur": "oramal",  "Summasi": 10000,  "qurami": "Shal",     "eni": "90x90",  "tag": "sale"},
    {"id": 16, "Ati": "Naqishli oramal",          "tur": "oramal",  "Summasi": 10000,  "qurami": "Shal",     "eni": "90x90",  "tag": "sale"},
    {"id": 17, "Ati": "Qara jemper (baxmal)",     "tur": "jemper",  "Summasi": 120000, "qurami": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 18, "Ati": "Aq jemper (Turkzar)",      "tur": "jemper",  "Summasi": 90000,  "qurami": "Trikotaj", "eni": "S-XXL",  "tag": ""},
    {"id": 19, "Ati": "Qara shapan (zardozi)",    "tur": "shapan",  "Summasi": 40000,  "qurami": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 20, "Ati": "Kok shapan (zardozi)",     "tur": "shapan",  "Summasi": 45000,  "qurami": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 21, "Ati": "Kok shapan (naqishli)",    "tur": "shapan",  "Summasi": 40000,  "qurami": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 22, "Ati": "Qara jaket (naqishli)",    "tur": "jaket",   "Summasi": 120000, "qurami": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
    {"id": 23, "Ati": "Qara jaket (jengsiz)",     "tur": "jaket",   "Summasi": 90000,  "qurami": "Baxmal",   "eni": "S-XXL",  "tag": ""},
    {"id": 24, "Ati": "Qiz jaketi (qizil)",       "tur": "jaket",   "Summasi": 90000,  "qurami": "Baxmal",   "eni": "S-XXL",  "tag": "new"},
]

SELECTING_TUR, SELECTING_TOVAR, TOVAR_DETAIL, ENTERING_MIQDOR, ENTERING_ISM, ENTERING_TEL = range(6)

def get_turlar():
    return list(dict.fromkeys([t["tur"] for t in tovarlar]))

def tag_emoji(tag):
    if tag == "new": return " 🆕"
    if tag == "sale": return " 🔖"
    return ""

def tag_text_full(tag):
    if tag == "new": return "🆕 Jana tovar"
    if tag == "sale": return "🔖 Chegirma bar!"
    return ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    turlar = get_turlar()
    keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
    keyboard.append([InlineKeyboardButton("🛍️ Barligi", callback_data="tur:barligi")])
    await update.message.reply_text(
        "👋 Xosh kelipsiз!\n\n🛍️ *Qadelik zatlar uyi*\n\nQaysı turdi tanlaysiz?",
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
        label = f"{t['nomi']}{tag_emoji(t['tag'])}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"m:{t['id']}")])
    keyboard.append([InlineKeyboardButton("⬅️ Artqa", callback_data="back:start")])
    await query.edit_message_text(
        f"📋 *{tur.capitalize()}* tovarlari:\n\nKormekshi bolganinizdi tanlan 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_TOVAR

async def tovar_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tovar bosilganda — rasm + to'liq ma'lumot + Artqa/Zakaz tugmalari"""
    query = update.callback_query
    await query.answer()
    mid = int(query.data.split(":")[1])
    m = next((x for x in tovarlar if x["id"] == mid), None)
    if not m:
        return
    context.user_data["tovar"] = m

    tag = tag_text_full(m["tag"])
    caption = (
        f"🏷️ *{m['nomi']}*\n"
        f"{'━' * 20}\n"
        f"📁 Turi: {m['tur'].capitalize()}\n"
        f"🧵 Quramı: {m['tarkib']}\n"
        f"📏 Eni/Olshemi: {m['eni']}\n"
        f"💰 Bahası: *{m['narx']:,} som/metr*\n"
        + (f"✨ {tag}\n" if tag else "") +
        f"{'━' * 20}\n"
        f"Buyirpa bermekshisiz be?"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Zakaz berish", callback_data=f"zakaz:{m['id']}")],
        [InlineKeyboardButton("⬅️ Artqa", callback_data=f"back:tur")],
    ]
    fid = file_ids.get(str(m["id"]))
    if fid:
        await query.message.reply_photo(
            photo=fid,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        try:
            await query.message.delete()
        except:
            pass
    else:
        await query.edit_message_text(caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    return TOVAR_DETAIL

async def zakaz_boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    m = context.user_data.get("tovar")
    if not m:
        mid = int(query.data.split(":")[1])
        m = next((x for x in tovarlar if x["id"] == mid), None)
        context.user_data["tovar"] = m

    keyboard = [
        [InlineKeyboardButton("0.5", callback_data="miqdor:0.5"),
         InlineKeyboardButton("1", callback_data="miqdor:1"),
         InlineKeyboardButton("1.5", callback_data="miqdor:1.5")],
        [InlineKeyboardButton("2", callback_data="miqdor:2"),
         InlineKeyboardButton("3", callback_data="miqdor:3"),
         InlineKeyboardButton("5", callback_data="miqdor:5")],
        [InlineKeyboardButton("Basqasha (jazın)", callback_data="miqdor:custom")],
    ]
    await query.message.reply_text(
        f"📏 *{m['nomi']}*\n\nNeshe metr/dona kerek?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ENTERING_MIQDOR

async def miqdor_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    val = query.data.split(":")[1]
    if val == "custom":
        await query.message.reply_text("✏️ Sanın jazın (misali: 2.5):")
        return ENTERING_MIQDOR
    context.user_data["miqdor"] = float(val)
    await query.message.reply_text("👤 Atınızdı jazın:")
    return ENTERING_ISM

async def miqdor_matn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        miqdor = float(update.message.text.strip().replace(",", "."))
        context.user_data["miqdor"] = mugdari
        await update.message.reply_text("👤 Atınızdı jazın:")
        return ENTERING_ISM
    except:
        await update.message.reply_text("❗ Tek san jazın (misali: 2 yaki 1.5):")
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
    jami = m["narx"] * mugdar

    await update.message.reply_text(
        f"✅ *Buyirtpaniz qabıl etildi!*\n\n"
        f"🏷️ {m['nomi']}\n"
        f"📏 Sanı: {miqdor} metr\n"
        f"💰 Jami: *{jami:,.0f} som*\n"
        f"👤 Atı: {ism}\n"
        f"📞 Tel: {tel}\n\n"
        f"Tez arada @{OWNER} siz menen baylanisadi! 🙏",
        parse_mode="Markdown"
    )

    owner_text = (
        f"🔔 *Jana buyirtpa!*\n\n"
        f"🏷️ Tovar: {m['nomi']}\n"
        f"📁 Turi: {m['tur']}\n"
        f"🧵 Quramı: {m['tarkib']}\n"
        f"📏 Sanı: {miqdor} metr\n"
        f"💰 Jami: {jami:,.0f} som\n"
        f"👤 Qariydar: {ism}\n"
        f"📞 Tel: {tel}\n"
        f"🆔 TG: @{update.effective_user.username or 'joq'}"
    )
    try:
        await context.bot.send_message(chat_id=f"@{OWNER}", text=owner_text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Xate: {e}")

    keyboard = [
        [InlineKeyboardButton("🛍️ Jana buyirtpa", callback_data="restart")],
    ]
    await update.message.reply_text("Jańa buyirtpa bermekshizbe?", reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dest = query.data.split(":")[1]
    if dest == "start":
        turlar = get_turlar()
        keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
        keyboard.append([InlineKeyboardButton("🛍️ Barligi", callback_data="tur:barligi")])
        await query.message.reply_text(
            "🛍️ *Qadelik zatlar*\n\nQaysı turdi tanlaysiz?",
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SELECTING_TUR
    elif dest == "tur":
        tur = context.user_data.get("tur", "barligi")
        list_ = tovarlar if tur == "barligi" else [t for t in tovarlar if t["tur"] == tur]
        keyboard = []
        for t in list_:
            label = f"{t['nomi']}{tag_emoji(t['tag'])}"
            keyboard.append([InlineKeyboardButton(label, callback_data=f"m:{t['id']}")])
        keyboard.append([InlineKeyboardButton("⬅️ Artqa", callback_data="back:start")])
        await query.message.reply_text(
            f"📋 *{tur.capitalize()}* tovarlari:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SELECTING_TOVAR

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    turlar = get_turlar()
    keyboard = [[InlineKeyboardButton(f"📦 {t.capitalize()}", callback_data=f"tur:{t}")] for t in turlar]
    keyboard.append([InlineKeyboardButton("🛍️ Barligi", callback_data="tur:barligi")])
    await query.message.reply_text(
        "🛍️ *Qadelik zatlar*\n\nQaysı turdi tanlaysiz?",
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
            SELECTING_TOVAR: [
                CallbackQueryHandler(tovar_detail, pattern="^m:"),
                CallbackQueryHandler(back_handler, pattern="^back:"),
            ],
            TOVAR_DETAIL: [
                CallbackQueryHandler(zakaz_boshlash, pattern="^zakaz:"),
                CallbackQueryHandler(back_handler, pattern="^back:"),
            ],
            ENTERING_MIQDOR: [
                CallbackQueryHandler(miqdor_tanlandi, pattern="^miqdor:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, miqdor_matn),
            ],
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
