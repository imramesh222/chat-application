from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.routers import include_routers
from app.settings import Settings
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from app.admin_dashboard import setup_admin

# from app.repo.datasource import DataSource
# from sqlalchemy import text

# db = DataSource()
# session = db.get_session()
# print(session.execute(text("SELECT 1")).fetchall())
# session.close()
# # Create tables



app = FastAPI(title="CHAT-APPLICATION API", version="1.0.0")
setup_admin(app)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    print("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )
settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins = list(settings.ALLOW_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="supersecret")

include_routers(app)


@app.get("/")
async def hc():
    return {"error": False, "msg": "Ok", "result": {"status": "SERVING"}}
