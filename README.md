# Todo Python Django

A simple todo application built with Python and Django.

## Features

- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- Clean and intuitive interface

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-python-django
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

- Add new todos using the input form
- Click on todos to mark them as complete
- Delete todos using the delete button

## Technologies Used

- Python
- Django
- SQLite

## License

MIT