from uuid import uuid4
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None


tasks: list[TaskSchema] = []
categories: list[CategorySchema] = []


@app.get("/tasks")
async def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()),
                          title=payload.title,
                          completed=False)
    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}")
async def update_task(task_id: str,
                      payload: TaskUpdateSchema) -> TaskSchema:
    for task in tasks:
        if task.id == task_id:
            task.title = payload.title if payload.title else task.title
            task.completed = payload.completed \
                if payload.completed is not None else task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return None
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/categories")
async def read_categories() -> list[CategorySchema]:
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreateSchema) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()),
                                  name=payload.name)
    categories.append(new_category)
    return new_category


@app.patch("/categories/{category_id}")
async def update_category(category_id: str, payload: CategoryUpdateSchema) \
        -> CategorySchema:
    for category in categories:
        if category.id == category_id:
            category.name = payload.name if payload.name is not None \
                else category.name
            return category
    raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/categories/{category_id}",
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return None
    raise HTTPException(status_code=404, detail="Category not found")
