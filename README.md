
# Shifa Products

This is a work in progress of Shifa Products marketplace using Python-Django as backend with Bootstrapp Frontend.

Shifa Products is an Freelance project designed to sell medicinal products, Customers are allowed to:
  - Leave reviews and rate products
  - Add addresses
  - View order status
  - Review order history
  - Edit their profile
  - Manage passwords

To write this project, I needed to understand concepts such as: MVT architecture, backend development, url routing, Object-Relation Mapping(Django ORM), static files management, Django templates.


## Installation

Cloning the repository:

```bash
   git@github.com:VladimirAzanza/shifa_products.git
   cd shifa_products
```

Activate virtual environment (Linux):

```bash
  python -m venv ./venv
  source .venv/bin/activate
```
next, install dependencies:
```bash
  pip install -r requirements.txt
```
migrate:
```bash
  python manage.py migrate
```
Create env file -> .env:
```bash
  touch .env
```
Environment variables (You have an example at .env.example):
```bash
    # Django env
  SECRET_KEY=django-secret-key
  DEBUG=False
  ALLOWED_HOSTS=localhost 127.0.0.1
  CSRF_TRUSTED_ORIGINS=https://domain

  # Telegram env
  TELEGRAM_TOKEN=Here your telegram bot token from Bot Father
  TELEGRAM_CHAT_ID=Here the chat id from getUserInfo

  # DB variables at settings.py:
  DB_ENGINE=PostgreSQL or SQLite
  POSTGRES_DB=shifa_products
  POSTGRES_USER=administrator
  POSTGRES_PASSWORD=password
  DB_HOST=db
  DB_PORT=5432
```
Finally, run the project with:
```bash
  python manage.py runserver
```


## 🛠 Skills
Python, Django, Bootstrap
