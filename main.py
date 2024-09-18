import os
import typing
import urllib.parse

import fastapi
import httpx

DOMAIN = os.getenv("DOMAIN", "https://localhost:8080")
AUTHORIZE_URL = "http://www.strava.com/oauth/authorize"
TOKEN_URL = "http://www.strava.com/oauth/token"
CLIENT_ID = os.getenv("CLIENT_ID", "123")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "123456")


app = fastapi.FastAPI()


@app.get("/")
async def root(request: fastapi.Request) -> dict[str, typing.Any]:
    return dict(request.query_params.items())


@app.get("/login")
async def login() -> fastapi.responses.RedirectResponse:
    query_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "https://strava-basics.rj.r.appspot.com/callback",
        "approval_prompt": "force",
        "scope": "read",
    }
    full_url = urllib.parse.urljoin(AUTHORIZE_URL, f"{urllib.parse.urlencode(query_params)}")
    return fastapi.responses.RedirectResponse(full_url)


@app.get("/callback")
async def callback(request: fastapi.Request) -> dict[str, typing.Any]:
    response = httpx.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": request.query_params["code"],
            "grant_type": "authorization_code",
        },
    )

    return response.json()
