from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select

from db.database import get_session
from models.status import Status, StatusCreate, StatusRead
from crud.status import get_status_by_id
from crud.status import (
    create_status,
    delete_status,
    get_status,
    get_status_by_id,
    get_status_by_title,
    get_statuss_from_todo_list,
    update_status,
)
from auth.dependencies import get_current_user, require_role  # Import role-based dependency

router = APIRouter()

@router.post("/", response_model=StatusRead)
def create(status: StatusCreate, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    try:
        todo = get_status_by_id(session, status.todolist_id)
        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo-List with ID '{status.todolist_id}' not found")
        
        # Create the status with the Todo-List ID
        status_data = Task(**status.model_dump(), created_at=datetime.now())
        created_status = create_status(session, status_data)
        session.refresh(created_status)  # Refresh to load relationships
        return created_status
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[StatusRead])
def read_all(session: Session = Depends(get_session)):
    try:
        return get_statuss(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{status_id}", response_model=StatusRead)
def read(status_id: int, session: Session = Depends(get_session)):
    try:
        status = get_status_by_id(session, status_id)
        if not status:
            raise HTTPException(status_code=404, detail=f"Task with ID {status_id} not found")
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/title/{title}", response_model=StatusRead)
def read_by_title(title: str, session: Session = Depends(get_session)):
    try:
        todolist = get_status_by_title(session, title)
        if not todolist:
            raise HTTPException(status_code=404, detail=f"Todo-list with title '{title}' not found")
        return todolist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/todo/{todo_list_id}", response_model=list[StatusRead])
def read_by_todo_id(todo_list_id: int, session: Session = Depends(get_session)):
    try:
        statuss = get_statuss_from_todo_list(session, todo_list_id)
        if not statuss:
            raise HTTPException(status_code=404, detail=f"No Todo-Lists found for ID '{todo_list_id}'")
        return statuss
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{status_id}", response_model=Task)
def update(
    status_id: int,
    status_data: dict = Body(
        ...,
        examples=[
            {
                "title": "Updated Task Title",
                "content": "Updated content for the Task"
            }
        ]
    ),
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    try:
        updated_status = update_status(session, status_id, status_data)
        if not updated_status:
            raise HTTPException(status_code=404, detail=f"Task with ID {status_id} not found")
        return updated_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{status_id}", response_model=Task)
def delete(status_id: int, session: Session = Depends(get_session), current_user: dict = Depends(require_role("admin"))):
    try:
        deleted_status = delete_status(session, status_id)
        if not deleted_status:
            raise HTTPException(status_code=404, detail=f"Task with ID {status_id} not found")
        return deleted_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")