import React, { useState, useEffect } from "react";
import TaskList from "./TaskList";
import TaskForm from "./TaskForm";
import UserForm from "./UserForm";

export default function TaskManager() {
    const [tasks, setTasks] = useState([]);
    const [users, setUsers] = useState([]);
    const [searchQuery, setSearchQuery] = useState(""); // 🔍 Стейт для поиска

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                alert("Ошибка: пользователь не авторизован.");
                return;
            }

            const response = await fetch("http://localhost:5000/tasks/", {
                headers: { "Authorization": token }
            });

            if (!response.ok) {
                throw new Error("Ошибка при загрузке задач");
            }

            const data = await response.json();
            setTasks(data);
        } catch (error) {
            console.error("Ошибка при загрузке задач:", error);
        }
    };

    const onTaskCreated = (task) => {
        setTasks([...tasks, task]);
    };

    const onUserCreated = (user) => {
        setUsers([...users, user]);
        alert(`Пользователь ${user.username} успешно создан!`);
    };

    const onTaskDeleted = async (taskId) => {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`http://localhost:5000/tasks/${taskId}`, {
                method: "DELETE",
                headers: { "Authorization": token }
            });

            if (response.ok) {
                setTasks(tasks.filter((task) => task.id !== taskId));
                alert("Задача успешно удалена!");
            } else {
                const data = await response.json();
                alert(`Ошибка при удалении задачи: ${data.error}`);
            }
        } catch (error) {
            console.error("Ошибка при удалении задачи:", error);
        }
    };

    const onTaskUpdated = async (taskId, title, description) => {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`http://localhost:5000/tasks/${taskId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": token
                },
                body: JSON.stringify({ title, description })
            });

            if (response.ok) {
                const updatedTask = await response.json();
                setTasks(tasks.map((task) => (task.id === taskId ? updatedTask : task)));
                alert("Задача успешно обновлена!");
            } else {
                const data = await response.json();
                alert(`Ошибка при обновлении задачи: ${data.error}`);
            }
        } catch (error) {
            console.error("Ошибка при обновлении задачи:", error);
        }
    };

    // 🔍 Фильтрация задач по названию и описанию
    const filteredTasks = tasks.filter(task =>
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div>
            <h1>Менеджер задач</h1>
            <UserForm onUserCreated={onUserCreated} />
            <TaskForm onTaskCreated={onTaskCreated} />

            {/* 🔍 Поле поиска */}
            <input
                type="text"
                placeholder="🔍 Поиск по задачам"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />

            <TaskList tasks={filteredTasks} onTaskDeleted={onTaskDeleted} onTaskUpdated={onTaskUpdated} />
        </div>
    );
}
