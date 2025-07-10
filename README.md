# Chat Application Backend

A real-time chat backend built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **WebSockets**. Supports JWT authentication, user/room/message management, role-based access (global admin and per-room admin), and persistent chat history.

---

## Features

- **User Authentication**: JWT-based login and protected endpoints.
- **User Management**: Signup, update, password change, and user listing.
- **Room Management**: Create, update, delete, and list chat rooms. Room creator is the admin.
- **Message Management**: Send and fetch messages in rooms. All messages are persisted in the database.
- **WebSocket Chat**: Real-time messaging in rooms, protected by JWT.
- **Role-Based Access**: Global admin and per-room admin logic for room operations.
- **Swagger UI**: API docs and testing at `/docs`.

---

## Admin & Analytics Features

- **Admin Dashboard**: Web-based admin dashboard at `/admin` using SQLAdmin. Manage users, rooms, and messages with a modern UI.
- **RBAC Protection**: Only users with `role="admin"` can access the admin dashboard.
- **Admin Login**: Login to the dashboard with your admin email and password.
- **Analytics Endpoints**: 
  - `/admin/analytics/messages-per-room`: Get message counts per room (with optional date filters).
  - `/admin/analytics/user-activity`: Get message counts per user (with optional date filters).
- **CSV Export**: Add `?format=csv` to analytics endpoints to download results as CSV files for use in Excel, Google Sheets, etc.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd chat-application
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** The following dependencies are required for admin and analytics features:
- `sqladmin`
- `itsdangerous`

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
SERVICE_PORT=8003
SECRET_KEY=15d8f5f31c97b88........
DATABASE_URL=postgresql://postgres:password@localhost:5432/your_database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_NAME=your database
DATABASE_PASSWORD=your password
CHUNK_SIZE=512
```

### 5. Run Database Migrations
```bash
cd liquibase
liquibase update
cd ..
```

### 6. Start the Service
```bash
./start_service.sh
```

---

## API Usage

### **Authentication**
- `POST /auth/login` — Login, returns JWT token and user info.
- `POST /auth/token` — Login, returns only session info.
- Use the `access_token` from the response for all protected endpoints.

### **User Endpoints**
- `POST /user/signup` — Register a new user.
- `GET /user/users` — List users (admin only).
- `PUT /user/update/{user_id}` — Update user info.
- `POST /user/update_password` — Change password.

### **Room Endpoints**
- `POST /room/` — Create a room (authenticated user becomes admin).
- `GET /room/rooms` — List rooms (admin sees all, user sees their own).
- `GET /room/{room_id}` — Get room details.
- `PATCH /room/{room_id}` — Update room (admin only).
- `DELETE /room/{room_id}` — Delete room (admin only).

### **Message Endpoints**
- `POST /message/rooms/{room_id}/messages` — Send message to a room.
- `GET /message/rooms/{room_id}/messages` — List messages in a room.

### **WebSocket Chat**
- **Endpoint:** `ws://localhost:8003/ws/{room_id}?token=YOUR_JWT_TOKEN`
- **How to use:**
  1. Login and get a JWT token.
  2. Connect to the WebSocket endpoint with the token as a query parameter.
  3. Send plain text messages. All connected clients in the room receive the message.
  4. All messages are saved to the `messages` table.

---

## Current Limitations
- **No room membership management:** Any authenticated user can send messages to any room if they know the room ID. There is no way for a room admin to add/remove users from a room.
- **No private/direct messaging:** All messages are public within a room.
- **No message editing/deletion:** Once sent, messages cannot be edited or deleted.

---

## Development & Debugging
- Use print/log statements in your WebSocket handler for debugging.
- Check `service.log` and `logs/uvicorn.log` for errors.
- Use pgAdmin or psql to inspect the database.

---

## License
MIT
