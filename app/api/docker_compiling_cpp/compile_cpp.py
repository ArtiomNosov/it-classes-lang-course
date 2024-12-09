import os
import subprocess

'''
В этом файле две функции: compile_cpp() и save_cpp()
compile через докер компилирует с++ код и возвращает 
либо ошибку, либо выведенный код. save сохраняет в 
файлик, но это временное решение. лучше потом делать
просто реквест обратно на сайт с выведенным результатом.
'''

def compile_cpp(code: str) -> str:
    import subprocess

    # Команда для запуска контейнера
    command = [
        "docker", "run", "--rm", 
        "-v", "/home/i313/Programming/it-class-v2/it-classes-lang-course/app/api/docker_compiling_cpp:/usr/src/app", 
        "-w", "/usr/src/app", 
        "gcc:latest", 
        "bash", "-c", "g++ -o app main.cpp && ./app"
    ]

    try:
        # Запускаем команду и получаем вывод
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("An error occurred wtih docker:")
        return e.stderr

def save_cpp():
    # Чтение кода из файла
    with open('app/api/docker_compiling_cpp/main.cpp', 'r') as user_code:
        code = user_code.read()

    # Получаем результат компиляции и выполнения
    result = compile_cpp(code)

    # Сохраняем результат в файл
    with open('app/api/docker_compiling_cpp/result', 'w') as output_file:
        output_file.write(result)
        print(result)

