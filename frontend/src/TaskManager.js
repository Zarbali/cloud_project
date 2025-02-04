import React, { useState, useEffect } from "react";
import TaskList from "./TaskList";
import TaskForm from "./TaskForm";
import UserForm from "./UserForm";

export default function TaskManager() {
    const [tasks, setTasks] = useState([]);
    const [users, setUsers] = useState([]);
    const [searchQuery, setSearchQuery] = useState(""); // 🔍 State for search

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                alert("Error: User is not authorized.");
                return;
            }

            const response = await fetch("http://localhost:5000/tasks/", {
                headers: { "Authorization": token }
            });

            if (!response.ok) {
                throw new Error("Error loading tasks");
            }

            const data = await response.json();
            setTasks(data);
        } catch (error) {
            console.error("Error loading tasks:", error);
        }
    };

    const onTaskCreated = (task) => {
        setTasks([...tasks, task]);
    };

    const onUserCreated = (user) => {
        setUsers([...users, user]);
        alert(`User ${user.username} has been successfully created!`);
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
                alert("Task successfully deleted!");
            } else {
                const data = await response.json();
                alert(`Error deleting task: ${data.error}`);
            }
        } catch (error) {
            console.error("Error deleting task:", error);
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
                alert("Task successfully updated!");
            } else {
                const data = await response.json();
                alert(`Error updating task: ${data.error}`);
            }
        } catch (error) {
            console.error("Error updating task:", error);
        }
    };

    // 🔍 Filter tasks by title and description
    const filteredTasks = tasks.filter(task =>
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div>
            <h1>Task Manager</h1>
            <UserForm onUserCreated={onUserCreated} />
            <TaskForm onTaskCreated={onTaskCreated} />

            {/* 🔍 Search input */}
            <input
                type="text"
                placeholder="🔍 Search tasks"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />

            <TaskList tasks={filteredTasks} onTaskDeleted={onTaskDeleted} onTaskUpdated={onTaskUpdated} />
        </div>
    );
}
