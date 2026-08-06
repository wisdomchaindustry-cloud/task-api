from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from database import engine, create_db_and_tables, seed_tasks
from models import Task

app = FastAPI()


@app.on_event("startup")
def startup():
    create_db_and_tables()
    seed_tasks()


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "title is required"}
    )


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


@app.get("/", summary="API info", description="Returns basic info about this API")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health check", description="Returns server status")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List tasks", description="Returns all tasks")
def get_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/tasks/{task_id}", summary="Get one task", description="Returns a single task by id, or 404 if not found")
def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"}
            )

        return task


@app.post("/tasks", status_code=201, summary="Create task", description="Creates a new task with a title")
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title is required"}
        )

    with Session(engine) as session:
        new_task = Task(title=task.title, done=False)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task


@app.put("/tasks/{task_id}", summary="Update task", description="Updates a task by id")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title is required"}
        )

    with Session(engine) as session:
        existing_task = session.get(Task, task_id)

        if existing_task is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"}
            )

        existing_task.title = task.title
        existing_task.done = task.done
        session.add(existing_task)
        session.commit()
        session.refresh(existing_task)
        return existing_task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete task", description="Deletes a task by id")
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"}
            )

        session.delete(task)
        session.commit()
        return