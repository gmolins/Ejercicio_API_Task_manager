from datetime import datetime
import random
from sqlmodel import SQLModel, Session
from db.database import engine, create_db_and_tables, drop_db_and_tables
from models.status import Status
from models.user import User
from models.todo import TodoList
from models.task import Task
from auth.hashing import hash_password  # Importamos la función para hashear contraseñas

def seed_data(num_dummies=5):
    # Borrar la base de datos y las tablas existentes
    drop_db_and_tables() 
    # Crear la base de datos y las tablas
    create_db_and_tables()

    with Session(engine) as session:
        # Crear usuarios
        try:
            users = []
            for i in range(num_dummies):
                users.append(User(id=i, username=f"User {i}", email=f"user{i}@example.com", role=random.choice(["user", "admin", "viewer"]), hashed_password=hash_password(f"password{i}")))
            session.add_all(users)
            session.commit()
        except Exception as e:
            print(f"Error creating users: {e}")

        # Crear todos linkados a usuarios
        try:
            todos = []
            for i in range(num_dummies):
                todos.append(TodoList(id=i, title=f"Todo entry {i}", description=f"Todo list for entry {i}", owner_id=users[i].id, created_at=datetime.now()))
            session.add_all(todos)
            session.commit()
        except Exception as e:
            print(f"Error creating todos: {e}")

        # Crear tasks
        try:
            tasks = []
            for i in range(num_dummies):
                tasks.append(Task(id=i, title=f"Task {i}", description=f"Content for task {i}", is_completed=False, created_at=datetime.now(), todo_list_id=todos[i].id))
            session.add_all(tasks)
            session.commit()
        except Exception as e:
            print(f"Error creating tasks: {e}")
        
        # Crear status
        try:
            status1 = Status(id=0, title=f"WIP", color=f"Blue", todo_list_id=todos[0].id)
            status2 = Status(id=0, title=f"Completed", color=f"Green", todo_list_id=todos[0].id)
            status3 = Status(id=0, title=f"Blocker", color=f"Red", todo_list_id=todos[0].id)
            session.add_all([status1, status2, status3])
            session.commit()
        except Exception as e:
            print(f"Error creating status: {e}")
            
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
