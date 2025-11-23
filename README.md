# Todo Python Django

> 🎓 **Part of the AI Coding Bootcamp** - A hands-on project to learn Django web development with AI assistance

A feature-rich todo application built with Python and Django, featuring modern UI design, comprehensive testing, and full CRUD operations.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- 📅 Due date assignment and tracking
- ✓ Mark todos as complete/resolved
- 🎨 Modern glassmorphism UI with animations
- 🏷️ Categories and tags support
- ⚡ Priority levels (Low, Medium, High, Urgent)
- 🧪 Comprehensive test suite (38 tests)
- 🎯 Overdue detection

## Installation

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/BuraYu/todo-python-v.git
cd todo-python-django
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Run migrations:
```bash
uv run python manage.py migrate
```

4. Start the development server:
```bash
uv run python manage.py runserver
```

5. Open your browser and navigate to `http://127.0.0.1:8000`

### Running Tests

```bash
uv run python manage.py test todo
```

## Usage

- **Add Todo**: Click "+ Add New Todo" button
- **Edit Todo**: Click the "Edit" button on any todo
- **Complete**: Use "Done" button to mark todos complete
- **Delete**: Click "Delete" button (with confirmation)
- **Admin Panel**: Access Django admin at `/admin/` (requires superuser)

### Create Superuser

```bash
uv run python manage.py createsuperuser
```

## Project Structure

```
todo-python-django/
├── mysite/              # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI config
├── todo/                # Todo app
│   ├── models.py        # Database models
│   ├── views.py         # Business logic
│   ├── urls.py          # App URL patterns
│   ├── admin.py         # Admin configuration
│   ├── tests.py         # Test suite
│   └── templates/       # HTML templates
│       └── todo/
│           ├── home.html    # Todo list view
│           └── base.html    # Form template
├── manage.py            # Django management script
└── pyproject.toml       # Dependencies (uv)
```

## Technologies Used

- **Python 3.13** - Programming language
- **Django 5.2.8** - Web framework
- **SQLite** - Database
- **uv** - Fast Python package manager
- **HTML/CSS** - Modern glassmorphism UI

## What I Learned

This project was built as part of an AI Coding Bootcamp to learn:
- Django's MTV (Model-Template-View) architecture
- Database modeling with Django ORM
- CRUD operations and URL routing
- Template rendering and forms
- Writing comprehensive tests
- Modern CSS with glassmorphism effects

## License

MIT