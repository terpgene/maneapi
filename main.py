from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel

# Declare the Enum class extending both String Type and Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

# Path with Enums
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}

# Initial root path
@app.get("/")
async def root():
    return {"message": "Hello World!"}

# Path with item with type
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Using two similar paths. Declare the static first
@app.get("/user/me")
async def read_user_me():
    return {"user_id": "the current user"}

# Using two similar paths. Declare the varying second
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Path Parameters
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# Querying Parameters - for searches
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/item")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# Optional Parameters
@app.get("/opts/{opts_id}")
async def read_opt(opts_id: str, q: Optional[str] = None):
    if q:
        return {"opts_id": opts_id, "q": q}
    return {"opts_id": opts_id}


# Query parameter type conversion - you can declare bool types and they will be converted
@app.get("/optional/{optional_id}")
async def read_optional(optional_id: str, q: Optional[str] = None, short: bool = False):
    optional = {"optonal_id": optional_id}
    if q:
        optional.update({"q": q})
    if not short:
        optional.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return optional

# Multiple path and query parameters
@app.get("/usr/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update( 
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Required query parameters
@app.get("/mute/{mute_id}")
async def read_user_itemized(mute_id: str, needy: str):
    item = {"mute_id": mute_id, "needy": needy}
    return item



# Implementing Request Body
class Item(BaseModel):
    name: str
    description: Optional[str] = None 
    price: float
    tax: Optional[float] = None 

@app.post("/transact/")
async def create_transact(transact: Item):
    transact_dict = transact.dict()
    if transact.tax:
        price_with_tax = transact.price + transact.tax
        transact_dict.update({"price_with_tax": price_with_tax})
    return transact_dict

