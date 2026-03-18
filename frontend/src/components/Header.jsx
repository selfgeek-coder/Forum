import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/header.css";

export default function Header() {
    const login = localStorage.getItem("login");
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("login");
        navigate("/login");
    };

    return (
        <header className="app-header">
            <div className="container app-header__inner">
                <div className="header-left">
                    <h1 className="header-logo" onClick={() => navigate("/")}>
                        Форум
                    </h1>
                </div>
                <div className="header-right">
                    {login ? (
                        <>
                            <span className="header-user">{login}</span>
                            <button
                                className="header-create"
                                onClick={() => navigate("/?create=1")}
                            >
                                Создать пост
                            </button>
                            <button className="header-logout" onClick={handleLogout}>
                                Выйти
                            </button>
                        </>
                    ) : (
                        <button className="header-login" onClick={() => navigate("/login")}>
                            Войти
                        </button>
                    )}
                </div>
            </div>
        </header>
    );
}