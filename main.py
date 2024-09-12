import typing

import fastapi
import uvicorn

from router import router

HOST = "0.0.0.0"
PORT = 8081

app = fastapi.FastAPI()
app.include_router(router)


@app.get("/")
async def root(request: fastapi.Request) -> dict[str, typing.Any]:
    return dict(request.query_params.items())


@app.get("/redirect")
async def redirect(request: fastapi.Request) -> fastapi.responses.RedirectResponse:
    url = request.url_for("root")
    redirect_url = f"{url}"
    query_params = request.query_params
    if query_params:
        redirect_url += f"?{query_params}"
    return fastapi.responses.RedirectResponse(redirect_url)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, workers=1)
