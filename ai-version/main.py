from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="To-Do List API")


# -------------------------
# Models
# -------------------------

class TaskCreate(BaseModel):
    title: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool


# -------------------------
# In-memory data
# -------------------------

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build To-Do API", "done": False},
    {"id": 3, "title": "Test Endpoints", "done": True},
]

next_id = 4


# -------------------------
# Helper
# -------------------------

def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


# -------------------------
# Routes
# -------------------------

@app.get("/")
def root():
    return {"message": "To-Do List API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_id

    if task.title is None or task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={"error": "title is required"}
        )

    new_task = {
        "id": next_id,
        "title": task.title.strip(),
        "done": False
    }

    tasks.append(new_task)
    next_id += 1

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskUpdate):
    task = find_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    if updated.title is None or updated.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={"error": "title is required"}
        )

    task["title"] = updated.title.strip()
    task["done"] = updated.done

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    tasks.remove(task)

    return Response(status_code=status.HTTP_204_NO_CONTENT)