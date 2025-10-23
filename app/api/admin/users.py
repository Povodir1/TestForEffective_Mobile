from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.crud.user import db_get_all_users
from app.security import check_permissions,ActionEnum as Act,ResourceEnum as Res,get_token
from app.schemas.user import UserTokenDataSchema

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/all")
def get_all_users(session:Session = Depends(get_session),
                  user:UserTokenDataSchema = Depends(get_token),
                  perm = Depends(check_permissions(Res.USERS,Act.READ_ALL))):

    response = db_get_all_users(session)
    return response



