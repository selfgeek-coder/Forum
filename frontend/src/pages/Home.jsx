import { useEffect, useMemo, useState } from "react";
import api from "../api/axios";
import Header from "../components/Header";
import PostCard from "../components/PostCard";
import CreatePostModal from "../components/CreatePostModal";
import { useSearchParams } from "react-router-dom";
import { getAuthInfo } from "../utils/jwt";
import "../styles/home.css";

export default function Home() {
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [page, setPage] = useState(1);
    const [hasNext, setHasNext] = useState(false);
    const [searchParams, setSearchParams] = useSearchParams();

    const auth = useMemo(() => getAuthInfo(), [searchParams]);
    const createOpen = searchParams.get("create") === "1";

    const fetchNews = async (pageNumber = 1) => {
        setLoading(true);
        setError("");

        try {
            const res = await api.get(`/post/news/${pageNumber}`);
            const data = res.data.data;

            setNews(data.posts);
            setHasNext(data.pagination.has_next);
        } catch (err) {
            setError("Ошибка при загрузке новостей");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNews(page);
    }, [page]);

    const handleCloseCreate = () => {
        const next = new URLSearchParams(searchParams);
        next.delete("create");
        setSearchParams(next, { replace: true });
    };

    const handleCreated = () => {
        setPage(1);
        fetchNews(1);
    };

    const handleDeleted = (postId) => {
        setNews((prev) => prev.filter((p) => p.id !== postId));
    };

    return (
        <div className="app-shell">
            <Header />

            <main className="container">
                <section className="news-surface">
                    <div className="page-header">
                        <div>
                            <h2 className="page-title">Новости</h2>
                            <div className="page-subtitle">Лента свежих постов сообщества</div>
                        </div>
                    </div>

                    {loading && <div className="muted">Загрузка новостей...</div>}
                    {error && <div className="alert alert--error">{error}</div>}

                    <div className="news-list">
                        {news.map((post) => (
                            <PostCard
                                key={post.id}
                                post={post}
                                auth={auth}
                                onDeleted={handleDeleted}
                            />
                        ))}
                    </div>

                    <div className="pagination">
                        <button
                            className="btn btn--secondary"
                            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
                            disabled={page === 1}
                        >
                            Назад
                        </button>
                        <span className="muted">Страница {page}</span>
                        <button
                            className="btn btn--secondary"
                            onClick={() => hasNext && setPage((prev) => prev + 1)}
                            disabled={!hasNext}
                        >
                            Далее
                        </button>
                    </div>
                </section>
            </main>

            <CreatePostModal
                open={createOpen && auth.isAuthenticated}
                onClose={handleCloseCreate}
                onCreated={handleCreated}
            />
        </div>
    );
}