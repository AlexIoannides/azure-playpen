"""Example web API."""
from datetime import datetime

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def heartbeat():
    "Return a heartbeat."
    now = datetime.now()
    response = {
        "timestamp": now.isoformat(timespec="milliseconds"), "message": "I am healthy."
    }
    return response


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0")
