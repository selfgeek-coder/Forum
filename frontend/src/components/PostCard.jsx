import { useState } from "react";
import api from "../api/axios";

export default function PostCard({ post }) {
    const [likes, setLikes] = useState(post.likes_count);
    const [isLiked, setIsLiked] = useState(false); // В идеале статус должен приходить с бэкенда
    const [showComments, setShowComments] = useState(false);
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState("");

    // Логика лайков
    const handleLike = async () => {
        try {
            if (!isLiked) {
                const res = await api.post("/like/add", { post_id: post.id });
                setLikes(res.data.data.likes_count);
                setIsLiked(true);
            } else {
                await api.delete("/like/remove", { data: { post_id: post.id } });
                setLikes(prev => prev - 1);
                setIsLiked(false);
            }
        } catch (err) {
            alert(err.response?.data?.detail?.message || "Ошибка при обработке лайка");
        }
    };

    // Загрузка комментариев
    const toggleComments = async () => {
        if (!showComments && comments.length === 0) {
            try {
                const res = await api.get(`/comment/post/${post.id}`);
                setComments(res.data.data.comments);
            } catch (err) {
                console.error("Ошибка загрузки комментариев");
            }
        }
        setShowComments(!showComments);
    };

    // Отправка комментария
    const handleAddComment = async () => {
        if (!newComment.trim()) return;
        try {
            const res = await api.post("/comment/create", {
                post_id: post.id,
                content: newComment
            });
            setComments([res.data.data, ...comments]);
            setNewComment("");
        } catch (err) {
            alert("Не удалось отправить комментарий");
        }
    };

    return (
        <div className="news-card">
            <h3>{post.title}</h3>
            <p>{post.content}</p>
            <div className="news-footer">
                <span>Автор: {post.author}</span>
                <div className="news-actions">
                    <button 
                        className={`action-btn ${isLiked ? "liked" : ""}`} 
                        onClick={handleLike}
                    >
                        ❤️ {likes}
                    </button>
                    <button className="action-btn" onClick={toggleComments}>
                        💬 {post.comments_count}
                    </button>
                </div>
            </div>

            {showComments && (
                <div className="comments-section">
                    <div className="comment-form">
                        <input 
                            value={newComment}
                            onChange={(e) => setNewComment(e.target.value)}
                            placeholder="Напишите комментарий..."
                        />
                        <button onClick={handleAddComment}>Отправить</button>
                    </div>
                    <div className="comments-list">
                        {comments.map(c => (
                            <div key={c.id} className="comment-item">
                                <strong>{c.author_login}:</strong> {c.content}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}