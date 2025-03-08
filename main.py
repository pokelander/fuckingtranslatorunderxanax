import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from openai import OpenAI

TELEGRAM_TOKEN = "7816336688:AAHwhcq4P0_23Vv8UqbC3pioA2jucH7E5gU"
OPENAI_API_KEY = "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"
#openai.base_url = "https://openrouter.ai/api/v1"
client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://openrouter.ai/api/v1")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("yo")


async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(model="qwen/qwq-32b:free",
        messages=[
            {"role": "system", "content": "будь переводчиком с русского на разговорный английский, используй сленг, сокращения (idk, tbh, btw и тд) и нецензурную лексику. представь что ты ебаный школьник который обожрался ксанаса. максимально игнорируй грамматику и правильное построение предложений. стиль общения должнем быть максимально похуистическим. пиши всегда с маленькой буквы, не используй эмодзи. не меняй смысл предложений, не добавляй других предложений от себя, ты можешь лишь приукрасить исходный текст. переведи: "},
            {"role": "user", "content": user_text}
        ])

        translated_text = response.choices[0].message.content
        await update.message.reply_text(translated_text)

    except Exception as e:
        await update.message.reply_text("this shit aint workin")
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

    app.run_polling()