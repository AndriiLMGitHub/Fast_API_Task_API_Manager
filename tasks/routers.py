from typing import Annotated
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from .schemas import TaskSchemaSingleGet, TaskShemaPost, TaskShemaGetList
from .services import (
    create_task_view,
    list_tasks_view,
    delete_task_view,
    update_task_view,
    partial_update_task_view,
    get_task_by_id_view
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks API"],
)


@router.get("/", summary="List all tasks", response_model=TaskShemaGetList)
async def list_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await list_tasks_view(db)
    return {
        "success": True,
        "data": tasks
    }


@router.get("/{task_id}", summary="Get task by id", response_model=TaskSchemaSingleGet)
async def get_task_by_id(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id_view(task_id, db)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "success": True,
        "data": task
    }


@router.post("/", summary="Create a new task", response_model=TaskSchemaSingleGet)
async def create_task(
    task: Annotated[TaskShemaPost, Depends()],
    db: AsyncSession = Depends(get_db)
):
    response = await create_task_view(db, task)

    return {
        "success": True,
        "data": response
    }


@router.put('/{task_id}', summary="Update task by id", response_model=TaskSchemaSingleGet)
async def update_task(
    task_id: int,
    task_data: Annotated[TaskShemaPost, Depends()],
    db: AsyncSession = Depends(get_db)
):
    updated_task = await update_task_view(db, task_id, task_data)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "success": True,
        "data": updated_task
    }


@router.patch('/{task_id}', summary="Partially update task by id", response_model=TaskSchemaSingleGet)
async def partial_update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    completed: bool | None = False,
    db: AsyncSession = Depends(get_db)
):
    updated_task = await partial_update_task_view(db, task_id, title, description, completed)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "success": True,
        "data": updated_task
    }


@router.delete('/{task_id}', summary="Delete task by id")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_task_view(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "success": True,
        "message": "Task deleted successfully"
    }
