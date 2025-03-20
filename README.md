# Сервис управления заказами

> Вместо celery конечно круто было бы взять
> taskiq. Но раз нужно celery, то оптимальным 
> выбором брокера будет Rabbitmq из-за интеграции
> с celery


> _(Только авторизованные)_ написано только у одной ручки
> хотя логично на все /orders проверять авторизацию
> но допустим так и задумано


> По хорошему изменения статуса заказов нужно хранить как 
> event sourcing но такого требования нет

### Структура
```
.
├── Dockerfile
├── Makefile
├── README.md
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── endpoints
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── orders.py
│   ├── common
│   │   ├── __init__.py
│   │   ├── enums
│   │   │   ├── __init__.py
│   │   │   ├── action.py
│   │   │   ├── error.py
│   │   │   ├── jwt.py
│   │   │   └── order.py
│   │   ├── fn.py
│   │   ├── initializer.py
│   │   ├── times.py
│   │   └── types_.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   ├── app.py
│   │   │   ├── compilation.py
│   │   │   ├── message_broker.py
│   │   │   └── redis.py
│   │   ├── constants
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   ├── app.py
│   │   │   ├── celery.py
│   │   │   ├── message_broker.py
│   │   │   └── redis.py
│   │   ├── security.py
│   │   ├── tasks
│   │   │   ├── __init__.py
│   │   │   └── order.py
│   │   └── web.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── extensions
│   │   │   ├── __init__.py
│   │   │   └── datetime_utc.py
│   │   ├── migrations
│   │   │   ├── README
│   │   │   ├── __init__.py
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   │       └── 20250320010506_6b0923af6de2_initial.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── order.py
│   │   │   └── user.py
│   │   └── session.py
│   ├── infrastructure
│   │   ├── __init__.py
│   │   ├── message_broker
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   ├── consumer.py
│   │   │   └── message_fabric.py
│   │   └── redis
│   │       ├── __init__.py
│   │       └── order.py
│   ├── repository
│   │   ├── __init__.py
│   │   ├── abstract
│   │   │   ├── __init__.py
│   │   │   ├── order.py
│   │   │   └── user.py
│   │   └── alchemy
│   │       ├── __init__.py
│   │       ├── order.py
│   │       └── user.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── mappers
│   │   │   ├── __init__.py
│   │   │   └── order.py
│   │   ├── message.py
│   │   ├── order.py
│   │   ├── token.py
│   │   └── user.py
│   └── services
│       ├── __init__.py
│       ├── order.py
│       ├── order_processing.py
│       └── user.py
├── test.py
├── tests
│   └── __init__.py
└── uv.lock
```


### Запуск

Енвы из .env.example подойдут для тестового запуска
`make run_prod` затем после запуска `make upgrade`