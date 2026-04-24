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
    text = "🧮 *Kalkulator*  
━━━━━━━━━━━  
Display: 0"  
    msg = await update.message.reply_text(text, reply_markup=calculator_keyboard(), parse_mode="Markdown")  
    # Simpan message_id untuk di-edit nanti  
    context.user_data['display_msg_id'] = msg.message_id  
    context.user_data['display'] = "0"

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

    # init state  
    if 'display' not in context.user_data:  
        context.user_data['display'] = "0"  
    if 'display_msg_id' not in context.user_data:  
        context.user_data['display_msg_id'] = None

    current = context.user_data['display']

    # Commands on keyboard  
    if text == 'Menu':  
        # Tampilkan inline menu jika pengguna minta  
        await context.bot.send_message(  
            chat_id=update.effective_chat.id,  
            text="🤖 *Menu Utama*",  
            reply_markup=main_menu(),  
            parse_mode="Markdown"  
        )  
        return

    # Tentukan display_value berdasarkan input  
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
            # Evaluasi matematika dengan sangat hati-hati  
            if current != '0':  
                sanitized = current.replace('*', '*').replace('/', '/')  
                result = eval(sanitized)  
                # Format untuk bilangan float agar tidak terlalu panjang  
                if isinstance(result, float):  
                    result_str = f"{result:.10f}".rstrip('0').rstrip('.')  
                    if result_str == '':  
                        result_str = '0'  
                else:  
                    result_str = str(result)  
                context.user_data['display'] = result_str  
                display_value = result_str  
            else:  
                display_value = '0'  
        except Exception as e:  
            logger.error(f"Calc error: {e}")  
            context.user_data['display'] = 'ERR'  
            display_value = 'ERR'  
    else:  
        # Angka dan operator  
        allowed = set(['0','1','2','3','4','5','6','7','8','9','.', '+', '-', '*', '/'])  
        if len(text) == 1 and text in allowed:  
            # Handle angka  
            if text in ['0','1','2','3','4','5','6','7','8','9','.']:  
                if current == '0' and text == '.':  
                    new_display = '0.'  
                elif current == '0' and text != '.':  
                    new_display = text  
                elif text == '.':  
                    # Cek apakah sudah ada '.' di angka terakhir  
                    parts = []  
                    tmp = ''  
                    for ch in current:  
                        if ch in '+-*/':  
                            if tmp:  
                                parts.append(tmp)  
                            tmp = ''  
                        else:  
                            tmp += ch  
                    if tmp:  
                        parts.append(tmp)  
                    if parts and '.' in parts[-1]:  
                        new_display = current  # tidak tambah '.' lagi  
                    else:  
                        new_display = current + '.'  
                else:  
                    new_display = current + text  
            # Handle operator  
            elif text in ['+', '-', '*', '/']:  
                if current == '0':  
                    new_display = '0' + text  
                else:  
                    # Hapus operator terakhir jika ada operator baru  
                    if current[-1] in ['+', '-', '*', '/']:  
                        new_display = current[:-1] + text  
                    else:  
                        new_display = current + text  
            else:  
                new_display = current  
            context.user_data['display'] = new_display  
            display_value = new_display  
        else:  
            return

    # Edit atau Reply message  
    msg_id = context.user_data.get('display_msg_id')  
    new_text = f"🧮 *Kalkulator*  
━━━━━━━━━━━  
Display: {display_value}"

    if msg_id:  
        # Edit message yang sudah ada  
        try:  
            await context.bot.edit_message_text(  
                chat_id=update.effective_chat.id,  
                message_id=msg_id,  
                text=new_text,  
                reply_markup=calculator_keyboard(),  
                parse_mode="Markdown"  
            )  
        except Exception as e:  
            logger.error(f"Edit error: {e}")  
            # Jika edit gagal, buat message baru  
            msg = await context.bot.send_message(  
                chat_id=update.effective_chat.id,  
                text=new_text,  
                reply_markup=calculator_keyboard(),  
                parse_mode="Markdown"  
            )  
            context.user_data['display_msg_id'] = msg.message_id  
    else:  
        # Reply baru jika belum ada message_id  
        msg = await context.bot.send_message(  
            chat_id=update.effective_chat.id,  
            text=new_text,  
            reply_markup=calculator_keyboard(),  
            parse_mode="Markdown"  
        )  
        context.user_data['display_msg_id'] = msg.message_id

    # Hapus message keyboard user (optional, best effort)  
    try:  
        await update.message.delete()  
    except Exception as e:  
        logger.debug(f"Delete user message failed: {e}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    # Handle callback dari inline menu  
    query = update.callback_query  
    await query.answer()

    if query.data == "calc":  
        await query.edit_message_text(f"🧮 *Kalkulator*  
Gunakan tombol angka untuk memasukkan ekspresi.", reply_markup=calculator_keyboard(), parse_mode="Markdown")  
    elif query.data == "about":  
        await query.edit_message_text("🤖 *Bot Kalkulator Telegram*  
Tekan /start untuk mulai!", parse_mode="Markdown")

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
