import datetime
import os
import openai
import telebot
import MessageHistory as mh



from settings import OpenAI_API_KEY
from settings import Telegram_BOT_API_KEY


openai.api_key = OpenAI_API_KEY
bot = telebot.TeleBot(Telegram_BOT_API_KEY)

botBehaviorModification = "[Act like a seasoned professor with a lot of experience and knowledge, answering questions in detail and step by step if possible.]"

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    user_id = str(message.from_user.id)
    mh.MessageHistory.add_message(user_id, message)

    # Load the message history for the user
    message_history = mh.MessageHistory.load().get(user_id, [])
    # Get the last user message and the last bot response in the history
    last_user_message = ""
    last_bot_response = ""
    for msg in reversed(message_history):
        if msg['is_response']:
            last_bot_response = msg['message']
        else:
            last_user_message = msg['message']
        if last_user_message and last_bot_response:
            break

    NewMessage = f"{botBehaviorModification} your last message was: {last_bot_response}, so {message.text}"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=NewMessage,
        temperature=0.9,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    mh.MessageHistory.add_response(user_id, response['choices'][0]['text'], message.date)
    bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
    #print(f"{datetime.datetime.fromtimestamp(message.date)} \n {message.from_user.first_name}:\n {message.text} \n Bot: {response['choices'][0]['text']} \n")

bot.polling()

