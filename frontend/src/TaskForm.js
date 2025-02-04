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
                // Update existing task
                const response = await fetch(`http://localhost:5000/tasks/${editingTask.id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ title, description }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Task successfully updated!");
                    onTaskUpdated(data);
                } else {
                    alert(`Error: ${data.error}`);
                }
            } else {
                // Create new task
                const response = await fetch("http://localhost:5000/tasks/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ title, description, username }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Task successfully created!");
                    onTaskCreated(data); // Send task data back
                } else {
                    alert(`Error: ${data.error}`);
                }
            }
        } catch (error) {
            console.error("Error submitting task form:", error);
            alert("Failed to send request.");
        }
    };

    return (
        <form onSubmit={onSubmit}>
            <h2>{editingTask ? "Edit Task" : "Create Task"}</h2>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Task Title"
                required
            />
            <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Task Description"
            ></textarea>
            {!editingTask && (
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username (optional)"
                />
            )}
            <button type="submit">{editingTask ? "Update Task" : "Create Task"}</button>
        </form>
    );
}
