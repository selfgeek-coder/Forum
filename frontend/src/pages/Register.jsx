import { useNavigate } from "react-router-dom";
import { useForm } from "../hooks/useForm";
import { AuthService } from "../services/authService";
import "../styles/auth.css";

const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

export default function Register() {
  const navigate = useNavigate();

  const onSubmit = async (values) => {
    try {
      await AuthService.register(values);
      alert("Регистрация успешна");
      navigate("/login");
    } catch (err) {
      const detail = err.response?.data?.detail;
      let msg = "Ошибка регистрации. Попробуйте снова.";
      if (Array.isArray(detail)) {
        msg = detail.map(d => d.msg.replace(/^Value error, /, "")).join(" ");
      } else if (detail?.message) {
        msg = detail.message.replace(/^Value error, /, "");
      }
      setErrors({ submit: msg });
    }
  };

  const { values, errors, handleChange, handleSubmit, setErrors } = useForm(
    { email: "", login: "", name: "", password: "" },
    onSubmit,
    (vals) => {
      const errs = {};
      if (!isValidEmail(vals.email)) errs.email = "Введите корректный email";
      if (!vals.login) errs.login = "Введите логин";
      if (!vals.name) errs.name = "Введите имя";
      if (!vals.password) errs.password = "Введите пароль";
      return errs;
    }
  );

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="auth-title">Регистрация</div>
        <input name="email" placeholder="Email" value={values.email} onChange={handleChange} />
        <input name="login" placeholder="Логин" value={values.login} onChange={handleChange} />
        <input name="name" placeholder="Имя" value={values.name} onChange={handleChange} />
        <input type="password" name="password" placeholder="Пароль" value={values.password} onChange={handleChange} />
        {errors.submit && <div className="auth-error">{errors.submit}</div>}
        <button className="auth-button" onClick={handleSubmit}>Зарегистрироваться</button>
        <div className="auth-footer">
          Уже есть аккаунт?{" "}
          <span className="auth-link" onClick={() => navigate("/login")}>Войти</span>
        </div>
      </div>
    </div>
  );
}