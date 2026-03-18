import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api/axios";
import Header from "../components/Header";
import PostCard from "../components/PostCard";
import { getAuthInfo } from "../utils/jwt";
import "../styles/home.css";

export default function PostPage() {
  const { id } = useParams();
  const postId = Number(id);

  const auth = useMemo(() => getAuthInfo(), []);
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchPost = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get(`/post/${postId}`);
      setPost(res.data.data);
    } catch (err) {
      setError("Не удалось загрузить пост");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!Number.isFinite(postId) || postId <= 0) {
      setError("Некорректный ID поста");
      setLoading(false);
      return;
    }
    fetchPost();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId]);

  return (
    <div className="app-shell">
      <Header />
      <main className="container">
        <section className="news-surface">
          <div className="page-header">
            <div>
              <h2 className="page-title">Пост</h2>
              <div className="page-subtitle">
                <Link className="md-link" to="/">
                  ← Назад к новостям
                </Link>
              </div>
            </div>
          </div>

          {loading && <div className="muted">Загрузка...</div>}
          {error && <div className="alert alert--error">{error}</div>}

          {post ? (
            <PostCard
              post={post}
              auth={auth}
              showFull
              onDeleted={() => (window.location.href = "/")}
            />
          ) : null}
        </section>
      </main>
    </div>
  );
}

