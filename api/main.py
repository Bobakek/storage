from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os
import json
from aiogram import Bot
from dotenv import load_dotenv
from starlette.responses import HTMLResponse

load_dotenv()

# Путь к базе данных
DB_PATH = "./bot/storage/db.json"
DB_DIR = "./bot/storage"

# Telegram Bot API токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация Telegram бота
bot = Bot(token=BOT_TOKEN)


# Убедимся, что файл базы данных существует
def ensure_db_exists():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({}, f)


# Функция для загрузки базы данных
def load_db():
    ensure_db_exists()
    with open(DB_PATH, "r") as f:
        return json.load(f)


# Инициализация FastAPI
app = FastAPI()

# Настройка Jinja2Templates для рендера HTML
templates = Jinja2Templates(directory="templates")


# Эндпоинт для получения списка файлов
@app.get("/files")
async def get_files():
    db = load_db()
    if not db:
        return JSONResponse(content={"message": "No files available"}, status_code=200)

    files = []
    for name, data in db.items():
        file_id = data["file_id"]
        try:
            # Получаем информацию о файле
            file_info = await bot.get_file(file_id)
            file_size = file_info.file_size  # Размер файла в байтах

            # Проверка, не превышает ли файл лимит
            if file_size > 20 * 1024 * 1024:  # 20 МБ
                file_size = "Too Large (over 20 MB)"

        except Exception:
            file_size = "Unknown (too large or error)"

        files.append({"name": name, "file_id": file_id, "size": file_size})

    return {"files": files}


# Эндпоинт для получения ссылки на скачивание файла
@app.get("/files/{file_name}")
async def get_file_download_link(file_name: str):
    db = load_db()
    if file_name not in db:
        raise HTTPException(status_code=404, detail="File not found")

    file_id = db[file_name]["file_id"]

    # Получаем путь к файлу от Telegram
    try:
        file = await bot.get_file(file_id)
        file_path = file.file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file path: {e}")

    # Формируем ссылку для скачивания
    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    return {"name": file_name, "download_url": download_url}

# Функция для сохранения базы данных
def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

# Эндпоинт для удаления файла
@app.delete("/files/{file_name}")
async def delete_file(file_name: str):
    db = load_db()

    # Проверяем, существует ли файл в базе данных
    if file_name not in db:
        raise HTTPException(status_code=404, detail="File not found")

    # Удаляем файл из базы данных
    del db[file_name]
    save_db(db)

    return JSONResponse(content={"message": f"File '{file_name}' successfully deleted."})

# Эндпоинт для отображения HTML-страницы
@app.get("/", response_class= HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})