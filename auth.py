import typing

import fastapi
import fastapi.security
import uvicorn

from router import router

HOST = "0.0.0.0"
PORT = 8080

app = fastapi.FastAPI()
app.include_router(router)


oauth2_authorization_code_bearer = fastapi.security.OAuth2AuthorizationCodeBearer(
    # authorizationUrl="https://strava.com/oauth2/authorize",
    # tokenUrl="https://strava.com/oauth2/token",
    authorizationUrl="http://localhost:8081/authorize",
    tokenUrl="http://localhost:8081/token",
    scopes={"read": "Read-only access", "activity:read_all": "Read all activities"},
)


async def get_token(
    request: fastapi.Request,
    oauth2_scheme: typing.Annotated[
        fastapi.security.OAuth2AuthorizationCodeBearer,
        fastapi.Depends(oauth2_authorization_code_bearer),
    ],
):
    return await oauth2_scheme(request)


@app.get("/")
async def root(token: typing.Annotated[typing.Any, fastapi.Security(get_token)]):
    return {"token": token}


if __name__ == "__main__":
    uvicorn.run("auth:app", host=HOST, port=PORT, workers=1, reload=True)
