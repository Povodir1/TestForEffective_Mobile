from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.crud.item import db_create_item,db_get_item,db_get_all_items
router = APIRouter(prefix="/items",tags=["Items"])

@router.get("/all")
def get_all_items(limit:int = 10,page:int = 1,session:Session = Depends(get_session)):
    response = db_get_all_items(limit,page, session)
    return response

@router.get("/{item_id}")
def get_item(item_id:int,session:Session = Depends(get_session)):
    response = db_get_item(item_id,session)
    return response

