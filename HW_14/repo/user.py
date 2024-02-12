import os
import hashlib
from models.users import UsertDB


class UserRepo():
    """
    Модуль для роботи з репозиторієм користувачів.

    Атрибути:
    - db: Екземпляр сесії бази даних.
    """
    def __init__(self, db) -> None:
        self.db = db


    def create(self, user):
        """
        Створити нового користувача.

        Повертає:
        Нового користувача.

        """
        password, salt = self.hash_password(user.password)
        new_user = UsertDB(**user.dict())
        new_user.password = password
        new_user.salt = salt
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def get_by_username(self, username):
        """
        Отримати користувача по імю.

        Повертає:
        Користувача.

        """
        return self.db.query(UsertDB).filter(UsertDB.username == username).first()
    
    def get_by_email(self, email):
        """
        Отримати користувача по email

        Повертає:
        Користувача.

        """
        return self.db.query(UsertDB).filter(UsertDB.email == email).first()
        

    def get_user_check_pass(self, username, password):
        """
        Перевірка пароля користувача

        Повертає:
        Користувача, якщо пароль вірний.

        """
        user = self.db.query(UsertDB).filter(UsertDB.username == username).first()
        password_from_db = user.password
        user_salt = user.salt
        hashed_pass, _ = self.hash_password(password=password, salt=user_salt)
        if hashed_pass==password_from_db:
            return user
        else:
            return None
    

    def generate_salt(self):
        """
        Генерація солі

        Повертає:
        Сіль.

        """
        return os.urandom(16)  # 16 байтів солі (128 біт)

    def hash_password(self, password, salt=None):
        """
        Функція для хешування паролю з використанням солі

        Повертає:
        Захешований пароль та сіль.

        """
        if salt is None:
            salt = self.generate_salt()
        else:
            salt = bytes.fromhex(salt)  
        salted_password = password.encode() + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return str(hashed_password), str(salt.hex())
    
    def verify_password(self, plain_password, hashed_password, salt):
        """
        Верифікація паролю

        Повертає:
        True, якщо пароль вірний.

        """
        return hashed_password == self.hash_password(plain_password, salt)[0]
     