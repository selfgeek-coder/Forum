import { useNavigate } from "react-router-dom";
import { useForm } from "../hooks/useForm";
import { AuthService } from "../services/authService";
import "../styles/auth.css";

const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

export default function Login() {
  const navigate = useNavigate();

  const onSubmit = async (values) => {
    try {
      const res = await AuthService.login(values);
      const data = res.data.data;
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("login", data.login);
      navigate("/");
    } catch (err) {
      const detail = err.response?.data?.detail;
      setErrors({
        submit: detail?.message ?? "Ошибка входа. Попробуйте снова.",
      });
    }
  };

  const { values, errors, handleChange, handleSubmit, setErrors } = useForm(
    { email: "", password: "" },
    onSubmit,
    (vals) => {
      const errs = {};
      if (!isValidEmail(vals.email)) errs.email = "Введите корректный email";
      if (!vals.password) errs.password = "Введите пароль";
      return errs;
    }
  );

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="auth-title">Вход</div>
        <input
          name="email"
          className={`auth-input ${errors.email ? "auth-input--error" : ""}`}
          placeholder="Email"
          value={values.email}
          onChange={handleChange}
        />
        <input
          name="password"
          type="password"
          className={`auth-input ${errors.password ? "auth-input--error" : ""}`}
          placeholder="Пароль"
          value={values.password}
          onChange={handleChange}
        />
        {errors.submit && <div className="auth-error">{errors.submit}</div>}
        <button className="auth-button" onClick={handleSubmit}>
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