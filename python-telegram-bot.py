import logging
import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

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
    # Langsung tampilkan keyboard angka saat /start ditekan
    text = "🧮 *Kalkulator*\nGunakan tombol angka di bawah untuk memasukkan ekspresi."
    await update.message.reply_text(text, reply_markup=calculator_keyboard(), parse_mode="Markdown")

def main_menu():
    # Tetap sediakan main menu (inline) bila diperlukan
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton("🧮 Kalkulator", callback_data="calc")],
        [InlineKeyboardButton("❓ Tentang Bot", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)

def calculator_keyboard():
    # Reply keyboard: tombol akan muncul di atas kolom input pengguna
    keyboard = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C", "DEL", "Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle teks dari ReplyKeyboard (angka/operator)
    text = update.message.text.strip()

    # init state
    if 'display' not in context.user_data:
        context.user_data['display'] = "0"

    current = context.user_data['display']

    # Commands on keyboard
    if text == 'Menu':
        # Tampilkan inline menu jika pengguna minta
        await update.message.reply_text("🤖 *Menu Utama*", reply_markup=main_menu(), parse_mode="Markdown")
        return

    if text == 'C':
        context.user_data['display'] = '0'
        display_value = '0'
    elif text == 'DEL':
        if current != '0':
            current = current[:-1] if len(current) > 1 else '0'
        context.user_data['display'] = current
        display_value = current
    elif text == '=':
        try:
            calc_text = current.rstrip('+-*/')
            result = str(eval(calc_text)) if calc_text not in ['', '0'] else '0'
            context.user_data['display'] = result
            display_value = result
        except Exception as e:
            logger.error(f"Calc error: {e}")
            context.user_data['display'] = '0'
            display_value = 'ERR'
    else:
        # assume digit or operator
        allowed = set(list('0123456789.+-*/'))
        # If user pressed e.g. '7' or '/' or '.'
        if all(ch in allowed for ch in text):
            if current == '0' and text not in ['+', '-', '*', '/', '.']:
                new_display = text
            elif current == '0' and text == '.':
                new_display = '0.'
            elif text in '+-*/':
                if current and current[-1] not in '+-*/':
                    new_display = current + text
                else:
                    new_display = current.rstrip('+-*/') + text
            elif text == '.':
                parts = current.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').split()
                if parts and '.' in parts[-1]:
                    new_display = current
                else:
                    new_display = current + '.'
            else:
                new_display = current + text
        else:
            # fallback: ignore unknown input
            return

        context.user_data['display'] = new_display
        display_value = new_display

    # respond with updated display
    await update.message.reply_text(f"🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: {display_value}", reply_markup=calculator_keyboard(), parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle callback dari inline menu
    query = update.callback_query
    await query.answer()
    
    if query.data == "calc":
        await query.edit_message_text(f"🧮 *Kalkulator*\nGunakan tombol angka untuk memasukkan ekspresi.", reply_markup=calculator_keyboard(), parse_mode="Markdown")
    elif query.data == "about":
        await query.edit_message_text("🤖 *Bot Kalkulator Telegram*\nTekan /start untuk mulai!", parse_mode="Markdown")

def main():
    try:
        logger.info("🚀 Memulai Bot Telegram...")
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        # Handler untuk keyboard angka - hanya terima dari keyboard, bukan pesan biasa
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("✅ Bot terhubung ke Telegram!")
        print("Bot nyala, Boss! Langsung cek Telegram lo.")
        application.run_polling()
    except Exception as e:
        logger.error(f"❌ Error saat menjalankan bot: {e}")
        raise

if __name__ == '__main__':
    main()
