# Doubt Solver Backend

A general-purpose online doubt-solving platform backend built with Django and Django REST Framework. Initially focused on GMAT, but architected for extensibility to other subjects.

## Features
- User registration, login, and profile APIs
- Submit a question and get an AI-generated answer (OpenAI GPT-3.5-turbo)
- PostgreSQL database support
- Extensible for multiple subjects

## Setup Instructions

1. **Clone the repository and create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Configure environment variables:**
    - Create a `.env` file in the root directory with:
      ```env
      DEBUG=True
      SECRET_KEY=your-secret-key
      OPENAI_API_KEY=your-openai-api-key
      DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
      ```

3. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

4. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

5. **API Endpoints:**
    - `POST /users/register/` — Register a new user
    - `POST /users/login/` — Login and get token
    - `GET /users/profile/` — Get user profile (auth required)
    - `POST /qa/ask/` — Submit a question (auth required)

## Notes
- Uses Token Authentication (DRF)
- Requires PostgreSQL for production
- See code for further extensibility 