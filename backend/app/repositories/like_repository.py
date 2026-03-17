from typing import Optional
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.db.database import SessionLocal
from app.db.models import Like, Post


class LikeRepository:
    @staticmethod
    def add_like(user_id: int, post_id: int) -> bool:
        """Добавить лайк для поста"""
        db = SessionLocal()
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            if not post:
                return False
            
            like = Like(user_id=user_id, post_id=post_id)
            db.add(like)
            
            post.likes_count += 1
            
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return False
        finally:
            db.close()

    @staticmethod
    def remove_like(user_id: int, post_id: int) -> bool:
        """Удалить лайк с поста"""
        db = SessionLocal()
        try:
            like = db.query(Like).filter(
                Like.user_id == user_id,
                Like.post_id == post_id
            ).first()
            
            if like:
                db.delete(like)
                
                post = db.query(Post).filter(Post.id == post_id).first()
                if post and post.likes_count > 0:
                    post.likes_count -= 1
                
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def has_user_liked(user_id: int, post_id: int) -> bool:
        """Проверить, лайкнул ли пользователь пост"""
        db = SessionLocal()
        try:
            like = db.query(Like).filter(
                Like.user_id == user_id,
                Like.post_id == post_id
            ).first()
            return like is not None
        finally:
            db.close()

    @staticmethod
    def get_likes_count(post_id: int) -> int:
        """Получить количество лайков на посте"""
        db = SessionLocal()
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            return post.likes_count if post else 0
        finally:
            db.close()

    @staticmethod
    def get_post_likes(post_id: int) -> list:
        """Получить все лайки поста"""
        db = SessionLocal()
        try:
            likes = db.query(Like).filter(Like.post_id == post_id).all()
            return likes
        finally:
            db.close()
