from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()

# Request body + path parameters
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None




@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return{"item_id": item_id, **item.dict()}