import { createContext, useContext, useState, useEffect } from "react";
import { decodeJwt } from "../utils/jwt";

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState({
    isAuthenticated: false,
    userId: null,
    login: null,
  });

  useEffect(() => {
    const token = localStorage.getItem("token");
    const payload = decodeJwt(token);
    const login = localStorage.getItem("login") ?? payload?.name ?? null;
    setAuth({
      token,
      isAuthenticated: Boolean(token && payload?.user_id),
      userId: payload?.user_id ?? null,
      login,
    });
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("login");
    setAuth({ isAuthenticated: false, userId: null, login: null });
  };

  return (
    <AuthContext.Provider value={{ auth, setAuth, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
