# Базовый образ с компилятором C++
FROM gcc:latest

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app/api/docker_compiling_cpp

# Копируем код в контейнер
COPY . .

# Команда для компиляции и выполнения кода
CMD ["bash", "-c", "g++ -o program main.cpp && ./program"]
