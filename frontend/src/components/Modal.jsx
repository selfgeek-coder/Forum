import React, { useEffect } from "react";

export default function Modal({ open, title, children, onClose, footer }) {
  useEffect(() => {
    if (!open) return;

    const onKeyDown = (e) => {
      if (e.key === "Escape") onClose?.();
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="md-modal__backdrop" onMouseDown={onClose}>
      <div className="md-modal" onMouseDown={(e) => e.stopPropagation()}>
        <div className="md-modal__header">
          <div className="md-modal__title">{title}</div>
          <button className="md-icon-btn" onClick={onClose} aria-label="Закрыть">
            <span className="material-symbols-outlined" aria-hidden="true">
              close
            </span>
          </button>
        </div>
        <div className="md-modal__body">{children}</div>
        {footer ? <div className="md-modal__footer">{footer}</div> : null}
      </div>
    </div>
  );
}

