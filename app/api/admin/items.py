from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def post_item():
    pass

@router.delete("/{item_id}")
def del_item():
    pass

