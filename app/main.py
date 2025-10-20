from fastapi import FastAPI

from app.api.auth import router as auth_router

from app.api.admin.users import router as admin_user_router
from app.api.admin.items import router as admin_item_router

from app.api.user.items import router as user_items
from app.api.user.basket import router as user_basket
from app.api.user.orders import router as user_orders
from app.api.user.profile import router as user_profile

app = FastAPI()

app.include_router(auth_router)

app.include_router(admin_item_router)
app.include_router(admin_user_router)

app.include_router(user_items)
app.include_router(user_basket)
app.include_router(user_orders)
app.include_router(user_profile)