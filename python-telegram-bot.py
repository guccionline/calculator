import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load .env file jika ada (untuk development lokal)
if os.path.exists('.env'):
    load_dotenv()

# Token bot dari environment variable (Railway atau lokal)
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Validasi token
if not TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN tidak ditemukan! Set di Railway Variables atau .env file")

# Setup logging biar kita tau kalau ada yang fucked up
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🤖 *Selamat Datang di Bot!*\n\nPilih menu di bawah:"
    await update.message.reply_text(text, reply_markup=main_menu(), parse_mode="Markdown")

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🧮 Kalkulator", callback_data="calc")],
        [InlineKeyboardButton("❓ Tentang Bot", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)

def calculator_keyboard():
    # Susunan tombol biar mirip kalkulator beneran dengan emoji
    keyboard = [
        [InlineKeyboardButton("C", callback_data="clear"), InlineKeyboardButton("⬅️ DEL", callback_data="del"), InlineKeyboardButton("➗", callback_data="/")],
        [InlineKeyboardButton("7️⃣", callback_data="7"), InlineKeyboardButton("8️⃣", callback_data="8"), InlineKeyboardButton("9️⃣", callback_data="9"), InlineKeyboardButton("✖️", callback_data="*")],
        [InlineKeyboardButton("4️⃣", callback_data="4"), InlineKeyboardButton("5️⃣", callback_data="5"), InlineKeyboardButton("6️⃣", callback_data="6"), InlineKeyboardButton("➖", callback_data="-")],
        [InlineKeyboardButton("1️⃣", callback_data="1"), InlineKeyboardButton("2️⃣", callback_data="2"), InlineKeyboardButton("3️⃣", callback_data="3"), InlineKeyboardButton("➕", callback_data="+")],
        [InlineKeyboardButton("0️⃣", callback_data="0"), InlineKeyboardButton(".", callback_data="."), InlineKeyboardButton("=", callback_data="=")],
        [InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    # Menu utama
    if data == "calc":
        await query.edit_message_text(
            text="🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: 0",
            reply_markup=calculator_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    if data == "about":
        about_text = "ℹ️ *Tentang Bot*\n\n🤖 Bot Kalkulator V\nBuat hitung-hitungan dengan mudah!\n\n/start - Kembali ke menu"
        await query.edit_message_text(text=about_text, reply_markup=main_menu(), parse_mode="Markdown")
        return
    
    if data == "menu":
        await query.edit_message_text(
            text="🤖 *Selamat Datang di Bot!*\n\nPilih menu di bawah:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        return
    
    # Kalkulator logic
    message_text = query.message.text
    if "Display:" in message_text:
        current_text = message_text.split("Display: ")[-1].strip()
    else:
        current_text = "0"
    
    if current_text == "0" and data not in [".", "="]:
        current_text = ""

    if data == "=":
        try:
            result = str(eval(current_text))
            display_text = f"🧮 *Kalkulator*\n━━━━━━━━━━━\n📊 Hasil: {result}"
            await query.edit_message_text(
                text=display_text,
                reply_markup=calculator_keyboard(),
                parse_mode="Markdown"
            )
        except:
            await query.edit_message_text(
                text="🧮 *Kalkulator*\n━━━━━━━━━━━\n❌ Error! Input tidak valid.",
                reply_markup=calculator_keyboard(),
                parse_mode="Markdown"
            )
    elif data == "clear":
        await query.edit_message_text(
            text="🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: 0",
            reply_markup=calculator_keyboard(),
            parse_mode="Markdown"
        )
    elif data == "del":
        new_text = current_text[:-1] if current_text else "0"
        await query.edit_message_text(
            text=f"🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: {new_text or '0'}",
            reply_markup=calculator_keyboard(),
            parse_mode="Markdown"
        )
    else:
        new_text = current_text + data
        await query.edit_message_text(
            text=f"🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: {new_text}",
            reply_markup=calculator_keyboard(),
            parse_mode="Markdown"
        )

def main():
    try:
        logger.info("🚀 Memulai Bot Telegram...")
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        
        logger.info("✅ Bot terhubung ke Telegram!")
        print("Bot nyala, Boss! Langsung cek Telegram lo.")
        application.run_polling()
    except Exception as e:
        logger.error(f"❌ Error saat menjalankan bot: {e}")
        raise

if __name__ == '__main__':
    main()
