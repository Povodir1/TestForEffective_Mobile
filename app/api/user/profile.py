from fastapi import APIRouter,Depends
from app.crud.user import db_get_user,db_update_user,db_delete_user
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas.user import UserTokenDataSchema,UserUpdateSchema
from app.security import get_token,user_auth,black_token
router = APIRouter(prefix="/users",tags=["Users"])

@router.patch("/change_me")
def change_me(new_data:UserUpdateSchema,user:UserTokenDataSchema = Depends(get_token),session:Session = Depends(get_session)):
    response = db_update_user(user.id,new_data, session)
    return response

@router.get("/me")
def get_me(user:UserTokenDataSchema = Depends(get_token),session:Session = Depends(get_session)):
    response = db_get_user(user.id,session)
    return response

@router.delete("/me")
def delete_me(user:UserTokenDataSchema = Depends(get_token),b_token:str = Depends(user_auth),session:Session = Depends(get_session)):
    db_delete_user(user.id,session)
    black_token(b_token,session)
    return {"message":"User soft-deleted"}