from fastapi import APIRouter

router = APIRouter()

@router.get("/all")
def get_all_items():
    pass

@router.get("/{item_id}")
def get_item():
    pass

