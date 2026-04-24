# Deployment Railway - Panduan Lengkap 🚂

## Masalah yang Sering Terjadi & Solusi

### Masalah: `telegram.error.InvalidToken: You must pass the token...`

**Penyebab Utama:**
- ❌ `TELEGRAM_TOKEN` belum di-set di Railway Variables
- ❌ Token tidak ter-copy dengan benar
- ❌ Ada spasi/karakter ekstra di token

**Solusi Step-by-Step:**

1. **Buka Railway Dashboard**
   - Login ke [railway.app](https://railway.app)
   - Pilih project `python-telegram-bot`

2. **Pergi ke Variables Page**
   - Klik tab "Variables" (bukan "Logs" atau "Settings")
   - Lihat apakah `TELEGRAM_TOKEN` sudah ada

3. **Jika Belum Ada:**
   - Klik tombol "New Variable" atau "+"
   - **KEY**: Type `TELEGRAM_TOKEN` (persis seperti ini)
   - **VALUE**: Copy-paste token dari BotFather (tanpa spasi!)
   - Klik **Save** atau tombol checkmark

4. **Redeploy Bot**
   - Tunggu Railway redeploy otomatis, atau
   - Klik tombol "Redeploy" di Railway dashboard
   - Tunggu status jadi "Deployed" (hijau)

5. **Check Logs**
   - Klik tab "Logs"
   - Cari pesan: `✅ Bot terhubung ke Telegram!`
   - Jika ada: ✅ BOT SUDAH BERJALAN!
   - Jika masih error: scroll up dan cek error message

---

## Cara Dapatkan Token Bot Telegram ✅

1. **Buka Telegram** atau ke [@BotFather](https://t.me/botfather)
2. **Kirim `/newbot`**
3. **Ikuti petunjuk:**
   - Beri nama bot (misal: Kalkulator Bot)
   - Beri username bot (misal: MyCalculatorBot)
4. **Dapatkan Token** - akan dikirim BotFather seperti:
   ```
   8640797874:AAHNCn5aPd9eB6-PWZ1nW4K1nTENOcOQpH4
   ```
5. **Copy token ini** dan paste di Railway Variables

---

## Verifikasi Bot Jalan ✨

Setelah set variables dan redeploy:

1. **Buka Telegram**
2. **Cari bot berdasarkan username** yang dibuat di BotFather
3. **Kirim command:** `/start`
4. **Bot harus respond** dengan menu kalkulator

---

## Logs & Debugging 🔍

**Lokasi Logs di Railway:**
- Buka project → Tab "Logs"
- Scroll down untuk lihat pesan terbaru
- Scroll up untuk lihat history

**Pesan-Pesan Penting:**
```
✅ Memulai Bot Telegram...           → Bot starting
✅ Bot terhubung ke Telegram!        → Token valid, ready
Bot nyala, Boss!                     → Bot running
telegram.error.InvalidToken          → ❌ Token error

❌ TELEGRAM_TOKEN tidak ditemukan!   → Variable belum set
```

---

## Tips & Trik 💡

### ✅ DO's:
- ✅ Set TELEGRAM_TOKEN di Railway Variables
- ✅ Copy token dari BotFather dengan hati-hati (no extra spaces)
- ✅ Redeploy setelah set variables
- ✅ Check logs untuk memastikan bot running
- ✅ Test bot dengan `/start` di Telegram

### ❌ DON'Ts:
- ❌ Jangan hardcode token di python-telegram-bot.py
- ❌ Jangan commit `.env` file ke GitHub
- ❌ Jangan share token ke orang lain
- ❌ Jangan edit "Raw Editor" di Railway (gunakan "Variables")
- ❌ Jangan expect bot running sebelum set TELEGRAM_TOKEN

---

## Free Tier Railway 🎁

- **Credit:** $5 gratis per bulan
- **Uptime:** 24/7 (unlimited)
- **Bandwidth:** Unlimited
- **Resources:** Shared, cukup untuk bot Telegram

---

## Contact & Support

Jika masih ada masalah:
1. Cek README.md di repo
2. Check Railway Logs
3. Verifikasi token dari BotFather
4. Coba restart project di Railway dashboard
