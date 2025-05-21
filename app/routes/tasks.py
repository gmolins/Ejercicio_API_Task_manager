from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select

from db.database import get_session
from models.task import Task, TaskRead, TaskCreate
from models.todo import TodoList
from crud.todo import get_todolist_by_id
from crud.tasks import (
    create_task,
    get_tasks,
    get_task_by_id,
    get_task_by_title,
    get_tasks_from_todo_list
)
from auth.dependencies import get_current_user, require_role  # Import role-based dependency

router = APIRouter()

@router.post("/", response_model=TaskRead)
def create(task: TaskCreate, session: Session = Depends(get_session)):
    try:
        todo = get_todolist_by_id(session, task.todolist_id)
        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo-List with ID '{task.todolist_id}' not found")
        
        # Create the task with the Todo-List ID
        task_data = Task(**task.model_dump())
        created_task = create_task(session, task_data)
        session.refresh(created_task)  # Refresh to load relationships
        return created_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[TaskRead])
def read_all(session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    try:
        return get_tasks(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{todolist_id}", response_model=TaskRead)
def read(task_id: int, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    try:
        task = get_task_by_id(session, task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/title/{title}", response_model=TaskRead)
def read_by_title(title: str, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    try:
        todolist = get_task_by_title(session, title)
        if not todolist:
            raise HTTPException(status_code=404, detail=f"Todo-list with title '{title}' not found")
        return todolist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/user/{user_name}", response_model=list[TaskRead])
def read_by_user_name(todo_list_title: str, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    try:
        todos = get_tasks_from_todo_list(session, todo_list_title)
        if not todos:
            raise HTTPException(status_code=404, detail=f"No Todo-Lists found for user '{todo_list_title}'")
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{todo_id}", response_model=TodoList)
def update(
    todo_id: int,
    todo_data: dict = Body(
        ...,
        example={
            "title": "Updated Todo-List Title",
            "content": "Updated content for the Todo-List"
        }
    ),
    session: Session = Depends(get_session),
):
    try:
        updated_todo = update_todolist(session, todo_id, todo_data)
        if not updated_todo:
            raise HTTPException(status_code=404, detail=f"Todo-List with ID {todo_id} not found")
        return updated_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/title/{title}", response_model=TodoList)
def update_by_title(
    title: str,
    todo_data: dict = Body(
        ...,
        example={
            "title": "Updated Todo-List Title",
            "content": "Updated content for the Todo-List"
        }
    ),
    session: Session = Depends(get_session),
):
    try:
        updated_todo = update_todolist_by_title(session, title, todo_data)
        if not updated_todo:
            raise HTTPException(status_code=404, detail=f"Todo-List with title '{title}' not found")
        return updated_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{todolist_id}", response_model=TodoList)
def delete(todolist_id: int, session: Session = Depends(get_session), current_user: dict = Depends(require_role("admin"))):
    try:
        deleted_todolist = delete_todolist(session, todolist_id)
        if not deleted_todolist:
            raise HTTPException(status_code=404, detail=f"Todo-List with ID {todolist_id} not found")
        return deleted_todolist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/title/{title}", response_model=TodoList)
def delete_by_title(title: str, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    try:
        deleted_todolist = delete_todolist_by_title(session, title)
        if not deleted_todolist:
            raise HTTPException(status_code=404, detail=f"Todo-List with title '{title}' not found")
        return deleted_todolist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")