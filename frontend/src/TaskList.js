import React, { useState } from "react";

export default function TaskList({ tasks, onTaskDeleted, onTaskUpdated }) {
    const [editingTaskId, setEditingTaskId] = useState(null);
    const [editedTitle, setEditedTitle] = useState("");
    const [editedDescription, setEditedDescription] = useState("");
    const [editedStatus, setEditedStatus] = useState("");

    const handleEdit = (task) => {
        setEditingTaskId(task.id);
        setEditedTitle(task.title);
        setEditedDescription(task.description);
        setEditedStatus(task.status || "To Do"); // ✅ По умолчанию "To Do"
    };

    const handleSaveEdit = () => {
        onTaskUpdated(editingTaskId, editedTitle, editedDescription, editedStatus);
        setEditingTaskId(null);
        setEditedTitle("");
        setEditedDescription("");
        setEditedStatus("");
    };

    const handleCancelEdit = () => {
        setEditingTaskId(null);
        setEditedTitle("");
        setEditedDescription("");
        setEditedStatus("");
    };

    return (
        <div>
            <h2>Task List</h2>
            <ul>
                {tasks.map((task) => (
                    <li key={task.id} className={`status-${task.status.toLowerCase().replace(" ", "-")}`}>
                        {editingTaskId === task.id ? (
                            <div>
                                <input
                                    type="text"
                                    value={editedTitle}
                                    onChange={(e) => setEditedTitle(e.target.value)}
                                    placeholder="Edit title"
                                />
                                <textarea
                                    value={editedDescription}
                                    onChange={(e) => setEditedDescription(e.target.value)}
                                    placeholder="Edit description"
                                ></textarea>

                                {/* ✅ Добавляем выпадающий список для выбора статуса */}
                                <select
                                    value={editedStatus}
                                    onChange={(e) => setEditedStatus(e.target.value)}
                                >
                                    <option value="To Do">To Do</option>
                                    <option value="In Progress">In Progress</option>
                                    <option value="Done">Done</option>
                                </select>

                                <button className="save-button" onClick={handleSaveEdit}>Сохранить</button>
                                <button className="cancel-button" onClick={handleCancelEdit}>Отменить</button>
                            </div>
                        ) : (
                            <div>
                                <strong>{task.title}</strong>
                                <p>{task.description}</p>
                                {task.user_id && <p>User ID: {task.user_id}</p>}
                                <p>Creation Date: {new Date(task.created_at).toLocaleString()}</p>

                                {/* ✅ Отображаем статус задачи */}
                                <p>
                                    Status:{" "}
                                    <span className={`task-status status-${task.status.toLowerCase().replace(" ", "-")}`}>
                                        {task.status}
                                    </span>
                                </p>

                                <button className="edit-button" onClick={() => handleEdit(task)}>Редактировать</button>
                                <button className="delete-button" onClick={() => onTaskDeleted(task.id)}>Удалить</button>
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
}
