import React, { useMemo, useState } from "react";
import api from "../api/axios";
import Modal from "./Modal";
import { formatApiError } from "../utils/apiError";
import { capitalizeFirstLetter } from "../utils/text";

export default function CreatePostModal({ open, onClose, onCreated }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const canSubmit = useMemo(() => title.trim().length > 0 && content.trim().length > 0, [title, content]);

  const handleCreate = async () => {
    if (!canSubmit) {
      setError("Введите заголовок и текст поста.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const normalizedTitle = capitalizeFirstLetter(title.trim());
      await api.post("/post/create", { title: normalizedTitle, content });
      setTitle("");
      setContent("");
      onCreated?.();
      onClose?.();
    } catch (err) {
      setError(formatApiError(err, "Ошибка при создании поста."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      open={open}
      title="Создать пост"
      onClose={onClose}
      footer={
        <div className="md-modal__actions">
          <button className="btn btn--secondary" onClick={onClose} disabled={loading}>
            Отмена
          </button>
          <button className="btn btn--primary" onClick={handleCreate} disabled={loading || !canSubmit}>
            {loading ? "Создание..." : "Создать"}
          </button>
        </div>
      }
    >
      {error ? <div className="alert alert--error">{error}</div> : null}

      <div className="md-field">
        <label className="md-label">Заголовок</label>
        <input
          className="md-input"
          value={title}
          onChange={(e) => setTitle(capitalizeFirstLetter(e.target.value))}
          placeholder="Например: Обновление проекта"
        />
      </div>

      <div className="md-field">
        <label className="md-label">Текст</label>
        <textarea
          className="md-textarea"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Напишите, что нового…"
          rows={6}
        />
      </div>
    </Modal>
  );
}

