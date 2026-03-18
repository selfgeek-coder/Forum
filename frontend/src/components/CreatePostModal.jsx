import React, { useMemo } from "react";
import Modal from "./Modal";
import { useForm } from "../hooks/useForm";
import { PostService } from "../services/postService";
import { capitalizeFirstLetter } from "../utils/text";

export default function CreatePostModal({ open, onClose, onCreated }) {
  const onSubmit = async (values) => {
    try {
      await PostService.create({
        title: capitalizeFirstLetter(values.title.trim()),
        content: values.content.trim(),
      });
      setValues({ title: "", content: "" });
      onCreated?.();
      onClose?.();
    } catch (err) {
      setErrors({ submit: "Ошибка при создании поста" });
    }
  };

  const { values, errors, handleChange, handleSubmit, setValues, setErrors } = useForm(
    { title: "", content: "" },
    onSubmit,
    (vals) => {
      const errs = {};
      if (!vals.title.trim()) errs.title = "Введите заголовок";
      if (!vals.content.trim()) errs.content = "Введите текст";
      return errs;
    }
  );

  const canSubmit = useMemo(() => values.title.trim() && values.content.trim(), [values]);

  return (
    <Modal
      open={open}
      title="Создать пост"
      onClose={onClose}
      footer={
        <div className="md-modal__actions">
          <button className="btn btn--secondary" onClick={onClose} disabled={false}>Отмена</button>
          <button className="btn btn--primary" onClick={handleSubmit} disabled={!canSubmit}>
            Создать
          </button>
        </div>
      }
    >
      {errors.submit && <div className="alert alert--error">{errors.submit}</div>}

      <div className="md-field">
        <label className="md-label">Заголовок</label>
        <input
          className="md-input"
          name="title"
          value={values.title}
          onChange={handleChange}
          placeholder="Например: Обновление проекта"
        />
        {errors.title && <small className="md-error">{errors.title}</small>}
      </div>

      <div className="md-field">
        <label className="md-label">Текст</label>
        <textarea
          className="md-textarea"
          name="content"
          value={values.content}
          onChange={handleChange}
          placeholder="Напишите, что нового…"
          rows={6}
        />
        {errors.content && <small className="md-error">{errors.content}</small>}
      </div>
    </Modal>
  );
}