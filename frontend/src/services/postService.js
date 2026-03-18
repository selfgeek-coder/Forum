import api from "../api/axios";

export const PostService = {
  create: (data) => api.post("/post/create", data),
  fetchNews: (page) => api.get(`/post/news/${page}`),
  fetchById: (id) => api.get(`/post/${id}`),
  delete: (id) => api.delete(`/post/${id}`),
};
