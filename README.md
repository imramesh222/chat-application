# Chat Application API

A modern chat application backend built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  
Database migrations are managed with **Liquibase**.

## Features

- User authentication (JWT-based)
- User registration and profile management
- Room creation (with per-room admin/owner)
- Messaging within rooms
- Role-based access (global admin, per-room admin)
- RESTful API with interactive Swagger UI

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd chat-application
```

### 2. Set up your environment

- Create a `.env` file with your database and secret settings.
- Install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up the database

- Configure your PostgreSQL connection in `.env` and `liquibase/liquibase.properties`.
- Run migrations:

```bash
cd liquibase
liquibase update
```

### 4. Start the application

```bash
./start_service.sh
```

### 5. Access the API

- Open [http://localhost:8002/docs](http://localhost:8002/docs) for Swagger UI.

## Project Structure

- `app/` - Main FastAPI application code
- `liquibase/` - Database migration scripts
- `requirements.txt` - Python dependencies

## License

MIT

---

**Happy chatting!**
