from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from app.repo.user_repo import UserRepo
from app.repo.datasource import DataSource
from app.utils.hashing import Hash
from app.utils.auth import get_current_user
from app.model.user_record import UserRecord
from app.model.room_record import RoomRecord
from app.model.message_record import MessageRecord
from starlette.middleware.sessions import SessionMiddleware

class AdminAuthBackend(AuthenticationBackend):
    def __init__(self):
        super().__init__(secret_key="supersecret")
        self.user_repo = UserRepo(DataSource())

    async def authenticate(self, request: Request):
        # Check session
        user_id = request.session.get("user")
        if user_id:
            user_record = self.user_repo.get_user_by_id(user_id)
            if user_record and user_record.role == "admin":
                return user_record
        return None

    async def login(self, request: Request):
        form = await request.form()
        email = form.get("username")
        password = form.get("password")
        user_record = self.user_repo.get_user_by_email(email)
        if user_record and user_record.role == "admin" and Hash.verify(password, user_record.password):
            # Set session
            request.session["user"] = str(user_record.id)
            response = RedirectResponse(url="/admin", status_code=302)
            return response
        return RedirectResponse(url="/admin/login", status_code=302)

    async def logout(self, request: Request):
        response = RedirectResponse(url="/admin/login", status_code=302)
        # Optionally, clear session/cookie here
        return response

def setup_admin(app):
    db = DataSource()
    engine = db.engine

    class UserAdmin(ModelView, model=UserRecord):
        column_list = [
            "id",
            "username",
            "email",
            "role",
            "full_name",
            "phone",
            "created_at"
        ]
        name = "User"
        name_plural = "Users"

    class RoomAdmin(ModelView, model=RoomRecord):
        column_list = [
            "id",
            "name",
            "description",
            "admin_id",
            "created_at"
        ]
        name = "Room"
        name_plural = "Rooms"

    class MessageAdmin(ModelView, model=MessageRecord):
        column_list = [
            "id",
            "content",
            "user_id",
            "room_id",
            "created_at"
        ]
        name = "Message"
        name_plural = "Messages"

    admin = Admin(app, engine, authentication_backend=AdminAuthBackend())
    admin.add_view(UserAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(MessageAdmin)
