# 📁 **Telegram File Storage Bot**  
Ваш персональный менеджер файлов в Telegram с удобным веб-интерфейсом!  


### 📖 Описание  
**Telegram File Storage Bot** — это проект, который позволяет:  
1. Загружать файлы через Telegram-бота.  
2. Управлять ими через веб-интерфейс:  
   - 📄 Просматривать список загруженных файлов.  
   - ⬇️ Скачивать файлы напрямую с серверов Telegram.  
   - ❌ Удалять файлы из базы данных.  

Проект построен на основе **Telegram Bot API** и **FastAPI**, с веб-интерфейсом на HTML/CSS/JavaScript.  

---

### 🛠 Технологии  

- **Python**:  
  - [Aiogram](https://docs.aiogram.dev/en/latest/) — для взаимодействия с Telegram Bot API.  
  - [FastAPI](https://fastapi.tiangolo.com/) — для создания API и веб-интерфейса.  
- **HTML, CSS, JavaScript**: Для создания интерактивного интерфейса.  
- **Jinja2**: Для рендеринга HTML через шаблоны.  
- **JSON**: Для хранения информации о загруженных файлах.  

---

### 📂 Структура проекта  

```
project/
├── api/
│   ├── main.py                 # Логика FastAPI-приложения
├── bot/
│   ├── bot.py                  # Telegram-бот
│   └── storage/
│       └── db.json             # База данных (JSON)
├── templates/
│   └── index.html              # Веб-интерфейс
├── .env                        # Переменные окружения (токен бота)
├── requirements.txt            # Список зависимостей
└── README.md                   # Описание проекта
```

---

---

### 🖥 Установка и запуск  

#### 1. Клонируйте репозиторий:  
```bash
git clone https://github.com/yourusername/telegram-file-storage.git
cd telegram-file-storage
```  

#### 2. Установите зависимости:  
```bash
pip install -r requirements.txt
```  

#### 3. Настройте переменные окружения:  
Создайте файл `.env` в корне проекта и добавьте токен вашего бота:  
```
BOT_TOKEN=ваш_токен_бота
```  

#### 4. Запустите Telegram-бот:  
```bash
python bot/bot.py
```  

#### 5. Запустите FastAPI-приложение:  
```bash
uvicorn api.main:app --reload
```  

#### 6. Откройте веб-интерфейс:  
Перейдите по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

---

### 🧪 Примеры API-запросов  

#### Получение списка файлов  
**GET** `/files`  
```json
{
    "files": [
        {
            "name": "example.png",
            "file_id": "BQACAgIAAxkBA...",
            "size": 204800
        }
    ]
}
```  

#### Скачивание файла  
**GET** `/files/{file_name}`  
Ответ:  
```json
{
    "name": "example.png",
    "download_url": "https://api.telegram.org/file/bot<TOKEN>/path_to_file"
}
```  

#### Удаление файла  
**DELETE** `/files/{file_name}`  
Ответ:  
```json
{
    "message": "File 'example.png' successfully deleted."
}
```  

---

### 🌟 Возможности  

- Поддержка файлов **до 20 МБ** (Telegram Bot API ограничивает размер).  Возможность поиска по названию файла в самом тг боте.
- Удобный веб-интерфейс для управления файлами.  
- Лёгкость интеграции с другими проектами.  

---



---

### 🌍 Ссылки  

- [Документация FastAPI](https://fastapi.tiangolo.com/)  
- [Документация Aiogram](https://docs.aiogram.dev/en/latest/)

