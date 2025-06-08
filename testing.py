from modules_for_app.db_utils.db_init import SessionLocal
from modules_for_app.models.user import User
import os
from dotenv import load_dotenv

load_dotenv()

# Создаём сессию к базе
db = SessionLocal()

# Создаём пользователя
user = User(
    email="test@example.com",
    username="testuser",
    phone="+79998887766"
)
user.set_password("super-secret-password")  # шифруем с солью

# Добавляем и сохраняем
db.add(user)
db.commit()
db.refresh(user)

print("Пользователь создан:", user)
