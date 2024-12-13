import bcrypt

def hash_password(password: str):
    # Генерация соли
    salt = bcrypt.gensalt()
    # Хэширование пароля с солью
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(hashed, to_check) -> bool:
    if bcrypt.checkpw(to_check.encode('utf-8'), hashed):

        return True
    else:
        return False