# FastAPI Project

Базовий FastAPI-проєкт, створений за допомогою менеджера пакетів [uv](https://docs.astral.sh/uv/).

## Вимоги

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Встановлення залежностей

```bash
uv sync
```

## Запуск проєкту

Запустіть сервер розробки:

```bash
uv run fastapi dev main.py
```

Після запуску API буде доступне за адресою [http://127.0.0.1:8000](http://127.0.0.1:8000).

Перевірте роботу ендпоінту:

```bash
curl http://127.0.0.1:8000/
```

Очікувана відповідь:

```json
{"message": "Hello World!"}
```

## Перевірка якості коду

Встановіть pre-commit хуки (один раз):

```bash
uv run pre-commit install
```

Запустіть перевірки вручну:

```bash
uv run pre-commit run --all-files
```
