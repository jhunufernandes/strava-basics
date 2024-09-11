import typing

import fastapi
import fastapi.security
import starlette
import starlette.config
import starlette.middleware.cors
import starlette.middleware.sessions
import uvicorn
from authlib.integrations.starlette_client import OAuth

HOST = "0.0.0.0"
PORT = 8080
SCOPE = 'activity:read_all'

SESSION_SECRET = 'REPLACE WITH A PROPER SECRET OF YOUR CHOICE'


oauth2_authorization_code_bearer = fastapi.security.OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://strava.com/oauth2/authorize",
    tokenUrl="https://strava.com/oauth2/token",
)


async def get_token(
    request: fastapi.Request,
    oauth2_scheme: typing.Annotated[
        fastapi.security.OAuth2AuthorizationCodeBearer,
        fastapi.Depends(oauth2_authorization_code_bearer),
    ],
):
    return await oauth2_scheme(request)


app = fastapi.FastAPI()
app.add_middleware(
    starlette.middleware.sessions.SessionMiddleware,
    secret_key=SESSION_SECRET,
    https_only=True,
)
app.add_middleware(
    starlette.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(token: typing.Annotated[typing.Any, fastapi.Security(get_token)]):
    return {"token": token}


config = starlette.config.Config('.env')
oauth = OAuth(config)
oauth.register(
    'strava',
    authorize_url='https://strava.com/oauth2/authorize',
    access_token_url='https://strava.com/oauth2/token',
    scope=SCOPE,
)


@app.get("/login")
async def login(request: fastapi.Request):
    redirect_uri = request.url_for("auth")
    return await oauth.strava.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: fastapi.Request):
    token = await oauth.strava.authorize_access_token(request)
    return token


if __name__ == "__main__":
    uvicorn.run("oauth2:app", host=HOST, port=PORT, workers=1)
