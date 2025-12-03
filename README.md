Game Rent Bot (Telegram + Mini App)
Телеграм‑бот и мини‑приложение для аренды игрового оборудования (приставок).

1. Требования
Python 3.10+

pip

Node.js (для npx localtunnel, опционально)

Telegram‑аккаунт и созданный бот через @BotFather

Установленные зависимости проекта:

bash
pip install -r requirements.txt
2. Структура проекта
bot.py — Telegram‑бот (long polling)

api.py — backend на FastAPI (каталог, заказы)

db.py — модели SQLAlchemy и подключение к SQLite (rent.db)

schemas.py — Pydantic‑схемы

mini_app/ — фронтенд мини‑приложения

index.html

style.css

script.js

.env — конфиг с токеном бота и URL (не коммитить)

3. Первичная настройка
Создать файл .env в корне:

text
TELEGRAM_BOT_TOKEN=ТВОЙ_ТОКЕН_ОТ_BOTFATHER
(остальные переменные можно добавить позже).

Убедиться, что БД создаётся автоматически:

При первом запуске любого из модулей вызывается Base.metadata.create_all(engine) и создаёт rent.db.

4. Запуск backend (FastAPI)
В отдельном терминале из корня проекта:

bash
python -m pip install uvicorn fastapi  # если нужно
python -m uvicorn api:app --reload
Backend будет доступен по адресу:

http://127.0.0.1:8000

Документация Swagger: http://127.0.0.1:8000/docs

Через /docs удобно добавить тестовые товары через POST /items.

5. Запуск статики Mini App локально
В папке mini_app:

bash
cd mini_app
python -m http.server 5432
Страница будет доступна по адресу:

http://127.0.0.1:5432/index.html

На этом этапе Mini App можно тестировать просто в браузере (каталог должен подтягиваться из API_URL в script.js).

6. Проброс наружу (tunнели) — опционально для Telegram
Чтобы Mini App и API были доступны из Telegram, нужно пробросить локальные порты наружу (пример с localtunnel):

Мини‑приложение (порт 5432):

bash
cd mini_app
npx localtunnel --port 5432
# полученный https‑URL → для Mini App
API (порт 8000):

bash
cd ..
npx localtunnel --port 8000
# полученный https‑URL → в const API_URL в script.js
В mini_app/script.js:

javascript
const API_URL = "https://ТВОЙ_ДОМЕН_ДЛЯ_API"; // туннель к 8000
7. Настройка Mini App в BotFather
@BotFather → /mybots → выбрать бота.

Bot Settings → Menu Button → Configure Mini App.

Ввести:

Title: Каталог

URL: https://ТВОЙ_ДОМЕН_ДЛЯ_MINI_APP/index.html

Сохранить.

Можно также добавить inline‑кнопку в коде bot.py с web_app=WebAppInfo(url=...).

8. Запуск Telegram‑бота
В отдельном терминале из корня проекта:

bash
python bot.py
Важно: одновременно должен быть запущен только один процесс бота с этим токеном. Если ранее использовался webhook, нужно один раз выполнить deleteWebhook через URL https://api.telegram.org/bot<TOKEN>/deleteWebhook?drop_pending_updates=true.

После запуска:

Написать боту /start.

Нажать кнопку для открытия Mini App.

Проверить, что каталог загружается, товары отображаются.

9. Остановка
Backend (uvicorn), http.server и bot.py останавливаются Ctrl + C в своих терминалах.

Туннели (localtunnel/ngrok) — тоже Ctrl + C.