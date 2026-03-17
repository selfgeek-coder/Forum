from typing import Optional, List, Tuple

from sqlalchemy import func
from app.db.database import SessionLocal
from app.db.models import Comment, User, Post


class CommentRepository:
    @staticmethod
    def create_comment(content: str, post_id: int, user_id: int) -> int:
        """Создать новый комментарий"""

        db = SessionLocal()
        try:
            comment = Comment(content=content, post_id=post_id, user_id=user_id)
            db.add(comment)
            db.commit()
            db.refresh(comment)
            return comment.id
        finally:
            db.close()

    @staticmethod
    def get_comment_by_id(comment_id: int) -> Optional[Tuple]:
        """Получить комментарий по comment_id"""

        db = SessionLocal()
        try:
            comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if comment:
                return (comment.id, comment.content, comment.post_id, comment.user_id, comment.created_at, comment.updated_at)
            return None
        finally:
            db.close()

    @staticmethod
    def update_comment(comment_id: int, content: str) -> bool:
        """Обновить комментарий"""

        db = SessionLocal()
        try:
            comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if comment:
                comment.content = content
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """Удалить комментарий"""

        db = SessionLocal()
        try:
            comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if comment:
                db.delete(comment)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get_comments_by_post(post_id: int, page: int = 1, page_size: int = 20) -> Tuple[List[Tuple], int, int]:
        """Получить комментарии поста с пагинацией"""

        db = SessionLocal()
        try:
            offset = (page - 1) * page_size

            total_comments = db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar()
            total_pages = (total_comments + page_size - 1) // page_size

            comments_query = db.query(
                Comment.id,
                Comment.content,
                Comment.post_id,
                Comment.user_id,
                Comment.created_at,
                Comment.updated_at,
                User.login.label("author_name")
            ).join(User, Comment.user_id == User.id).filter(
                Comment.post_id == post_id
            ).order_by(Comment.created_at.desc()).offset(offset).limit(page_size)

            comments = [tuple(row) for row in comments_query.all()]
            return comments, total_comments, total_pages
        finally:
            db.close()

    @staticmethod
    def get_post_exists(post_id: int) -> bool:
        """Проверить, существует ли пост"""

        db = SessionLocal()
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            return post is not None
        finally:
            db.close()
