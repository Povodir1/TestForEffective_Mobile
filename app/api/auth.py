from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserRegisterSchema,UserLoginSchema,UserTokenDataSchema
from app.security import create_token,user_by_auth,black_token,user_auth
from app.database import get_session
from sqlalchemy.orm.session import Session
from app.crud.user import db_create_user

router = APIRouter(tags=["Auth"])


@router.post("/register")
def register(new_user:UserRegisterSchema,session:Session = Depends(get_session)):
    try:
        user = db_create_user(new_user, session)
        user_data = UserTokenDataSchema(id= user.id,role = user.role)
        new_token = create_token(user_data,session)
        return {"access_token": new_token,
                "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),session:Session = Depends(get_session)):
    try:
        user_data = user_by_auth(form_data.username, form_data.password, session)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )
        new_token = create_token(user_data,session)
        return {"access_token": new_token,
                "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

@router.post("/logout")
def logout(b_token:str = Depends(user_auth),session:Session = Depends(get_session)):
    black_token(b_token,session)
    return {"message": "Токен отозван (внесен в черный список)"}
