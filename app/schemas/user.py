from pydantic import BaseModel,EmailStr
from typing import Optional

class UserLoginSchema(BaseModel):
    email:EmailStr
    password:str


class UserRegisterSchema(UserLoginSchema):
    again_password:str
    name:str
    surname:str
    middle_name:str


class UserUpdateSchema(BaseModel):
    name:Optional[str] = None
    surname:Optional[str] = None
    middle_name:Optional[str] = None

class UserTokenDataSchema(BaseModel):
    id:int
    role:str


class UserSchema(BaseModel):
    id:int
    name: str
    surname: str
    middle_name: str
    email:EmailStr
    role:str
    money:float

