from fastapi import APIRouter

router = APIRouter()

@router.patch("/change_me")
def change_me():
    pass

@router.get("/me")
def get_me():
    pass