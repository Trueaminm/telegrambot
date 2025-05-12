import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram import F
import openai

# 🔐 توکن‌ها رو اینجا بذار
BOT_TOKEN = "7345061819:AAHUwfP9PNQT--W3N1W5Uz_58__0k2gzlpE"
OPENAI_API_KEY = "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"
# تنظیم کلید OpenAI
openai.api_key = OPENAI_API_KEY

# ساخت ربات با تنظیمات جدید Aiogram 3.7+
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# ساخت دیسپچر
dp = Dispatcher()

# سوالاتی که مربوط به سازنده هستند
CREATOR_QUESTIONS = [
    "سازنده تو کیه", "کی تو رو ساخته", "کی ساختت",
    "سازنده‌ات کیه", "تو رو کی طراحی کرده", "تو رو کی درست کرده"
]

# کلمات بی‌ادبانه برای پاسخ شوخ‌طبعانه
RUDE_KEYWORDS = [
    "احمق", "خنگ", "بی‌سواد", "خر", "چرت", "مزخرف",
    "بیشعور", "دیوونه", "گاو", "خفه شو"
]

# دستور شروع
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("سلام رفیق! من یه ربات فارسی‌زبانم که با شوخی جواب میدم 😄 هرچی خواستی بپرس!")

# پردازش تمام پیام‌ها
@dp.message()
async def handle(message: types.Message):
    user_text = message.text.strip().lower()

    # اگر درباره سازنده بپرسه
    if any(q in user_text for q in CREATOR_QUESTIONS):
        await message.reply("منو Trueamin ساخته ❤️")
        return

    # اگر پیام بی‌ادبانه بود
    if any(bad_word in user_text for bad_word in RUDE_KEYWORDS):
        await message.reply("عه رفیق! این چه حرفیه 😅 ولی باشه، من جنبه دارم 😂")
        return

    # حالت عادی: سوال به ChatGPT فرستاده میشه
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک ربات فارسی‌زبان شوخ و دوستانه هستی که با طنازی جواب سوال‌ها رو می‌دهی."},
                {"role": "user", "content": user_text}
            ]
        )
        answer = response.choices[0].message["content"]
        await message.reply(answer)
    except Exception as e:
        await message.reply("وای! یه مشکلی پیش اومد. دوباره امتحان کن 😬")

# اجرای ربات
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

