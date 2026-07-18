# Task API

A simple CRUD API for managing a to-do list, built with FastAPI as part of the FlyRank Week 2 backend assignment. Tasks are stored in memory (no database) - data resets whenever the server restarts.

## How to run

1. Clone this repo and enter the folder:

   git clone https://github.com/wisdomchaindustry-cloud/task-api.git
   cd task-api

2. Create and activate a virtual environment:

   python -m venv venv
   venv\Scripts\activate      (Windows)
   source venv/bin/activate   (Mac/Linux)

3. Install dependencies:

   pip install -r requirements.txt

4. Run the server:

   uvicorn main:app --reload

5. Visit http://localhost:8000/docs for interactive Swagger documentation.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | / | API info |
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| GET | /tasks/{task_id} | Get a single task |
| POST | /tasks | Create a new task |
| PUT | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

## Example request

curl -i http://localhost:8000/tasks/1

HTTP/1.1 200 OK
content-type: application/json

{"id":1,"title":"Buy milk","done":false}

## Swagger UI

Full CRUD cycle tested via /docs "Try it out": Create, Read, Update, Delete all confirmed working with correct status codes (201, 200, 200, 204).

![Swagger UI](swagger-screenshot.png)

## The mortality experiment

I created a 4th task ("This task should disappear"), confirmed it existed via GET /tasks, then stopped the server (Ctrl+C) and restarted it (uvicorn main:app --reload). After restarting, GET /tasks showed only the original 3 seed tasks - the 4th task was gone. This happens because the task list lives only in the server's RAM as a Python variable; nothing was ever written to disk, so restarting the process wipes it clean and re-runs the hardcoded starting list from the top of the file.
