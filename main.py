from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import delete_and_create_db
from tasks.routers import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print("Loading app..")
    await delete_and_create_db()
    yield
    # Clean up the ML models and release the resources
    print("Closing app ...")


app = FastAPI(
    lifespan=lifespan,
    title="Task Manager API",
    description="An API to manage tasks with CRUD operations",
    version="1.0.0",
    debug=True,
)

app.include_router(tasks_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
