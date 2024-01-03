from fastapi import FastAPI
from syncLast import syncLast
import uvicorn

app = FastAPI()
# uvicorn main:app --reload


@app.get("/")
async def root():
    return syncLast()


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)
