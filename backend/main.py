from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth_router import router as auth_router
from app.routers.posts_router import router as posts_router
from app.routers.comments_router import router as comments_router
from app.routers.likes_router import router as likes_router
from app.db.database import init_database

app = FastAPI(title="Social Network API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server & production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    init_database()
    
    app.include_router(auth_router)
    app.include_router(posts_router)
    app.include_router(comments_router)
    app.include_router(likes_router)
    
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)