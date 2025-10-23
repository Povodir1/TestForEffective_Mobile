from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas.item import ItemCreateSchema,ItemPatchSchema
from app.crud.item import db_create_item,db_delete_item,db_patch_item
from app.security import check_permissions,ActionEnum as Act,ResourceEnum as Res

router = APIRouter(prefix="/items",tags=["Items"])

@router.post("/create",status_code=status.HTTP_201_CREATED)
def post_item(new_item:ItemCreateSchema,
              perm=Depends(check_permissions(Res.ITEMS, Act.CREATE)),
              session:Session = Depends(get_session)):

    response = db_create_item(new_item,session)
    return response

@router.patch("/update")
def patch_item(item_id:int,
               new_data:ItemPatchSchema,
               perm=Depends(check_permissions(Res.ITEMS, Act.UPDATE)),
               session:Session = Depends(get_session)):

    response = db_patch_item(item_id,new_data,session)
    return response

@router.delete("/{item_id}")
def del_item(item_id:int,
             perm=Depends(check_permissions(Res.ITEMS, Act.DELETE)),
             session:Session = Depends(get_session)):

    db_delete_item(item_id, session)
    return {"message":"Item deleted"}
