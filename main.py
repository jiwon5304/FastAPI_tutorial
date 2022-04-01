from enum import Enum
from optparse import Option
from typing import  Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, Query

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

# 요청: 모델만들기
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

# 요청: 모델사용
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# 요청: 경로 매개변수
# url: http://127.0.0.1:8000/items/1
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# 요청: 경로 매개변수 + 쿼리 매개변수
# url: http://127.0.0.1:8000/items/1?q=as
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# 유효성검사
app = FastAPI()

@app.get("/items/")
# async def read_items(q: Optional[str] = None):  #기본값: None
# async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")): # 유효성검사: 추가 검증 -> Q값은 선택값 & 3 < 길이 < 50 & 정규표현식
async def read_items(q: str = Query("fixedquery", min_length=3)): # 기본값: fixedquery & 3 < 길이 
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# url: http://127.0.0.1:8000/items/?q=foo&q=bar
# List 방법1
@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items

# List 방법2
@app.get("/items/")
async def read_items(q: list = Query([])):
    query_items = {"q": q}
    return query_items

# title, description 추가
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Alias parameters
# url: http://127.0.0.1:8000/items/?item-query=ddddd
@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# deprecated=True -> 더 이상 사용하지 않겠다는 뜻
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# include_in_schema=False -> OpenAPI 스키마(자동 문서)에서 쿼리 매개변수를 제외
@app.get("/items/")
async def read_items(
    hidden_query: Optional[str] = Query(None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}