import { useEffect, useState } from "react";
import api from "../api/axios";
import Header from "../components/Header";
import "../styles/home.css";

export default function Home() {
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [page, setPage] = useState(1);
    const [hasNext, setHasNext] = useState(false);

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

    return (
        <div className="home-page">
            <Header />

            {loading && <p>Загрузка новостей...</p>}
            {error && <p className="error">{error}</p>}

            <div className="news-list">
                {news.map((post) => (
                    <div key={post.id} className="news-card">
                        <h3>{post.title}</h3>
                        <p>{post.content}</p>
                        <div className="news-footer">
                            <span>Автор: {post.author}</span>
                            <span>❤️ {post.likes_count} 💬 {post.comments_count}</span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="pagination">
                <button
                    onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
                    disabled={page === 1}
                >
                    Назад
                </button>
                <span>Страница {page}</span>
                <button
                    onClick={() => hasNext && setPage((prev) => prev + 1)}
                    disabled={!hasNext}
                >
                    Далее
                </button>
            </div>
        </div>
    );
}