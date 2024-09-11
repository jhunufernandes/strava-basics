import datetime

import fastapi
import uvicorn

from router import router

HOST = "0.0.0.0"
PORT = 8081

app = fastapi.FastAPI()
app.include_router(router)


@app.get("/")
async def root() -> list[datetime.datetime]:
    dummy_times = [
        datetime.datetime(2018, 1, 1, 10, 0, 0),
        datetime.datetime(2018, 1, 2, 10, 30, 0),
        datetime.datetime(2018, 1, 3, 11, 0, 0),
    ]

    return dummy_times


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, workers=1)
