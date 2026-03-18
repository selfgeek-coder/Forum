import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import "../styles/auth.css";

const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

export default function Register() {
    const [form, setForm] = useState({
        email: "",
        login: "",
        name: "",
        password: ""
    });
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const handleRegister = async () => {
        setError("");

        if (!isValidEmail(form.email)) {
            setError("Введите корректный email адрес.");
            return;
        }

        try {
            await api.post("/register", form);
            alert("Регистрация успешна");
            navigate("/login");
        } catch (err) {
            const detail = err.response?.data?.detail;

            if (Array.isArray(detail)) {
                const messages = detail.map(d => d.msg.replace(/^Value error, /, "")).join(" ");
                setError(messages);
            } else if (detail?.message) {
                setError(detail.message.replace(/^Value error, /, ""));
            } else {
                setError("Ошибка регистрации. Попробуйте снова.");
            }
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-box">
                <div className="auth-title">Регистрация</div>

                <input
                    className={`auth-input ${error && !isValidEmail(form.email) ? "auth-input--error" : ""}`}
                    placeholder="Email"
                    value={form.email}
                    onChange={(e) => setForm({...form, email: e.target.value})}
                />

                <input 
                    className="auth-input" 
                    placeholder="Логин"
                    value={form.login}
                    onChange={(e) => setForm({...form, login: e.target.value})} 
                />

                <input 
                    className="auth-input" 
                    placeholder="Имя"
                    value={form.name}
                    onChange={(e) => setForm({...form, name: e.target.value})} 
                />

                <input 
                    type="password" 
                    className="auth-input" 
                    placeholder="Пароль"
                    value={form.password}
                    onChange={(e) => setForm({...form, password: e.target.value})} 
                />

                {error && <div className="auth-error">{error}</div>}

                <button className="auth-button" onClick={handleRegister}>
                    Зарегистрироваться
                </button>

                <div className="auth-footer">
                    Уже есть аккаунт?{" "}
                    <span className="auth-link" onClick={() => navigate("/login")}>
                        Войти
                    </span>
                </div>
            </div>
        </div>
    );
}