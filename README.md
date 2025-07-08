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

## API Endpoints

### **Authentication**
- `POST /auth/login` — User login, returns JWT token
- `POST /auth/logout` — User logout

### **Users**
- `POST /user/signup` — Register a new user
- `GET /user/users` — List all users (admin only)
- `GET /user/{user_id}` — Get user by ID (admin only)
- `PUT /user/update/{user_id}` — Update user info (admin only)
- `POST /user/update_password` — Change own password (authenticated)

### **Rooms**
- `POST /room/` — Create a room (any authenticated user; creator becomes room admin)
- `GET /room/rooms` — List all rooms (authenticated)
- `GET /room/{room_id}` — Get room by ID (authenticated)
- `PATCH /room/{room_id}` — Update room (room admin or global admin)
- `DELETE /room/{room_id}` — Delete room (room admin or global admin)

### **Messages**
- `POST /message/rooms/{room_id}/messages` — Send a message in a room (authenticated)
- `GET /message/rooms/{room_id}/messages` — List messages in a room (authenticated)

## Business Logic Overview

- **Authentication:**
  - JWT-based. All protected endpoints require a valid token.
  - Only admins can manage users globally.

- **User Management:**
  - Users can sign up and update their own password.
  - Admins can view, update, and delete any user.

- **Room Management:**
  - Any authenticated user can create a room; they become the room's admin (owner).
  - Only the room admin (or a global admin) can update or delete the room.
  - All authenticated users can view rooms and join them.

- **Messaging:**
  - Authenticated users can send and view messages in rooms they have access to.
  - Messages are linked to both the user and the room.

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
