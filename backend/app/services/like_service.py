from fastapi import HTTPException, status

from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository


class LikeService:
    def __init__(self, like_repository: LikeRepository, post_repository: PostRepository):
        self.like_repository = like_repository
        self.post_repository = post_repository
    
    def add_like(self, user_id: int, post_id: int):
        """Добавить лайк к посту"""

        post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )
        

        if self.like_repository.has_user_liked(user_id, post_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ALREADY_LIKED",
                    "message": "Вы уже лайкнули этот пост"
                }
            )
        
        success = self.like_repository.add_like(user_id, post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "LIKE_FAILED",
                    "message": "Не удалось добавить лайк"
                }
            )

        updated_post = self.post_repository.get_post_by_id(post_id)
        _, _, _, author_id = updated_post

        from sqlalchemy import func
        from app.db.database import SessionLocal
        from app.db.models import Post
        
        db = SessionLocal()
        try:
            post_obj = db.query(Post).filter(Post.id == post_id).first()
            likes_count = post_obj.likes_count if post_obj else 0
        finally:
            db.close()
        
        return {
            "post_id": post_id,
            "liked": True,
            "likes_count": likes_count
        }
    
    def remove_like(self, user_id: int, post_id: int):
        """Удалить лайк с поста"""

        post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )

        if not self.like_repository.has_user_liked(user_id, post_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "NOT_LIKED",
                    "message": "Вы не лайкнули этот пост"
                }
            )

        success = self.like_repository.remove_like(user_id, post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "UNLIKE_FAILED",
                    "message": "Не удалось удалить лайк"
                }
            )

        from sqlalchemy import func
        from app.db.database import SessionLocal
        from app.db.models import Post
        
        db = SessionLocal()
        try:
            post_obj = db.query(Post).filter(Post.id == post_id).first()
            likes_count = post_obj.likes_count if post_obj else 0
        finally:
            db.close()
        
        return {
            "post_id": post_id,
            "liked": False,
            "likes_count": likes_count
        }
    
    def get_likes_count(self, post_id: int):
        """Получить количество лайков на посте"""

        post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )
        
        likes_count = self.like_repository.get_likes_count(post_id)
        
        return {
            "post_id": post_id,
            "likes_count": likes_count
        }
