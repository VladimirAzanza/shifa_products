
# 💊 Shifa Products

This is a work in progress of Shifa Products marketplace using Python-Django as backend with Bootstrapp Frontend.

Shifa Products is a Freelance project designed to sell medicinal products, Customers are allowed to:
  - 🌟 Leave reviews and rate products
  - 🏠 Add addresses
  - 📦 View order status
  - 🕒 Review order history
  - ✏️ Edit their profile
  - 🔑 Manage passwords
  - 📧 Login with Gmail
  - 💬 Live chat with the site administrator
  - 🔍 Search for products
  - 🖨️ Download order details in PDF format

To develop this project, I needed to understand concepts such as: MVT architecture, backend development, url routing, Object-Relation Mapping(Django ORM), static file management, Django templates and API communication.

### Key Features
 - Product Image Validation: All product images are validated for JPEG format and must meet the resolution requirement of 2000x2000 pixels. The resolution limit is set to balance visual quality with loading performance.
 - Optimized Image Storage: Product images are automatically optimized during upload, reducing file size without compromising quality, using compression and resizing techniques. By optimizing the images, we ensure faster delivery to the frontend, improving the website’s overall loading speed and user experience, especially for mobile users or slow connections.
 - Product Search Functionality: Users can search for products using keywords related to the product name, description, or category name/slug. The search is case-insensitive and ensures that only available products are displayed in the results.

## ⚙️ Installation

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

  #Google social login
  #For more info visit: https://docs.allauth.org/en/latest/index.html
  CLIENT_ID=google-id-credential
  SECRET=google-secret-credential
```
Finally, run the project with:
```bash
  python manage.py runserver
```

## 📜 Logging Configuration

In Shifa Products, a logging system has been set up to track important events, errors, and activities within the project. This is configured in settings.py. Here’s how the logging system works and how you can access the logs:

The logging system is configured using a dictionary called LOGGING. 

- Handlers: Defines where the log messages should go. In this case, there are two handlers:

  - 📂 File Handler: Logs messages to a file (shifa_products/logs/debug.log).
  - 🖥️ Console Handler: Logs messages to the console.

- Formatters: Specifies how the log messages should be formatted.
- Loggers: Configures the loggers for specific parts of the project:

  - 🐍 django: Logs Django-related events to a file.
  - 🤖 telegram_notifications: Logs related to order telegram notifications.


## 📨 Tawk.to Webhook

This project integrates a Tawk.to webhook to receive notifications of events related to chats on the Tawk.to platform. The captured events include when a chat is started or ended. When one of these events is received, a notification is sent to a Telegram bot with details of the chat, such as the visitor's name and country.

### 🔗 Configure the webhook URL

Go to your Tawk.to account settings:
- 🌐 In the Webhooks section, add the URL of the webhook for your application.
- 🔄 Make sure the events you want to receive, such as "Chat Start" and "Chat End," are enabled.

When a chat is started or ended on Tawk.to, a notification will be sent to the Telegram bot in the following format, which is defined in shifa_products.constants.py:

```css
TELEGRAM_TAWKTO_MESSAGE = (
    '🚀 Chat {status} en Tawk.to\n'
    '👤 Usuario: {visitor_name}\n'
    '🌍 País: {visitor_country}\n'
)
```

## 🧪 Testing with Pytest

Shifa Products includes tests using Pytest to ensure that key functionalities of the system behave correctly. The tests are located in the shifa_products/tests/pytest_tests/ directory and currently focus on verifying the URLs of various endpoints. As the project evolves, more tests will be added to cover other aspects.

### 🏃‍♂️ Running the tests

To run the tests, simply execute the following command from the directory where pytest.ini is located:

```bash
pytest
```
By default, Pytest will search for any test files in the tests/pytest_tests/ directory and run them.

### 💡 Tips for running tests

- You can run specific test files or test functions by specifying their names:
```bash
pytest tests/pytest_tests/test_routes.py
```

### 💻 Generating the Model Diagram (models.png)

To generate a diagram of the models used in the project, you can use the Django Extensions package, which provides a command to create a visual representation of your models. Follow these steps:

```bash
pip install django-extensions
```

Add django-extensions to your INSTALLED_APPS: Open the settings.py file and add 'django_extensions' to your INSTALLED_APPS list.

INSTALLED_APPS = [
    ...
    'django_extensions',
]

Generate the Model Diagram: Once everything is installed, you can generate the diagram by running the following command:
```bash
python manage.py graph_models -a -g -o static/diagrams/models.png
```
View the Diagram: You can now view the diagram at static/diagrams/models.png. This file will show how the models in the project are related to each other.
## 🛠 Skills
Python, Django, Bootstrap, CSS, HTML
