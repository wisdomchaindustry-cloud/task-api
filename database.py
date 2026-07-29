from sqlmodel import SQLModel, create_engine, Session, select
from models import Task

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def seed_tasks():
    with Session(engine) as session:
        existing = session.exec(select(Task)).first()
        if existing is None:
            session.add(Task(title="Buy milk", done=False))
            session.add(Task(title="Walk the dog", done=False))
            session.add(Task(title="Read a book", done=False))
            session.commit()