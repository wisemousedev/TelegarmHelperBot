import datetime
import os
import json


class MessageHistory:
    MESSAGE_HISTORY_FILE = "message_history.json"

    @staticmethod
    def load():
        if os.path.exists(MessageHistory.MESSAGE_HISTORY_FILE):
            with open(MessageHistory.MESSAGE_HISTORY_FILE, "r") as f:
                return json.load(f)
        else:
            return {}

    @staticmethod
    def save(message_history):
        with open(MessageHistory.MESSAGE_HISTORY_FILE, "w") as f:
            json.dump(message_history, f, indent=4)

    @staticmethod
    def add_message(user_id, message):
        message_history = MessageHistory.load()

        if user_id not in message_history:
            message_history[user_id] = []

        message_entry = {
            "message": message.text,
            "timestamp": message.date,
            "is_response": False
        }

        message_history[user_id].append(message_entry)
        MessageHistory.save(message_history)

    @staticmethod
    def add_response(user_id, text, timestamp):
        message_history = MessageHistory.load()

        if user_id not in message_history:
            message_history[user_id] = []

        message_entry = {
            "message": text,
            "timestamp": timestamp,
            "is_response": True
        }

        message_history[user_id].append(message_entry)
        MessageHistory.save(message_history)

    @staticmethod
    def print_user_messages(user_id):
        message_history = MessageHistory.load()

        if user_id not in message_history:
            print(f"No messages found for user: {user_id}")
            return

        # Sort messages by timestamp
        sorted_messages = sorted(message_history[user_id],
                                 key=lambda x: datetime.datetime.fromtimestamp(x['timestamp']))

        for message in sorted_messages:
            message_type = 'Response' if message['is_response'] else 'Message'
            print(f"{message_type} at {datetime.datetime.fromtimestamp(message['timestamp'])}: {message['message']}")