from fastapi import FastAPI
from syncLast import syncLast
from syncAllRatings import syncAll
from syncLibrary import getDiff
import uvicorn
from threading import Thread

app = FastAPI()
# uvicorn main:app --reload


@app.get("/")
async def root():
    return syncLast()


@app.get("/ratings")
async def library():
    t = Thread(target=syncAll)
    t.start()
    return "started"


@app.get("/library")
async def library():
    t = Thread(target=getDiff)
    t.start()
    return "started"


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
  uvicorn.run("main:app", reload=True)
