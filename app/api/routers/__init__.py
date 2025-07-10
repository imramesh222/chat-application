from fastapi import FastAPI
from app.api.routers import auth_routes, user_routes, room_routes, message_routes, ws_routes,admin_analytics_routes

def include_routers(app):
    app.include_router(user_routes.router)
    app.include_router(room_routes.router)
    app.include_router(message_routes.router)
    app.include_router(auth_routes.router)
    app.include_router(ws_routes.router)
    app.include_router(admin_analytics_routes.router)