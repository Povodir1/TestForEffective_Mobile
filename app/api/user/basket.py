from fastapi import APIRouter, Depends
from app.crud.basket import db_get_basket_items,db_add_to_basket,db_delete_from_basket
from app.security import check_permissions,ActionEnum as Act,ResourceEnum as Res,get_token
from app.database import get_session
from app.schemas.user import UserTokenDataSchema

router = APIRouter(prefix="/basket",tags=["Basket"])

@router.get("/all")
def get_basket(user:UserTokenDataSchema = Depends(get_token),
               perm=Depends(check_permissions(Res.BASKET_ITEMS, Act.READ)),
               session = Depends(get_session)):

    response = db_get_basket_items(user.id,session)
    return response


@router.post("/add")
def add_to_basket(item_id:int,
                  count:int  = 1,
                  user:UserTokenDataSchema = Depends(get_token),
                  perm=Depends(check_permissions(Res.BASKET_ITEMS, Act.CREATE)),
                  session = Depends(get_session)):

    response = db_add_to_basket(user.id,item_id, count, session)
    return response


@router.delete("/del")
def del_from_basket(item_id:int,
                    user:UserTokenDataSchema = Depends(get_token),
                    perm=Depends(check_permissions(Res.BASKET_ITEMS, Act.DELETE)),
                    session = Depends(get_session)):

    response = db_delete_from_basket(item_id,user.id,session)
    return response
