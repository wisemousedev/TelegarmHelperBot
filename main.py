import datetime
import os
import openai
import telebot

from MessageHistory import MessageHistory

mh = MessageHistory()

from settings import OpenAI_API_KEY
from settings import Telegram_BOT_API_KEY

openai.api_key = OpenAI_API_KEY
bot = telebot.TeleBot(Telegram_BOT_API_KEY)


botBehaviorModification = "BehaviorModification.txt"
with open(botBehaviorModification, "r") as file:
    mode = file.read()

messages = [{"role": "system", "content": f"{mode}"}]


@bot.message_handler(func=lambda _: True)
def handle_message(message):
    user_id = str(message.from_user.id)

    # Load the user's message history
    history = mh.load_messages(user_id)

    # If history exists, append it to messages
    if history:
        for msg in history:
            if msg['is_response']:
                messages.append({"role": "assistant", "content": msg['text']})
            else:
                messages.append({"role": "user", "content": msg['text']})

    # Add the new message to the history
    mh.add_message(user_id, message)
    messages.append({"role": "user", "content": message.text})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        temperature=0.8
    )

    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    bot.send_message(chat_id=message.from_user.id, text=response)

    mh.add_response(user_id, response, message.date)
    mh.save()
    print(
        f"{datetime.datetime.fromtimestamp(message.date)} \n {message.from_user.first_name} ({message.from_user.id}): {message.text} \n Bot: {response} \n")


bot.polling()
