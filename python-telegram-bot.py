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

# Global storage untuk track message_id per user
calc_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Langsung tampilkan keyboard angka saat /start ditekan
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    key = f"{chat_id}_{user_id}"
    
    text = "🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: 0"
    msg = await update.message.reply_text(text, reply_markup=calculator_keyboard(), parse_mode="Markdown")
    
    # Simpan message_id global
    calc_state[key] = {
        'msg_id': msg.message_id,
        'display': '0'
    }

def main_menu():
    # Tetap sediakan main menu (inline) bila diperlukan
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton("🧮 Kalkulator", callback_data="calc")],
        [InlineKeyboardButton("❓ Tentang Bot", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)

def calculator_keyboard():
    # Reply keyboard: tombol akan muncul dan fill semua space
    keyboard = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C", "DEL", "Menu"]
    ]
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        one_time_keyboard=False,
        input_field_placeholder="Pilih tombol di atas →"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle teks dari ReplyKeyboard (angka/operator)
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    key = f"{chat_id}_{user_id}"
    
    # Init state jika belum ada
    if key not in calc_state:
        calc_state[key] = {'msg_id': None, 'display': '0'}
    
    state = calc_state[key]
    current = state['display']
    
    # Process command
    if text == 'C':
        # Clear
        new_display = '0'
    elif text == 'DEL':
        # Delete last char
        new_display = current[:-1] if len(current) > 1 else '0'
    elif text == '=':
        # Calculate
        try:
            expr = current.rstrip('+-*/.')
            if not expr or expr == '0':
                new_display = '0'
            else:
                result = eval(expr)
                new_display = str(result)
        except:
            new_display = 'ERR'
    elif text == 'Menu':
        # Show menu
        await context.bot.send_message(chat_id=chat_id, text="🤖 *Menu Utama*", reply_markup=main_menu(), parse_mode="Markdown")
        return
    else:
        # Add digit/operator
        allowed = set('0123456789.+-*/')
        if all(c in allowed for c in text):
            if current == '0' and text == '0':
                new_display = '0'
            elif current == '0' and text != '.' and text not in '+-*/':
                new_display = text
            elif current.endswith(('+-*/.')) and text in '+-*/.':
                new_display = current[:-1] + text
            else:
                new_display = current + text
        else:
            return
    
    # Update state
    state['display'] = new_display
    new_text = f"🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: {new_display}"
    
    # Edit existing message atau buat baru
    if state['msg_id']:
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=state['msg_id'],
                text=new_text,
                reply_markup=calculator_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.warning(f"Edit gagal: {e}, buat baru")
            msg = await context.bot.send_message(chat_id=chat_id, text=new_text, reply_markup=calculator_keyboard(), parse_mode="Markdown")
            state['msg_id'] = msg.message_id
    else:
        msg = await context.bot.send_message(chat_id=chat_id, text=new_text, reply_markup=calculator_keyboard(), parse_mode="Markdown")
        state['msg_id'] = msg.message_id
    
    # Hapus user message (best effort)
    try:
        await update.message.delete()
    except:
        pass

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
