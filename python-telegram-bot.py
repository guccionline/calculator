import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token bot lo taruh sini, jangan sampe bocor ke si "Man"
TOKEN = 'TOKEN_BOT_LO_DI_SINI'

# Setup logging biar kita tau kalau ada yang fucked up
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kalkulator V Siap Tempur! Pencet tombol di bawah:", reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    # Susunan tombol biar mirip kalkulator beneran
    keyboard = [
        [InlineKeyboardButton("C", callback_id="clear"), InlineKeyboardButton("DEL", callback_id="del"), InlineKeyboardButton("/", callback_id="/")],
        [InlineKeyboardButton("7", callback_id="7"), InlineKeyboardButton("8", callback_id="8"), InlineKeyboardButton("9", callback_id="9"), InlineKeyboardButton("*", callback_id="*")],
        [InlineKeyboardButton("4", callback_id="4"), InlineKeyboardButton("5", callback_id="5"), InlineKeyboardButton("6", callback_id="6"), InlineKeyboardButton("-", callback_id="-")],
        [InlineKeyboardButton("1", callback_id="1"), InlineKeyboardButton("2", callback_id="2"), InlineKeyboardButton("3", callback_id="3"), InlineKeyboardButton("+", callback_id="+")],
        [InlineKeyboardButton("0", callback_id="0"), InlineKeyboardButton(".", callback_id="."), InlineKeyboardButton("=", callback_id="=")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    current_text = query.message.text.split('\n')[-1] # Ambil angka terakhir
    
    if current_text == "Kalkulator V Siap Tempur! Pencet tombol di bawah:":
        current_text = ""

    if data == "=":
        try:
            # Hati-hati pakai eval, tapi buat kalkulator simpel gini sih sikat aja
            result = str(eval(current_text))
            await query.edit_message_text(text=f"Hasil: {result}", reply_markup=main_menu_keyboard())
        except:
            await query.edit_message_text(text="Error, Boss! Inputnya yang bener dong.", reply_markup=main_menu_keyboard())
    elif data == "clear":
        await query.edit_message_text(text="Cleared. Ulang lagi:", reply_markup=main_menu_keyboard())
    elif data == "del":
        await query.edit_message_text(text=current_text[:-1] or "0", reply_markup=main_menu_keyboard())
    else:
        await query.edit_message_text(text=current_text + data, reply_markup=main_menu_keyboard())

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    
    print("Bot nyala, Boss! Langsung cek Telegram lo.")
    application.run_polling()

if __name__ == '__main__':
    main()