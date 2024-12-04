import subprocess
import os

def run_in_docker(file_path):
    try:
        # Запуск Docker контейнера с C++ компилятором
        docker_command = f"sudo docker run --rm -v {os.path.abspath(file_path)}:/user_code.cpp gcc:latest bash -c 'g++ ./user_code.cpp -o ./user_code && ./user_code'"
        
        # Выполняем команду внутри Docker контейнера
        result = subprocess.run(docker_command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return f"Error during execution: {result.stderr}"
        
        return result.stdout  # Возвращаем вывод программы

    except Exception as e:
        return f"Error: {str(e)}"




