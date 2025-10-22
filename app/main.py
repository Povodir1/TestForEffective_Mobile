from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse

from app.api.auth import router as auth_router

from app.api.admin.users import router as admin_user_router
from app.api.manager.items import router as admin_item_router
from app.api.admin.permission import router as admin_permission_router

from app.api.guest.items import router as user_items
from app.api.user.basket import router as user_basket
from app.api.user.orders import router as user_orders
from app.api.user.profile import router as user_profile

from app.exceptions import (InvalidDataError,NoMoneyError,
                            ObjectNotFoundError,ObjectAlreadyExistError)

from app.new_dataset import main_seeder

app = FastAPI()

app.include_router(auth_router)

app.include_router(admin_item_router)
app.include_router(admin_user_router)
app.include_router(admin_permission_router)

app.include_router(user_items)
app.include_router(user_basket)
app.include_router(user_orders)
app.include_router(user_profile)


@app.exception_handler(InvalidDataError)
async def bad_request_exception_handler(request: Request, exc: InvalidDataError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail})

@app.exception_handler(ObjectNotFoundError)
async def not_found_exception_handler(request: Request, exc: ObjectNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail})

@app.exception_handler(ObjectAlreadyExistError)
async def conflict_exception_handler(request: Request, exc: ObjectAlreadyExistError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail})

@app.exception_handler(NoMoneyError)
async def forbidden_exception_handler(request: Request, exc: NoMoneyError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail})

#заполянем тестовыми данными
main_seeder()