from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.schemas.user import UserTokenDataSchema
from passlib.context import CryptContext
from app.config import settings
from pydantic import EmailStr
from app.database import get_session
from app.models.user import User
from app.models.token_blacklist import TokenBlackList
from fastapi import HTTPException,status

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_auth = OAuth2PasswordBearer(tokenUrl="/login")

def get_token(token:str = Depends(user_auth),session = Depends(get_session)):
    tk = session.query(TokenBlackList).filter(TokenBlackList.token == token).first()
    if tk:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    return decode_token(token)

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_pass(password:str,hash_password:str):
    return pwd_context.verify(password,hash_password)

def create_token(data:UserTokenDataSchema,session):
    to_encode = data.model_copy()
    token = jwt.encode(to_encode.model_dump(),settings.JWT_SECRET_KEY,algorithm=ALGORITHM)
    is_blacked = session.query(TokenBlackList).filter(TokenBlackList.token == token).first()
    if is_blacked:
        session.delete(is_blacked)
    return token

def decode_token(token:str):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=ALGORITHM)
    return UserTokenDataSchema(**payload)

#что с почтой делать если юзер удален с такойже почтой
def user_by_auth(email:str|EmailStr,password:str,session):
    user = session.query(User).filter(User.email == email,User.is_active == True).first()
    if not user:
        raise ValueError("Неверный логин или пароль")
    if not verify_pass(password,user.password_hash):
        raise ValueError("Неверный логин или пароль")
    return UserTokenDataSchema(id = user.id,role = user.role)


def is_token_blacklisted(token:str,session):
    blacked_token = session.query(TokenBlackList).filter(TokenBlackList.token == token).first()
    if blacked_token:
        raise ValueError("Unautorize")
    return token


def black_token(token,session):
    blacked_token = TokenBlackList(token = token)
    session.add(blacked_token)