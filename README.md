# Docker проект для Python приложений

## Быстрый старт

### Запуск приложения
```bash
docker-compose up
```

### Запуск в фоновом режиме
```bash
docker-compose up -d
```

### Остановка
```bash
docker-compose down
```

### Пересборка образа
```bash
docker-compose build
```

### Запуск с пересборкой
```bash
docker-compose up --build
```

### Выполнение команд в контейнере
```bash
docker-compose exec app bash
```

### Запуск другого Python скрипта
Измените команду в `docker-compose.yml` или запустите напрямую:
```bash
docker-compose run --rm app python your_script.py
```

## Структура проекта

- `Dockerfile` - конфигурация Docker образа
- `docker-compose.yml` - конфигурация для удобного запуска
- `requirements.txt` - зависимости Python
- `index.py` - основной файл FastAPI приложения
- `.env.sample` - пример файла с переменными окружения

## Настройка

### Переменные окружения

1. Скопируйте `.env.sample` в `.env`:
   ```bash
   cp .env.sample .env
   ```

2. Отредактируйте `.env` и укажите свои значения:
   - `GIGACHAT_AUTH_KEY` - секретный ключ для аутентификации GigaChat
   - `APP_API_KEY` - секретный ключ для авторизации API endpoints

**Важно:** Файл `.env` находится в `.gitignore` и не коммитится в репозиторий.

### Другие настройки

1. Добавьте зависимости в `requirements.txt`
2. Измените команду запуска в `docker-compose.yml` если нужно
3. Код автоматически синхронизируется через volume

## API

После запуска приложение доступно по адресу: http://localhost:8000
