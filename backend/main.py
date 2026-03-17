from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.posts_router import router as posts_router
from app.routers.comments_router import router as comments_router
from app.routers.likes_router import router as likes_router
from app.db.database import init_database

init_database()

app = FastAPI(title="Social Network API")

app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)