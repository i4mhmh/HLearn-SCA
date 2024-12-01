from typing import Union
from fastapi import FastAPI
from apps.api import user, datasets
import apps
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(user.userRouter)
app.include_router(datasets.datasetRouter)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "hello world"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}