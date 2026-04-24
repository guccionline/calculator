# Bot Kalkulator Telegram 🧮

Bot Telegram interaktif untuk melakukan operasi matematika dengan interface tombol yang user-friendly.

## Fitur ✨
- 🧮 Kalkulator penuh dengan operasi dasar (+, -, *, /)
- 🎨 Interface dengan emoji yang menarik
- ❌ Error handling untuk input tidak valid
- 🔄 Operasi Clear dan Delete
- 📱 Fully responsive di Telegram

## Setup Lokal

### Prerequisites
- Python 3.11+
- Token Bot Telegram

### Installation

1. Clone repository
```bash
git clone <repo-url>
cd python-telegram-bot
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Buat file `.env` dan tambahkan token:
```
TELEGRAM_TOKEN=your_token_here
```

4. Jalankan bot
```bash
python python-telegram-bot.py
```

## Deploy ke Railway 🚂

1. **Sign up/Login** di [Railway.app](https://railway.app)

2. **Buat project baru**
   - Klik "New Project"
   - Pilih "Deploy from GitHub"
   - Connect ke GitHub dan pilih repository ini

3. **Set Environment Variables**
   - Di Railway dashboard, pergi ke Variables
   - Tambahkan:
     ```
     TELEGRAM_TOKEN=your_token_here
     ```

4. **Deploy**
   - Railway akan otomatis detect `Procfile` dan `requirements.txt`
   - Bot akan langsung jalan!

5. **Monitor Logs**
   - Lihat logs di Railway dashboard untuk memastikan bot running

## Cara Pakai 📖

1. Cari bot di Telegram
2. Ketik `/start` untuk melihat menu
3. Pilih "🧮 Kalkulator"
4. Gunakan tombol untuk input angka dan operasi
5. Tekan "=" untuk lihat hasil

## Struktur File

```
python-telegram-bot/
├── python-telegram-bot.py    # Main bot file
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway config
├── runtime.txt              # Python version
├── .env                     # Environment variables (git ignored)
├── .railwayignore          # Files to ignore in Railway
└── README.md               # This file
```

## License

MIT License

## Author

Buatan dengan ❤️ untuk komunitas Indonesia
