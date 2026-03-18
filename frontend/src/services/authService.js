import api from "../api/axios";

export const AuthService = {
  login: ({ email, password }) => api.post("/login", { email, password }),
  register: (form) => api.post("/register", form),
};