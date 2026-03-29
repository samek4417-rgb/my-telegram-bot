import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

BOT_TOKEN = os.environ["8755429686:AAF6ULzszyABCoPGY3Q_IVyYi5-3Mn9ZaiI"]

WAITING_FOR_TEXT = 1

async def sovit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🔒 Username: {user.first_name}\n"
        f"User ID: {user.id}\n\n"
        f"⚠️ Your Text:\n"
        f"Ab apna text bhejo – main use voice mein badal dunga! 😍"
    )
    return WAITING_FOR_TEXT

async def text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.strip():
        await update.message.reply_text("❌ Please send some text to convert.")
        return WAITING_FOR_TEXT

    processing_msg = await update.message.reply_text("🎙️ Converting text to voice...")

    try:
        from gtts import gTTS

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
            mp3_path = mp3_file.name

        # Generate speech
        tts = gTTS(text=text, lang="hi")
        tts.save(mp3_path)

        # Send as audio file
        with open(mp3_path, "rb") as audio_file:
            await update.message.reply_audio(audio=audio_file, caption=f"🎤 {text[:50]}")

        await processing_msg.delete()

    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("sovit", sovit_command)],
        states={
            WAITING_FOR_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_voice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("🤖 Bot is running on Render...")
    app.run_polling()

if __name__ == "__main__":
    main()