# 1) Собираем React-приложение
FROM node:18 as build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . ./
RUN npm run build

# 2) Поднимаем Nginx, чтобы отдавать билд
FROM nginx:1.23-alpine

# Копируем сборку в стандартную директорию Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Пробрасываем порт 80
EXPOSE 80

# Важно: не уводим nginx в фон, чтобы контейнер не завершался
CMD ["nginx", "-g", "daemon off;"]
