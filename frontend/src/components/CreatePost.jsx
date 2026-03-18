import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import "../styles/createPost.css";

export default function CreatePost() {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const handleCreatePost = async () => {
        if (!title.trim() || !content.trim()) {
            setError("Введите заголовок и текст поста.");
            return;
        }

        setLoading(true);
        setError("");

        try {
            await api.post("/post/create", { title, content });
            alert("Пост успешно создан!");
            setTitle("");
            setContent("");
            navigate("/"); // можно оставить, чтобы вернуться на главную
        } catch (err) {
            setError("Ошибка при создании поста.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="create-post-page">
            <h2>Создать новый пост</h2>

            <input
                className="create-post-input"
                placeholder="Заголовок"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />

            <textarea
                className="create-post-textarea"
                placeholder="Текст поста"
                value={content}
                onChange={(e) => setContent(e.target.value)}
            />

            {error && <p className="create-post-error">{error}</p>}

            <button
                className="create-post-button"
                onClick={handleCreatePost}
                disabled={loading}
            >
                {loading ? "Создание..." : "Создать пост"}
            </button>
        </div>
    );
}