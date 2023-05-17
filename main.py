import os
import openai
import telebot


from settings import OpenAI_API_KEY
from settings import Telegram_BOT_API_KEY


openai.api_key = OpenAI_API_KEY
bot = telebot.TeleBot(Telegram_BOT_API_KEY)

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])

bot.polling()

