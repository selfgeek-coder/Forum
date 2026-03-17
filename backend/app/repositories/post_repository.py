from typing import Optional, List, Tuple

from sqlalchemy import func
from app.db.database import SessionLocal
from app.db.models import Post, User, Like

class PostRepository:
    @staticmethod
    def create_post(title: str, content: str, author_id: int) -> int:
        """Создать новый пост"""

        db = SessionLocal()
        try:
            post = Post(title=title, content=content, author_id=author_id)
            db.add(post)
            db.commit()
            db.refresh(post)
            return post.id
        finally:
            db.close()
    
    @staticmethod
    def get_post_by_id(post_id: int) -> Optional[Tuple]:
        """Получить пост по post_id: int"""

        db = SessionLocal()
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            if post:
                return (post.id, post.title, post.content, post.author_id)
            return None
        finally:
            db.close()
    
    @staticmethod
    def update_post(post_id: int, title: str, content: str) -> bool:
        """Обновить пост"""

        db = SessionLocal()
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            if post:
                post.title = title
                post.content = content
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    @staticmethod
    def delete_post(post_id: int) -> bool:
        """Удалить пост"""

        db = SessionLocal()
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            if post:
                db.delete(post)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    @staticmethod
    def get_posts_paginated(page: int, page_size: int) -> Tuple[List[Tuple], int, int]:
        """Получить посты с пагинацией"""

        db = SessionLocal()
        try:
            offset = (page - 1) * page_size

            total_posts = db.query(func.count(Post.id)).scalar()
            total_pages = (total_posts + page_size - 1) // page_size

            posts_query = db.query(
                Post.id,
                Post.title,
                Post.content,
                Post.created_at,
                User.login.label("author_name"),
                Post.likes_count,
                Post.comments_count
            ).join(User, Post.author_id == User.id).order_by(Post.created_at.desc()).offset(offset).limit(page_size)

            posts = [tuple(row) for row in posts_query.all()]
            return posts, total_posts, total_pages
        finally:
            db.close()