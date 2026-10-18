from fastapi import APIRouter, Depends, HTTPException, status
from .ERPNext_Bridge import ERPNextClient

router = APIRouter(prefix="/inventory", tags=["Inventory Router"])

@router.get("/items/{item_code}")
async def searchItem(item_code: str, bridge: ERPNextClient = Depends()):
    item = await bridge.searchItem(item_code)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item code '{item_code}' does not exist."
        )
    return {"status": "success", "item": item}