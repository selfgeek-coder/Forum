from fastapi import HTTPException, status

from app.repositories.post_repository import PostRepository

class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    def create_post(self, title: str, content: str, author_id: int):
        """Создать пост"""

        post_id = self.post_repository.create_post(title, content, author_id)
        
        return {
            "post_id": post_id,
            "title": title,
            "content": content,
            "author_id": author_id
        }
    
    def update_post(self, post_id: int, title: str, content: str, current_user_id: int):
        """Обновить пост"""

        post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )
        
        _, _, _, author_id = post
        
        if author_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "FORBIDDEN",
                    "message": "Вы можете редактировать только свои посты"
                }
            )
        
        success = self.post_repository.update_post(post_id, title, content)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "UPDATE_FAILED",
                    "message": "Не удалось обновить пост"
                }
            )
        
        return {
            "post_id": post_id,
            "title": title,
            "content": content
        }
    
    def delete_post(self, post_id: int, current_user_id: int):
        """Удалить пост"""
        
        post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )
        
        _, _, _, author_id = post
        
        if author_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "FORBIDDEN",
                    "message": "Вы можете удалять только свои посты"
                }
            )
        
        success = self.post_repository.delete_post(post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "DELETE_FAILED",
                    "message": "Не удалось удалить пост"
                }
            )
        
        return {
            "post_id": post_id
        }
    
    def get_news(self, page: int, page_size: int, current_user_id: int | None = None):
        """Получить новости с пагинацией"""

        posts, total_posts, total_pages = self.post_repository.get_posts_paginated(
            page, page_size
        )

        liked_post_ids: set[int] = set()
        if current_user_id is not None:
            post_ids = [p[0] for p in posts]
            liked_post_ids = self.post_repository.get_user_liked_post_ids(current_user_id, post_ids)
        
        news_list = []
        for post in posts:
            post_id, title, content, created_at, author_name, author_id, likes_count, comments_count = post
            news_list.append({
                "id": post_id,
                "title": title,
                "content": content,
                "created_at": created_at,
                "author": author_name,
                "author_id": author_id,
                "likes_count": likes_count,
                "comments_count": comments_count,
                "is_liked": post_id in liked_post_ids,
                "comments": []
            })
        
        return {
            "posts": news_list,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_posts": total_posts,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }

    def get_post(self, post_id: int, current_user_id: int | None = None):
        """Получить один пост по ID (публично, is_liked — если авторизован)."""
        row = self.post_repository.get_post_details(post_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "POST_NOT_FOUND",
                    "message": "Пост не найден"
                }
            )

        (
            pid,
            title,
            content,
            created_at,
            author_name,
            author_id,
            likes_count,
            comments_count,
        ) = row

        is_liked = False
        if current_user_id is not None:
            liked = self.post_repository.get_user_liked_post_ids(current_user_id, [pid])
            is_liked = pid in liked

        return {
            "id": pid,
            "title": title,
            "content": content,
            "created_at": created_at,
            "author": author_name,
            "author_id": author_id,
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": is_liked,
            "comments": []
        }