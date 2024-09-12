import typing

import authlib.integrations.starlette_client
import fastapi
import fastapi.middleware
import starlette.middleware.sessions
import uvicorn
import starlette.middleware

import authlib
from router import router

HOST = "0.0.0.0"
PORT = 8081

app = fastapi.FastAPI()
app.include_router(router)
app.add_middleware(starlette.middleware.sessions.SessionMiddleware, secret_key="some-random-string")

oauth = authlib.integrations.starlette_client.OAuth()
oauth.register(
    'strava',
    client_id='...',
    client_secret='...',
)


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


@app.route('/login')
async def login(request: fastapi.Request) -> typing.Any:
    redirect_uri = request.url_for('auth')
    return await oauth.strava.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: fastapi.Request) -> typing.Any:
    token = await oauth.strava.authorize_access_token(request)
    return token


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, workers=1)
