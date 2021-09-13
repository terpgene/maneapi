from fastapi import FastAPI
from enum import Enum
from typing import Optional

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

@app.get("/items")
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
