from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.crud.user import db_get_all_users

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/all")
def get_all_users(session:Session = Depends(get_session)):
    response = db_get_all_users(session)
    return response