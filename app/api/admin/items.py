from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas.item import ItemCreateSchema
from app.crud.item import db_create_item,db_delete_item

router = APIRouter(prefix="/items",tags=["Items"])

@router.post("/create")
def post_item(new_item:ItemCreateSchema,session:Session = Depends(get_session)):
    response = db_create_item(new_item,session)
    return response

@router.delete("/{item_id}")
def del_item(item_id:int,session:Session = Depends(get_session)):
    response = db_delete_item(item_id, session)
    return response

