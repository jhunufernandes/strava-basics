import typing
import uvicorn

import fastapi
import fastapi.security


HOST = "0.0.0.0"
PORT = 8080


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


@app.get("/")
async def root(token: typing.Annotated[typing.Any, fastapi.Security(get_token)]):
    return {"token": token}


if __name__ == "__main__":
    uvicorn.run("auth:app", host=HOST, port=PORT, workers=1)
