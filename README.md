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
- Token Bot Telegram dari [BotFather](https://t.me/botfather)

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
> ⚠️ Dapatkan token dari [@BotFather](https://t.me/botfather) di Telegram

4. Jalankan bot
```bash
python python-telegram-bot.py
```

## Deploy ke Railway 🚂

### Langkah 1: Persiapan Repository

Pastikan sudah push ke GitHub:
```bash
git add .
git commit -m "Setup Railway deployment"
git push origin main
```

### Langkah 2: Setup Railway Project

1. **Buka [Railway.app](https://railway.app)**
2. **Login dengan GitHub** atau buat akun baru
3. **Klik "New Project"**
4. **Pilih "Deploy from GitHub"**
5. **Authorize Railway** dan pilih repository `python-telegram-bot`

### Langkah 3: Set Environment Variables ⚠️ PENTING!

Setelah project terbuat di Railway:

1. **Buka Railway Dashboard** → Pilih project `python-telegram-bot`
2. **Pergi ke tab "Variables"** (bukan "Raw Editor")
3. **Klik "New Variable"** atau "+"
4. **Isi:**
   - **Key/Name**: `TELEGRAM_TOKEN`
   - **Value**: (paste token bot Anda dari BotFather)
5. **Klik "Save"** / tombol checkmark
6. **Redeploy** dengan klik tombol deploy atau tunggu automatic redeploy

### Langkah 4: Verifikasi Bot Jalan

1. **Buka tab "Logs"** di Railway dashboard
2. **Cari pesan:**
   ```
   ✅ Bot terhubung ke Telegram!
   Bot nyala, Boss! Langsung cek Telegram lo.
   ```
3. **Jika ada error**, scroll up dan cek:
   - `InvalidToken` → TELEGRAM_TOKEN belum di-set atau salah
   - `Connection refused` → Railway restart, tunggu beberapa detik

### Langkah 5: Test Bot

1. **Buka Telegram**
2. **Cari bot Anda** berdasarkan username yang dibuat di BotFather
3. **Kirim `/start`**
4. **Gunakan tombol kalkulator** untuk test

## Troubleshooting 🔧

### ❌ Error: "InvalidToken"
**Penyebab:** TELEGRAM_TOKEN tidak di-set atau tidak valid

**Solusi:**
1. Verifikasi token dari BotFather masih valid
2. Set TELEGRAM_TOKEN di Railway Variables (bukan di code!)
3. Tunggu Railway redeploy setelah set variable
4. Check logs untuk memastikan token ter-load

### ❌ Error: "Connection refused"
**Penyebab:** Railway sedang restart atau network issue

**Solusi:**
- Tunggu 30-60 detik untuk Railway selesai restart
- Klik tombol "Restart" di Railway dashboard

### ❌ Bot tidak respond
**Penyebab:** Bot status tidak running atau token error

**Solusi:**
1. Check Logs di Railway untuk error messages
2. Verifikasi bot username benar di BotFather
3. Coba kirim `/start` lagi

## Struktur File

```
python-telegram-bot/
├── python-telegram-bot.py    # Main bot file
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway config (worker: ...)
├── runtime.txt              # Python version (3.11.8)
├── .env                     # Environment variables (git ignored, lokal only)
├── .railwayignore          # Files to ignore when deploying
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Environment Variables

### Lokal Development
Gunakan file `.env`:
```
TELEGRAM_TOKEN=your_token_here
```

### Railway Production
Set di Railway Dashboard → Variables:
- Key: `TELEGRAM_TOKEN`
- Value: (paste token bot)

## Useful Links

- 🤖 [Telegram BotFather](https://t.me/botfather) - Buat/manage bot
- 🚂 [Railway.app](https://railway.app) - Hosting gratis
- 📚 [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io/)
- 📖 [Railway Docs](https://docs.railway.app/)

## License

MIT License

## Author

Buatan dengan ❤️ untuk komunitas Indonesia

