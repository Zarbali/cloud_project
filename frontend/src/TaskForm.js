import React, { useState, useEffect } from "react";

export default function TaskForm({ onTaskCreated, onTaskUpdated, editingTask }) {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [username, setUsername] = useState("");

    useEffect(() => {
        if (editingTask) {
            setTitle(editingTask.title);
            setDescription(editingTask.description);
            setUsername(editingTask.username || "");
        } else {
            setTitle("");
            setDescription("");
            setUsername("");
        }
    }, [editingTask]);

    const onSubmit = async (e) => {
        e.preventDefault();

        try {
            if (editingTask) {
                // Редактирование задачи
                const response = await fetch(`http://localhost:5000/tasks/${editingTask.id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ title, description }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Задача успешно обновлена!");
                    onTaskUpdated(data);
                } else {
                    alert(`Ошибка: ${data.error}`);
                }
            } else {
                // Создание задачи
                const response = await fetch("http://localhost:5000/tasks/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ title, description, username }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Задача успешно создана!");
                    onTaskCreated(data); // Передача данных задачи обратно
                } else {
                    alert(`Ошибка: ${data.error}`);
                }
            }
        } catch (error) {
            console.error("Ошибка при отправке формы задачи:", error);
            alert("Не удалось выполнить запрос.");
        }
    };

    return (
        <form onSubmit={onSubmit}>
            <h2>{editingTask ? "Редактировать задачу" : "Создать задачу"}</h2>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Название задачи"
                required
            />
            <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Описание задачи"
            ></textarea>
            {!editingTask && (
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Имя пользователя (опционально)"
                />
            )}
            <button type="submit">{editingTask ? "Обновить задачу" : "Создать задачу"}</button>
        </form>
    );
}
