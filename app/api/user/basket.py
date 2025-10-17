from fastapi import APIRouter

router = APIRouter()

@router.get("/all")
def get_basket():
    pass

@router.post("/add")
def add_to_basket():
    pass

@router.delete("/del")
def del_from_basket():
    pass
