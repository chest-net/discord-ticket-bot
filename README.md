# Discord Ticket Bot System

Современная система управления тикетами поддержки для Discord с использованием Disnake.

## 🌟 Особенности

- ✅ Приватные ветки (Private Threads) вместо отдельных каналов
- ✅ Slash Commands и Components V2 (Buttons, Select Menus, Modals)
- ✅ Система категорий тикетов
- ✅ Назначение ответственных сотрудников
- ✅ Передача тикетов с историей
- ✅ HTML-транскрипции всех тикетов
- ✅ PostgreSQL с asyncpg для хранения данных
- ✅ Системы логирования и аудита
- ✅ Production-ready архитектура

## 🚀 Установка

### Требования
- Python 3.11+
- PostgreSQL 12+
- Discord Server с нужными правами

### Шаги

1. **Клонируй репозиторий**
```bash
git clone https://github.com/chest-net/discord-ticket-bot.git
cd discord-ticket-bot
```

2. **Создай виртуальное окружение**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **Установи зависимости**
```bash
pip install -r requirements.txt
```

4. **Настрой базу данных**
```bash
alembic upgrade head
```

5. **Скопируй .env.example в .env и заполни переменные**
```bash
cp .env.example .env
```

6. **Запусти бота**
```bash
python bot.py
```

## 📋 Структура проекта

```
├── bot.py              # Точка входа
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
├── .env.example        # Пример переменных окружения
│
├── cogs/               # Команды и обработчики
│   ├── __init__.py
│   ├── ticket.py       # Команды для тикетов
│   └── admin.py        # Команды администрирования
│
├── events/             # Event-обработчики
│   ├── __init__.py
│   ├── ready.py
│   └── errors.py
│
├── views/              # UI Components
│   ├── __init__.py
│   ├── buttons.py
│   ├── selects.py
│   └── modals.py
│
├── services/           # Бизнес-логика
│   ├── __init__.py
│   ├── ticket_service.py
│   ├── transcript_service.py
│   └── role_service.py
│
├── database/           # Работа с БД
│   ├── __init__.py
│   ├── connection.py
│   ├── migrations/     # Alembic миграции
│   └── models.py       # SQLAlchemy модели
│
├── models/             # Pydantic модели
│   ├── __init__.py
│   ├── ticket.py
│   ├── user.py
│   └── transcript.py
│
├── utils/              # Вспомогательные функции
│   ├── __init__.py
│   ├── decorators.py
│   ├── permissions.py
│   ├── validators.py
│   └── logger.py
│
└── templates/          # HTML шаблоны
    └── transcript.html
```

## 🎮 Команды

### Администратор
- `/ticket setup` - Создать панель тикетов
- `/ticket config set-support-role` - Установить роль поддержки
- `/ticket config set-log-channel` - Установить канал логов

### Сотрудник
- `/ticket claim` - Взять тикет
- `/ticket transfer` - Передать тикет
- `/ticket close` - Закрыть тикет

### Пользователь
- Используй кнопку на панели для создания тикета

## 📊 База данных

### Таблицы
- `guilds` - Настройки сервера
- `tickets` - Основная информация о тикетах
- `ticket_messages` - Сообщения в тикетах
- `ticket_transfers` - История передач
- `ticket_actions` - Логи действий
- `ticket_settings` - Параметры тикетов

## 🔐 Безопасность

- Проверка прав через декораторы
- Защита от спама и гонки взаимодействий
- Асинхронная обработка запросов
- Логирование всех действий
- SQL injection защита через параметризованные запросы

## 📈 Производительность

- Пул соединений с PostgreSQL
- Кэширование роли и каналов
- Оптимизированные SQL запросы
- Асинхронная обработка
- Фоновые задачи через asyncio

## 📝 Лицензия

MIT License - см. LICENSE файл для деталей

## 👨‍💻 Автор

**chest-net** - [GitHub](https://github.com/chest-net)

## 🐛 Сообщения об ошибках

Если нашел баг, создай [Issue](https://github.com/chest-net/discord-ticket-bot/issues)
