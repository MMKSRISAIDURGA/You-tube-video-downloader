from typing import Union

from fastapi import FastAPI

app = FastAPI()
@app.get("/add")
def addNum(a,b):
    return 10+20