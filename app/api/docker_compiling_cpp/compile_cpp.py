import os
import subprocess

def compile_cpp(code: str) -> str:
    current_dir = os.getcwd()
    cpp_dir = os.path.join(current_dir, "app/api/docker_compiling_cpp")

    command = [
        "docker", "run", "--rm",
        "-v", f"{cpp_dir}:/usr/src/app",
        "-w", "/usr/src/app",
        "gcc:latest",
        "bash", "-c", "g++ main.cpp -o app && ./app"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Compilation success: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e.stderr}")
        return e.stderr

def save_cpp() -> str: # Возвращает скомпилированный код в виде строки
    # Определяем текущую директорию
    current_dir = os.getcwd()
    cpp_dir = os.path.join(current_dir, "app/api/docker_compiling_cpp")
    main_cpp_path = os.path.join(cpp_dir, 'main.cpp')
    app_path = os.path.join(cpp_dir, 'app')
    
    try:
        # Чтение кода из файла
        with open(main_cpp_path, 'r') as user_code:
            code = user_code.read()

        # Получаем результат компиляции и выполнения
        result = compile_cpp(code)
        print(f"Compiled code: {result}")
        return result
    finally:
        # Удаляем main.cpp
        os.remove(main_cpp_path)
        if os.path.exists(app_path):
            os.remove(app_path)
        