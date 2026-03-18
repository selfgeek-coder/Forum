import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import "../styles/auth.css";

const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const handleLogin = async () => {
        setError("");

        if (!isValidEmail(email)) {
            setError("Введите корректный email адрес.");
            return;
        }

        try {
            const res = await api.post("/login", { email, password });
            const data = res.data.data;

            localStorage.setItem("token", data.access_token);
            localStorage.setItem("login", data.login);

            navigate("/");
        } catch (err) {
            const detail = err.response?.data?.detail;
            if (detail?.message) {
                setError(detail.message);
            } else {
                setError("Ошибка входа. Попробуйте снова.");
            }
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <div className="auth-title">Вход</div>

                <input
                    className={`auth-input ${error && !isValidEmail(email) ? "auth-input--error" : ""}`}
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />

                <input
                    type="password"
                    className="auth-input"
                    placeholder="Пароль"
                    onChange={(e) => setPassword(e.target.value)}
                />

                {error && <div className="auth-error">{error}</div>}

                <button className="auth-button" onClick={handleLogin}>
                    Войти
                </button>

                <div className="auth-footer">
                    Нет аккаунта?{" "}
                    <span className="auth-link" onClick={() => navigate("/register")}>
                        Регистрация
                    </span>
                </div>
            </div>
        </div>
    );
}