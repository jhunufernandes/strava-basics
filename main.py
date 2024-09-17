import typing

import fastapi
import fastapi.middleware
import uvicorn

HOST = "0.0.0.0"
PORT = 8081

app = fastapi.FastAPI()


@app.get("/")
async def root(request: fastapi.Request) -> dict[str, typing.Any]:
    return dict(request.query_params.items())


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, workers=1)
