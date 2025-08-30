from .models import Task
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import TaskShemaPost, TaskShemaGet
from sqlalchemy import select
from typing import Optional


async def list_tasks_view(db: AsyncSession) -> list[TaskShemaGet]:
    query = select(Task)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return [TaskShemaGet.model_validate(task) for task in tasks]


async def get_task_by_id_view(task_id: int, db: AsyncSession) -> TaskShemaGet:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        return None
    await db.commit()
    return TaskShemaGet.model_validate(task)


async def create_task_view(db: AsyncSession, task: TaskShemaPost) -> TaskShemaGet:
    new_task = Task(**task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return TaskShemaGet.model_validate(new_task)


async def update_task_view(db: AsyncSession, task_id: int, task_data: TaskShemaPost) -> Optional[TaskShemaGet]:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        return None

    # Update all fields
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed

    await db.commit()
    await db.refresh(task)

    return TaskShemaGet.model_validate(task)


async def partial_update_task_view(
    db: AsyncSession,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    completed: bool | None = None
) -> TaskShemaGet | None:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        return None

    # Update only provided fields
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    await db.commit()
    await db.refresh(task)

    return TaskShemaGet.model_validate(task)


async def delete_task_view(db: AsyncSession, task_id: int) -> bool:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        return False
    await db.delete(task)
    await db.commit()
    return True
