from pydantic import BaseModel, EmailStr, field_validator, Field
import re


# --- USER ---
class UserRegister(BaseModel):
    email: EmailStr
    login: str
    name: str
    password: str

    @field_validator('login')
    @classmethod
    def validate_login(cls, v: str) -> str:
        v = v.strip()

        if len(v) < 3:
            raise ValueError('Логин должен содержать минимум 3 символа.')

        if ' ' in v:
            raise ValueError('Логин не должен содержать пробелы.')

        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Логин может содержать только буквы, цифры и _')

        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов.')

        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")

        if not re.search(r"[0-9]", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")

        return v


class UserLogin(BaseModel):
    email: EmailStr
    login: str
    password: str


# --- POST Base ---
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок поста")
    content: str = Field(..., min_length=1, max_length=10000, description="Содержание поста")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError('Заголовок не может быть пустым.')

        if len(v) < 3:
            raise ValueError('Заголовок должен содержать минимум 3 символа.')

        if not v[0].isupper():
            raise ValueError('Заголовок должен начинаться с заглавной буквы.')

        return v

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError('Содержание не может быть пустым.')

        if len(v) < 12:
            raise ValueError('Содержание должно быть не менее 12 символов.')

        return v


# --- Posts CRUD ---
class PostCreate(PostBase):
    pass


class PostEdit(PostBase):
    post_id: int


class PostDelete(BaseModel):
    post_id: int


# --- COMMENTS CRUD ---
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Текст комментария")

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError('Комментарий не может быть пустым.')

        if len(v) < 3:
            raise ValueError('Комментарий должен быть не менее 3 символов.')

        return v


class CommentCreate(CommentBase):
    post_id: int


class CommentEdit(CommentBase):
    comment_id: int


class CommentDelete(BaseModel):
    comment_id: int


class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# --- LIKES ---
class LikeCreate(BaseModel):
    post_id: int


class LikeDelete(BaseModel):
    post_id: int


class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: str

    class Config:
        from_attributes = True