import React, { useState } from "react";

export default function LoginForm({ onLogin }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:5000/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            if (response.ok) {
                localStorage.setItem("token", data.token);
                onLogin(data.user_id, data.username);
            } else {
                alert(`Ошибка: ${data.error}`);
            }
        } catch (error) {
            console.error("Ошибка входа:", error);
            alert("Ошибка при входе в систему.");
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <h2>Вход</h2>
            <input
                type="text"
                placeholder="Имя пользователя"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button type="submit">Войти</button>
        </form>
    );
}
