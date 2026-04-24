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
        [InlineKeyboardButton("🔴 C", callback_data="clear"), InlineKeyboardButton("⬅️ DEL", callback_data="del"), InlineKeyboardButton("➗", callback_data="/")],
        [InlineKeyboardButton("7️⃣", callback_data="7"), InlineKeyboardButton("8️⃣", callback_data="8"), InlineKeyboardButton("9️⃣", callback_data="9"), InlineKeyboardButton("✖️", callback_data="*")],
        [InlineKeyboardButton("4️⃣", callback_data="4"), InlineKeyboardButton("5️⃣", callback_data="5"), InlineKeyboardButton("6️⃣", callback_data="6"), InlineKeyboardButton("➖", callback_data="-")],
        [InlineKeyboardButton("1️⃣", callback_data="1"), InlineKeyboardButton("2️⃣", callback_data="2"), InlineKeyboardButton("3️⃣", callback_data="3"), InlineKeyboardButton("➕", callback_data="+")],
        [InlineKeyboardButton("0️⃣", callback_data="0"), InlineKeyboardButton("🔸", callback_data="."), InlineKeyboardButton("✅ =", callback_data="=")],
        [InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    # Ambil state kalkulator dari user data
    if 'display' not in context.user_data:
        context.user_data['display'] = "0"
        context.user_data['last_result'] = None
    
    current_display = context.user_data.get('display', '0')
    last_result = context.user_data.get('last_result', None)
    
    # Menu utama
    if data == "calc":
        context.user_data['display'] = "0"
        context.user_data['last_result'] = None
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
        context.user_data['display'] = "0"
        context.user_data['last_result'] = None
        await query.edit_message_text(
            text="🤖 *Selamat Datang di Bot!*\n\nPilih menu di bawah:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        return
    
    # Kalkulator logic
    if data == "clear":
        # Clear semua
        context.user_data['display'] = "0"
        context.user_data['last_result'] = None
        display_value = "0"
    
    elif data == "del":
        # Delete character terakhir
        if current_display != "0":
            current_display = current_display[:-1] if len(current_display) > 1 else "0"
        context.user_data['display'] = current_display
        display_value = current_display
    
    elif data == "=":
        # Hitung hasil
        try:
            # Hapus trailing operator jika ada
            calc_text = current_display.rstrip('+-*/')
            if calc_text and calc_text != current_display:
                calc_text = current_display[:-1]
            else:
                calc_text = current_display
            
            result = str(eval(calc_text))
            context.user_data['display'] = result
            context.user_data['last_result'] = result
            display_value = result
            display_text = f"🧮 *Kalkulator*\n━━━━━━━━━━━\n📊 Hasil: {result}"
        except:
            context.user_data['display'] = "0"
            display_value = "0"
            display_text = "🧮 *Kalkulator*\n━━━━━━━━━━━\n❌ Error! Input tidak valid."
            await query.edit_message_text(
                text=display_text,
                reply_markup=calculator_keyboard(),
                parse_mode="Markdown"
            )
            return
    
    else:
        # Input angka atau operator
        # Jika display adalah "0" dan input bukan operator atau titik
        if current_display == "0" and data not in ["+", "-", "*", "/", "."]:
            new_display = data
        elif current_display == "0" and data == ".":
            new_display = "0."
        elif current_display.endswith((".","0")) and data in ["+", "-", "*", "/"] and not current_display.endswith((".", "+")):
            # Jangan append operator ganda
            if not any(op in current_display for op in ["+", "-", "*", "/"]):
                new_display = current_display + data
            else:
                # Replace operator terakhir
                new_display = current_display.rstrip("+-*/") + data
        else:
            # Cegah operator ganda atau titik ganda
            if data == ".":
                # Cek ada titik di angka terakhir?
                parts = current_display.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split()
                if parts and "." in parts[-1]:
                    return  # Jangan add titik lagi
            elif data in ["+", "-", "*", "/"]:
                # Jangan add operator jika last char adalah operator
                if current_display and current_display[-1] in ["+", "-", "*", "/"]:
                    return
            
            new_display = current_display + data
        
        context.user_data['display'] = new_display
        display_value = new_display
    
    # Update message dengan display baru
    if data != "=":
        await query.edit_message_text(
            text=f"🧮 *Kalkulator*\n━━━━━━━━━━━\nDisplay: {display_value}",
            reply_markup=calculator_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(
            text=display_text,
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
