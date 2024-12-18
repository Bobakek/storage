import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ContentType
from aiogram import F
from dotenv import load_dotenv
import asyncio

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = "./storage/db.json"
DB_DIR = './storage'

# Инициализация объектов
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Функция для загрузки базы данных
def load_db():
    if not os.path.exists(DB_PATH):  # Если файл не существует, создаем пустой файл
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Создаем директорию, если её нет
        with open(DB_PATH, "w") as f:
            json.dump({}, f)  # Пустой словарь

    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)  # Загружаем содержимое
        except json.JSONDecodeError:  # Если файл повреждён или пустой
            return {}


# Функция для сохранения базы данных
def save_db(data):
    print(f"Saving to DB: {data}")  # Отладочная информация
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)  # Сохраняем данные


# Обработчик загрузки файла
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("Добро пожаловать! Вы можете загрузить файл, и я сохраню его для вас.")


# Обработчик получения документов
@dp.message(F.content_type == ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    db = load_db()
    file_id = message.document.file_id
    file_name = message.document.file_name

    print(f"Received file: {file_name} with file_id: {file_id}")  # Отладка

    # Сохраняем file_id и имя файла в базу данных
    db[file_name] = {'file_id': file_id}
    save_db(db)

    print(f"Database after save: {load_db()}")  # Отладка

    await message.reply(f"Файл '{file_name}' успешно загружен и сохранен на сервере Telegram!")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
