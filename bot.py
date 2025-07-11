import telebot
import openai
from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# وقتی کاربر /start می‌فرسته
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 👋 من دستیار هوش مصنوعی هستم. سوالی داری بپرس 🙂")

# همه‌ی پیام‌های متنی
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    user_id = message.from_user.id
    print(f"[User {user_id}] 👤 Message received: {user_input}")  # لاگ

    bot.send_chat_action(message.chat.id, 'typing')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print(f"[OpenAI 🔁] Response: {reply}")  # لاگ پاسخ

    except Exception as e:
        reply = f"❌ خطا در ارتباط با هوش مصنوعی:\n{str(e)}"
        print(f"[ERROR ❌] {e}")  # لاگ ارور

    bot.reply_to(message, reply)

print("🤖 Bot is running... منتظر پیام هستم...")
bot.infinity_polling()