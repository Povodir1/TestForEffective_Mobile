from fastapi import APIRouter,Depends
from app.crud.order import db_get_all_orders,db_create_order
from app.security import check_permissions,ActionEnum as Act,ResourceEnum as Res,get_token
from app.database import get_session
from app.schemas.user import UserTokenDataSchema
router = APIRouter(prefix="/orders",tags=["Orders"])

@router.get("/all")
def get_all_orders(user:UserTokenDataSchema = Depends(get_token),
                   perm=Depends(check_permissions(Res.ORDERS, Act.READ)),
                   session = Depends(get_session)):

    response = db_get_all_orders(user.id,session)
    return response

@router.post("/create")
def add_to_basket(user:UserTokenDataSchema = Depends(get_token),
                  perm=Depends(check_permissions(Res.ORDERS, Act.CREATE)),
                  session = Depends(get_session)):

    response = db_create_order(user.id,session)
    return response
