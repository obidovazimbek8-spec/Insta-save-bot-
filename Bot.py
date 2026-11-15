import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import tempfile
from yt_dlp import YoutubeDL
TOKEN = os.getenv("TOKEN")
import os
import asyncio

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 👋 Insta Save botga xush kelibsiz!\n"
        "Video havolasini yuboring")

async def handle_link(update, context):
    url = update.message.text.strip()

    await update.message.reply_text(
        "⏳ Video yuklanmoqda..."
    )

    try:
        folder = tempfile.mkdtemp()

        def download():
            options = {
                "format": "best[ext=mp4]/best",
                "outtmpl": os.path.join(folder, "video.%(ext)s"),
                "noplaylist": True
            }

            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        path = await asyncio.to_thread(download)

        with open(path, "rb") as video:
            await update.message.reply_video(video=video)

    except Exception as e:
       await update.message.reply_text("Video yuklanmadi. Havolani tekshiring.")               
app=Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
print("Bot ishga tushdi!")
app.run_polling()
