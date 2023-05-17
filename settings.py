import os
import dotenv

dotenv.load_dotenv('.env')

OpenAI_API_KEY = os.environ['OpenAI_API_KEY']
Telegram_BOT_API_KEY = os.environ['Telegram_BOT_API_KEY']