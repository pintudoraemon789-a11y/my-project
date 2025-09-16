from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid
import os
from dotenv import load_dotenv
import telebot

# Load token
load_dotenv("token.env.txt")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")  # username bot kamu, tanpa @

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN tidak ditemukan!")

bot = telebot.TeleBot(BOT_TOKEN)

# Simpan data unik
image_data = {}

# Handler upload foto
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    unique_code = str(uuid.uuid4())[:8]  # kode unik
    
    # Link ke bot ini sendiri
    bot_link = f"https://t.me/testertoko78_bot?start={unique_code}"

    # Simpan data
    image_data[unique_code] = {
        "file_id": file_id,
        "bot_link": bot_link
    }

    # Kirim gambar + caption (hanya link)
    bot.send_photo(
        message.chat.id,
        file_id,
        caption=f"👉 Klik link berikut untuk melanjutkan:\n{bot_link}"
    )

# Handler link unik (/start=kode)
@bot.message_handler(commands=['start'])
def start_handler(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) > 1:
        kode = parts[1]

        if kode in image_data:
            bot_link = image_data[kode]["bot_link"]

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("Join Dulu", url="https://t.me/livestreamingbolaaaaa"),
                InlineKeyboardButton("Coba Lagi", url=bot_link)
            )

            # Kirim caption + tombol (tanpa gambar)
            bot.send_message(
                message.chat.id,
                text=f"👉 Klik link berikut untuk melanjutkan:\n{bot_link}",
                reply_markup=markup
            )
        else:
            bot.send_message(message.chat.id, "❌ Link sudah tidak berlaku.")
    else:
        bot.send_message(message.chat.id, "👋 Halo! Selamat datang di bot 🚀")

print("🤖 Bot sedang berjalan...")
bot.infinity_polling()
