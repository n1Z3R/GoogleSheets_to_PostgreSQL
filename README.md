# GoogleSheets_to_PostgreSQL
Скрипт для наблюдения изменений в таблице GoogleSheets, бот для оповещения о сроках поставок на текущий день(каждый новый день оповещение), web страница с небольшим графиком из бд.
## Гайд:
1) @getmyid_bot - в этом telegram боте узнать ваш user id и записать в dockercompose.yml -> services -> bot -> environment -> CHAT_ID (для получения оповещений в тг).
2) ```docker compose up -d```

Адрес для проверки: http://127.0.0.1:8000/
