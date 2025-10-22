from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.security import check_permissions, ActionEnum as Act, ResourceEnum as Res, get_token,ResourceEnum,ActionEnum,RoleEnum
from app.schemas.user import UserTokenDataSchema
from app.crud.permission import db_get_all_permissions,db_add_permission,db_delete_permission,db_update_user_role

router = APIRouter(prefix="/roles",tags=["Permissions"])


@router.patch("/{user_id}")
def update_user_role(user_id:int,
                     role:RoleEnum,
                     user:UserTokenDataSchema = Depends(get_token),
                     perm = Depends(check_permissions(Res.PERMISSIONS,Act.READ)),
                     session:Session = Depends(get_session)):
    response = db_update_user_role(user_id,role,session)
    return response




@router.get("/permissions")
def get_all_permissions(user:UserTokenDataSchema = Depends(get_token),
                        perm = Depends(check_permissions(Res.PERMISSIONS,Act.READ)),
                        session:Session = Depends(get_session)):
    response = db_get_all_permissions(session)
    return response

@router.post("/permissions")
def add_permissions(role:RoleEnum,
                    resource:ResourceEnum,
                    action:ActionEnum,
                    user:UserTokenDataSchema = Depends(get_token),
                    perm = Depends(check_permissions(Res.PERMISSIONS,Act.CREATE)),
                    session:Session = Depends(get_session)):
    response = db_add_permission(role=role,resource=resource,action=action, session=session)
    return response

@router.delete("/permissions")
def delete_permissions( role:RoleEnum,
                        resource:ResourceEnum,
                        action:ActionEnum,
                        user:UserTokenDataSchema = Depends(get_token),
                        perm = Depends(check_permissions(Res.PERMISSIONS,Act.DELETE)),
                        session:Session = Depends(get_session)):

    response = db_delete_permission(role=role,resource=resource,action=action, session=session)
    return response