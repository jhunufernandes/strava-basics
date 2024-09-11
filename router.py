import fastapi

router = fastapi.APIRouter()


@router.get("/callback")
async def callback(request: fastapi.Request):
    print(request.query_params)
    return


@router.get("/authorize")
async def authorize(request: fastapi.Request):
    print(request.query_params)
    return


@router.get("/token")
async def token(request: fastapi.Request):
    print(request.query_params)
    return
