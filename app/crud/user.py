from sqlalchemy.orm import Session

from app.schemas.user import UserRegisterSchema,UserSchema,UserUpdateSchema
from app.models.user import User
from app.models.basket_item import BasketItem
from app.models.role import Role
from app.security import hash_pass,RoleEnum
from app.exceptions import InvalidDataError,ObjectAlreadyExistError,ObjectNotFoundError

def db_create_user(new_user:UserRegisterSchema,session):
    if new_user.password != new_user.again_password:
        raise InvalidDataError("Разные пароли")
    if new_user.email in [user.email for user in session.query(User).all()]:
        raise ObjectAlreadyExistError("Пользователь с таким email уже существует")
    user_role = session.query(Role).filter(Role.name == RoleEnum.User.value).first()
    user = User(name = new_user.name,surname = new_user.surname,
                middle_name = new_user.middle_name,email = new_user.email,
                role_id = user_role.id,password_hash = hash_pass(new_user.password))
    session.add(user)
    session.flush()
    return UserSchema(id = user.id,name = user.name,surname = user.surname,
                      middle_name = user.middle_name,email = user.email,
                      role = user.roles.name,money=user.money)


def db_get_user(user_id:int,session):
    user = session.query(User).filter(User.id == user_id,User.is_active == True).first()
    if not user:
        raise ObjectNotFoundError("Нет пользователя с таким id")
    return UserSchema(id=user.id, name=user.name, surname=user.surname,
                      middle_name=user.middle_name, email=user.email,
                      role=user.roles.name, money=user.money)

def db_get_all_users(session):
    users = session.query(User).all()
    return [UserSchema(id=user.id, name=user.name, surname=user.surname,
                      middle_name=user.middle_name, email=user.email,
                      role=user.roles.name, money=user.money) for user in users]

def db_update_user(user_id:int,new_data:UserUpdateSchema,session):
    user = session.query(User).filter(User.id == user_id,User.is_active == True).first()
    if not user:
        raise ObjectNotFoundError("Нет пользователя с таким id")
    for key, value in new_data.model_dump(exclude_none=True).items():
        setattr(user, key, value)
    session.flush()
    return UserSchema(id=user.id, name=user.name, surname=user.surname,
                      middle_name=user.middle_name, email=user.email,
                      role=user.roles.name, money=user.money)


def db_delete_user(user_id:int,session):
    user = session.query(User).filter(User.id == user_id,User.is_active == True).first()
    if not user:
        raise ObjectNotFoundError("Нет пользователя с таким id")
    user.is_active = False
    session.query(BasketItem).filter(BasketItem.user_id == user_id).delete()