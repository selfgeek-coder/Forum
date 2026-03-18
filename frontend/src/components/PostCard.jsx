import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import Modal from "./Modal";

export default function PostCard({ post, auth, onDeleted, showFull = false }) {
    const [likes, setLikes] = useState(post.likes_count);
    const [isLiked, setIsLiked] = useState(Boolean(post.is_liked));
    const [commentsCount, setCommentsCount] = useState(post.comments_count);
    const [showComments, setShowComments] = useState(false);
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState("");
    const [commentsLoading, setCommentsLoading] = useState(false);
    const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false);
    const [deleteLoading, setDeleteLoading] = useState(false);

    const isAuthed = Boolean(auth?.isAuthenticated);
    const isOwner = useMemo(() => {
        const userId = auth?.userId;
        return Boolean(isAuthed && userId && post.author_id === userId);
    }, [auth?.userId, isAuthed, post.author_id]);

    // Логика лайков
    const handleLike = async () => {
        if (!isAuthed) return;
        try {
            if (!isLiked) {
                const res = await api.post("/like/add", { post_id: post.id });
                setLikes(res.data.data.likes_count);
                setIsLiked(true);
            } else {
                const res = await api.delete("/like/remove", { data: { post_id: post.id } });
                setLikes(res.data.data.likes_count);
                setIsLiked(false);
            }
        } catch (err) {
            alert(err.response?.data?.detail?.message || "Ошибка при обработке лайка");
        }
    };

    // Загрузка комментариев
    const toggleComments = async () => {
        if (!isAuthed) return;
        if (!showComments && comments.length === 0) {
            try {
                setCommentsLoading(true);
                const res = await api.get(`/comment/post/${post.id}`);
                setComments(res.data.data.comments);
            } catch (err) {
                console.error("Ошибка загрузки комментариев");
            } finally {
                setCommentsLoading(false);
            }
        }
        setShowComments(!showComments);
    };

    // На странице поста: подгружаем и открываем комментарии автоматически
    useEffect(() => {
        if (!showFull) return;
        if (!isAuthed) return;
        if (showComments) return;
        if (comments.length > 0) return;

        (async () => {
            try {
                setCommentsLoading(true);
                const res = await api.get(`/comment/post/${post.id}`);
                setComments(res.data.data.comments);
                setShowComments(true);
            } catch {
                // no-op
            } finally {
                setCommentsLoading(false);
            }
        })();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [showFull, isAuthed, post.id]);

    // Отправка комментария
    const handleAddComment = async () => {
        if (!isAuthed) return;
        if (!newComment.trim()) return;
        try {
            const res = await api.post("/comment/create", {
                post_id: post.id,
                content: newComment
            });
            setComments([res.data.data, ...comments]);
            setCommentsCount((prev) => prev + 1);
            setNewComment("");
        } catch (err) {
            alert("Не удалось отправить комментарий");
        }
    };

    const handleDelete = async () => {
        if (!isOwner) return;
        setDeleteLoading(true);
        try {
            await api.delete("/post/delete", { data: { post_id: post.id } });
            setConfirmDeleteOpen(false);
            onDeleted?.(post.id);
        } catch (err) {
            alert(err.response?.data?.detail?.message || "Не удалось удалить пост");
        } finally {
            setDeleteLoading(false);
        }
    };

    return (
        <div className="news-card">
            <div className="news-card__meta">
                <span className="news-card__author">Автор: {post.author}</span>
                {post.created_at ? <span className="news-card__date">{new Date(post.created_at).toLocaleString()}</span> : null}
            </div>
            <h3 className="news-card__title">
                <Link className="md-link" to={`/post/${post.id}`}>{post.title}</Link>
            </h3>
            <p>{showFull ? post.content : (post.content && post.content.length > 260 ? `${post.content.slice(0, 260)}…` : post.content)}</p>
            <div className="news-footer">
                {isOwner ? (
                    <button className="md-text-btn md-text-btn--danger" onClick={() => setConfirmDeleteOpen(true)}>
                        <span className="material-symbols-outlined" aria-hidden="true">
                            delete
                        </span>
                        Удалить
                    </button>
                ) : (
                    <span />
                )}
                <div className="news-actions">
                    <button 
                        className={`action-btn ${isLiked ? "liked" : ""}`} 
                        onClick={handleLike}
                        disabled={!isAuthed}
                        title={!isAuthed ? "Войдите, чтобы ставить лайки" : undefined}
                    >
                        <span className="material-symbols-outlined" aria-hidden="true">
                            favorite
                        </span>
                        {likes}
                    </button>
                    <button
                        className="action-btn"
                        onClick={toggleComments}
                        disabled={!isAuthed}
                        title={!isAuthed ? "Войдите, чтобы читать и писать комментарии" : undefined}
                    >
                        <span className="material-symbols-outlined" aria-hidden="true">
                            chat_bubble
                        </span>
                        {commentsCount}
                    </button>
                </div>
            </div>

            {showFull && showComments && (
                <div className="comments-section">
                    <div className="comment-form">
                        <input 
                            value={newComment}
                            onChange={(e) => setNewComment(e.target.value)}
                            placeholder="Напишите комментарий..."
                        />
                        <button className="btn btn--primary btn--sm" onClick={handleAddComment}>Отправить</button>
                    </div>
                    <div className="comments-list">
                        {commentsLoading && <div className="muted">Загрузка комментариев...</div>}
                        {comments.map(c => (
                            <div key={c.id} className="comment-item">
                                <strong>{c.author_login}:</strong> {c.content}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <Modal
                open={confirmDeleteOpen}
                title="Удалить пост?"
                onClose={() => (deleteLoading ? null : setConfirmDeleteOpen(false))}
                footer={
                    <div className="md-modal__actions">
                        <button className="btn btn--secondary" onClick={() => setConfirmDeleteOpen(false)} disabled={deleteLoading}>
                            Отмена
                        </button>
                        <button className="btn btn--primary" onClick={handleDelete} disabled={deleteLoading}>
                            {deleteLoading ? "Удаление..." : "Удалить"}
                        </button>
                    </div>
                }
            >
                <div className="muted">
                    Вы уверены, что хотите удалить пост?
                    Это действие необратимо.
                </div>
            </Modal>
        </div>
    );
}