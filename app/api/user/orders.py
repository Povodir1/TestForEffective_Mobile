from fastapi import APIRouter

router = APIRouter(prefix="/order")

@router.get("/all")
def get_all_orders():
    pass

@router.post("/create")
def add_to_basket():
    pass
