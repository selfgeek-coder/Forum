export function formatApiError(err, fallbackMessage = "Произошла ошибка") {
  const detail = err?.response?.data?.detail;

  if (!detail) return fallbackMessage;

  if (typeof detail === "string") return detail;

  // FastAPI/Pydantic validation: [{loc, msg, type}, ...]
  if (Array.isArray(detail)) {
    const messages = detail
      .map((d) => (typeof d?.msg === "string" ? d.msg : null))
      .filter(Boolean)
      .map((m) => m.replace(/^Value error, /, ""));
    if (messages.length) return messages.join(" ");
    return fallbackMessage;
  }

  if (typeof detail === "object" && typeof detail.message === "string") {
    return detail.message.replace(/^Value error, /, "");
  }

  return fallbackMessage;
}

