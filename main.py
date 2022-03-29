from enum import Enum
from typing import  Optional
from fastapi import FastAPI

class ModelName(str, Enum):
    a = "alexnet"
    r = "resnet"
    l = "lenet"

app = FastAPI()


# 경로 매개변수: 일반 함수 정의
@app.get("/")
def root():
    return {"message": "Hello World2"}

# 경로 매개변수: 비동기함수 정의
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.a:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "resnet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# 쿼리 매개변수: 기본값
# url: http://127.0.0.1:8000/items/?skip=0&limit=10
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# 쿼리 매개변수: 선택적 매개변수
# url: http://127.0.0.1:8000/items/1?q=a
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# 쿼리 매개변수: 유형변환
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# 쿼리 매개변수: 다중 경로 및 쿼리 매개변수
# url: http://127.0.0.1:8000/users/1/items/2?q=w&short=false
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# 쿼리 매개변수: 필수 쿼리 매개변수
# url: http://127.0.0.1:8000/items/1?needy=sss
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# 쿼리 매개변수: 필수값, 기본값, 선택값
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
