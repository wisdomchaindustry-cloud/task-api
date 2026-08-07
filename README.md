 Task API

A simple CRUD API for managing a to-do list, built with FastAPI as part of the FlyRank backend track.

## How to run (local, without Docker)

1. Clone this repo and enter the folder:

git clone https://github.com/wisdomchaindustry-cloud/task-api.git
cd task-api

2. Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Mac/Linux)

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

## AI vs me

**Prompt used (first attempt):**

Build a to-do list API using FastAPI. It should have these endpoints:
- GET / → returns 200
- GET /health → returns 200
- GET /tasks → returns the whole list, status 200
- GET /tasks/{id} → returns a single task by id, status 200. If the id doesn't exist, return 404 with a JSON error like {"detail": "Task 99 not found"}
- POST /tasks → accepts JSON with a title (string). The server assigns the id, sets done to false, returns status 201. If the title is missing or empty, return 400 with {"error": "title is required"}
- PUT /tasks/{id} → accepts id, title, and done (true/false). Same validation and 404 rules as above. Returns status 200 if successful.
- DELETE /tasks/{id} → returns status 204 if successful. If the id doesn't exist, return 404 with {"detail": "Task 2 not found"}

Three example tasks should exist in memory when the server starts. No database.

**Result:** Every checkpoint passed on the first try — all status codes (200, 201, 204, 400, 404) and error JSON shapes matched exactly.

**What the AI did better:** It handled the missing/empty-title validation without needing a custom global exception handler. By making `title` optional in the Pydantic model and checking it manually, it got a precise `400` response directly — I had to build a separate exception handler in my own code to override FastAPI's default `422` for the same case.

**What it got wrong or ignored:** Nothing broke my checkpoints, but the AI invented its own JSON shape for `GET /` (`{"message": "To-Do List API"}`) since I never specified one — a silent decision filling a real gap in my prompt.

**What my prompt forgot to specify:** The exact JSON content of `GET /` and `GET /health` beyond their status codes, and any specific seed task titles.

**The rematch:** I added one sentence specifying the exact JSON for `GET /`. The regenerated version matched my own root endpoint's output exactly — proof that a more precise prompt produces a more precise result.

## Database upgrade: Postgres in Docker (A3)

### Why Postgres was chosen

This assignment moves storage from a single SQLite file (A2) to PostgreSQL running in a Docker container. Postgres is a real database server — the same kind of engine used by most production backends — rather than a single file on disk. Running it in Docker means no manual installation and no "works on my machine" problems: anyone cloning this repo gets an identical database, started with one command.

### Where the data lives now

Task rows live inside a Postgres container, and the actual data files are stored in a Docker-managed named volume (`taskdata`). This means the data survives even if the containers themselves are deleted and recreated — verified by running `docker compose down` followed by `docker compose up` and confirming tasks created beforehand were still present.

### How to run this project (with Docker)

1. Clone this repo and enter the folder:

git clone https://github.com/wisdomchaindustry-cloud/task-api.git
cd task-api

2. Copy the example environment file:

cp .env.example .env

3. Start the whole stack (app + database) with one command:

docker compose up

4. Visit http://localhost:8000/docs for interactive Swagger documentation.

No local Python installation, virtual environment, or manual Postgres setup is required — Docker handles all of it.

### Example SQL query

Connected directly to the database container to run raw SQL:

docker exec -it task-api-db-1 psql -U postgres -d tasks

```sql
SELECT * FROM tasks;
```

id | title | done
----+-----------------------+------
5 | Learn SQL basics | f
6 | Ship the Docker stack | t
7 | Write the README | f
(3 rows)


Changes made directly through `psql` (inserting, updating, deleting rows) were immediately reflected by the API with zero code changes — proof that the API layer and the storage layer are fully independent of each other.

### Database screenshot

![Database](db-screenshot.png)
