import os
import subprocess

def compile_cpp(code: str) -> str:
    # Определяем текущую директорию
    current_dir = os.getcwd()
    cpp_dir = os.path.join(current_dir, "app/api/docker_compiling_cpp")
    
    # Команда для запуска контейнера
    command = [
        "docker", "run", "--rm",
        "-v", f"{cpp_dir}:/usr/src/app",
        "-w", "/usr/src/app",
        "gcc:latest",
        "bash", "-c", "g++ main.cpp -o app && ./app"
    ]

    try:
        # Запускаем команду и получаем вывод
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("An error occurred with docker:")
        return e.stderr

def save_cpp():
    # Определяем текущую директорию
    current_dir = os.getcwd()
    cpp_dir = os.path.join(current_dir, "app/api/docker_compiling_cpp")
    
    # Чтение кода из файла
    with open(os.path.join(cpp_dir, 'main.cpp'), 'r') as user_code:
        code = user_code.read()

    # Получаем результат компиляции и выполнения
    result = compile_cpp(code)

    # Сохраняем результат в файл
    with open(os.path.join(cpp_dir, 'result'), 'w') as output_file:
        output_file.write(result)
        print(result)
