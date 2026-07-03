from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int

items_db = {}

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in items_db:
        raise HTTPException(400, "Item already exists")
    items_db[item_id] = item
    return {"message": "Item created", "item": item}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")
    return items_db[item_id]