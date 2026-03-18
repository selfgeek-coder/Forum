from fastapi import HTTPException, status

from app.repositories.comment_repository import CommentRepository


class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def create_comment(self, content: str, post_id: int, user_id: int):
        """Создать комментарий"""

        if not self.comment_repository.get_post_exists(post_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )

        comment_id = self.comment_repository.create_comment(content, post_id, user_id)
        created = self.comment_repository.get_comment_with_author(comment_id)
        if not created:
            return {
                "id": comment_id,
                "content": content,
                "post_id": post_id,
                "user_id": user_id,
                "created_at": "",
                "updated_at": "",
                "author_login": "",
            }

        return {
            "id": created[0],
            "content": created[1],
            "post_id": created[2],
            "user_id": created[3],
            "created_at": str(created[4]),
            "updated_at": str(created[5]),
            "author_login": created[6],
        }

    def update_comment(self, comment_id: int, content: str, current_user_id: int):
        """Обновить комментарий"""

        comment = self.comment_repository.get_comment_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "COMMENT_NOT_FOUND",
                    "message": "Комментарий не найден"
                }
            )

        _, _, _, user_id, _, _ = comment

        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "FORBIDDEN",
                    "message": "Вы можете редактировать только свои комментарии"
                }
            )

        success = self.comment_repository.update_comment(comment_id, content)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "UPDATE_FAILED",
                    "message": "Не удалось обновить комментарий"
                }
            )

        return {
            "comment_id": comment_id,
            "content": content
        }

    def delete_comment(self, comment_id: int, current_user_id: int):
        """Удалить комментарий"""

        comment = self.comment_repository.get_comment_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "COMMENT_NOT_FOUND",
                    "message": "Комментарий не найден"
                }
            )

        _, _, _, user_id, _, _ = comment

        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "FORBIDDEN",
                    "message": "Вы можете удалять только свои комментарии"
                }
            )

        success = self.comment_repository.delete_comment(comment_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "DELETE_FAILED",
                    "message": "Не удалось удалить комментарий"
                }
            )

        return {
            "comment_id": comment_id
        }

    def get_comments_by_post(self, post_id: int, page: int = 1, page_size: int = 20):
        """Получить комментарии поста"""

        if not self.comment_repository.get_post_exists(post_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )

        if page < 1:
            page = 1

        comments, total_comments, total_pages = self.comment_repository.get_comments_by_post(
            post_id, page, page_size
        )

        return {
            "comments": [
                {
                    "id": comment[0],
                    "content": comment[1],
                    "post_id": comment[2],
                    "user_id": comment[3],
                    "created_at": str(comment[4]),
                    "updated_at": str(comment[5]),
                    "author_login": comment[6]
                }
                for comment in comments
            ],
            "total_comments": total_comments,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
