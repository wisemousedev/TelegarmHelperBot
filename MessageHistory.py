import json
import os
from collections import defaultdict
from datetime import datetime

class MessageHistory:
    def __init__(self, directory="message_history"):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)
        self.histories = defaultdict(list)
        self.message_lists = defaultdict(list)  # Store the message lists here

        # Load message histories from saved JSON files
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                user_id = filename[:-5]  # remove the ".json" extension
                self.load(user_id)

    def add_message(self, user_id, message, is_response=False):
        self.histories[user_id].append({
            'timestamp': datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'),
            'first_name': message.from_user.first_name,
            'id': message.from_user.id,
            'text': message.text,
            'is_response': is_response
        })

    def add_response(self, user_id, response, timestamp):
        self.histories[user_id].append({
            'timestamp': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'text': response,
            'is_response': True
        })

    def save(self):
        for user_id, history in self.histories.items():
            with open(f"{self.directory}/{user_id}.json", 'w', encoding='utf-8') as f:
                json.dump(history, f, default=str, ensure_ascii=False)

    def load(self, user_id):
        try:
            with open(f"{self.directory}/{user_id}.json", 'r', encoding='utf-8') as f:
                self.histories[user_id] = json.load(f)
        except FileNotFoundError:
            self.histories[user_id] = []

    def save_messages(self, user_id, messages):
        self.message_lists[user_id] = messages

    def load_messages(self, user_id):
        return self.message_lists[user_id]
