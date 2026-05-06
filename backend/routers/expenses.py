from fastapi import APIRouter

router = APIRouter()


@router.get("/expenses")
async def get_expenses():
    return []


@router.get("/expenses/{expense_id}")
async def get_expense(expense_id: str):
    return {"message": "Phase 3에서 구현"}


@router.put("/expenses/{expense_id}")
async def update_expense(expense_id: str):
    return {"message": "Phase 3에서 구현"}


@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str):
    return {"message": "Phase 3에서 구현"}
