export function decodeJwt(token) {
  if (!token || typeof token !== "string") return null;

  const parts = token.split(".");
  if (parts.length < 2) return null;

  try {
    const base64Url = parts[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

export function getAuthInfo() {
  const token = localStorage.getItem("token");
  const payload = decodeJwt(token);
  const userId = payload?.user_id ?? null;
  const login = localStorage.getItem("login") ?? payload?.name ?? null;

  return {
    token,
    isAuthenticated: Boolean(token && userId),
    userId,
    login,
  };
}

