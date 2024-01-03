from fastapi import FastAPI
from syncLast import syncLast

app = FastAPI()
# uvicorn main:app --reload


@app.get("/")
async def root():
    return syncLast


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

