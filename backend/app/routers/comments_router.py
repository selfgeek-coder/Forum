from fastapi import APIRouter, HTTPException, status, Depends, Query

from app.schemas import CommentCreate, CommentEdit, CommentDelete
from app.security import verify_token
from app.repositories.comment_repository import CommentRepository
from app.services.comment_service import CommentService

router = APIRouter(prefix="/api/comment", tags=["CRUD Comments API"])

comment_repository = CommentRepository()
comment_service = CommentService(comment_repository)


@router.post("/create")
def create_comment(comment: CommentCreate, current_user: dict = Depends(verify_token)):
    """Создает комментарий к посту"""

    try:
        result = comment_service.create_comment(
            comment.content, comment.post_id, current_user["user_id"]
        )

        return {
            "success": True,
            "message": "Комментарий успешно создан",
            "data": result
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при создании комментария"
            }
        )


@router.put("/edit")
def edit_comment(comment: CommentEdit, current_user: dict = Depends(verify_token)):
    """Изменяет комментарий по ID"""

    try:
        result = comment_service.update_comment(
            comment.comment_id, comment.content, current_user["user_id"]
        )

        return {
            "success": True,
            "message": "Комментарий успешно обновлен",
            "data": result
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при редактировании комментария"
            }
        )


@router.delete("/delete")
def delete_comment(comment: CommentDelete, current_user: dict = Depends(verify_token)):
    """Удаляет комментарий по ID"""

    try:
        result = comment_service.delete_comment(comment.comment_id, current_user["user_id"])

        return {
            "success": True,
            "message": "Комментарий успешно удален",
            "data": result
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при удалении комментария"
            }
        )


@router.get("/post/{post_id}")
def get_comments_by_post(post_id: int, page: int = 1, page_size: int = Query(default=20, ge=1, le=100)):
    """
    Получить все комментарии поста с пагинацией
    - post_id: ID поста
    - page: номер страницы (начинается с 1)
    - page_size: количество комментариев на странице (по умолчанию 20, максимум 100)
    """

    if page < 1:
        page = 1

    try:
        result = comment_service.get_comments_by_post(post_id, page, page_size)

        return {
            "success": True,
            "message": "Комментарии успешно получены",
            "data": result
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при получении комментариев"
            }
        )
