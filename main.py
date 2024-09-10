# import datetime

# import uvicorn
# from fastapi import FastAPI

# # from auth import router as auth_router

# app = FastAPI()


# @app.get("/")
# async def root() -> list[datetime.datetime]:
#     dummy_times = [
#         datetime.datetime(2018, 1, 1, 10, 0, 0),
#         datetime.datetime(2018, 1, 2, 10, 30, 0),
#         datetime.datetime(2018, 1, 3, 11, 0, 0),
#     ]

#     return dummy_times


# app.include_router(auth_router, prefix="/auth")


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8080, workers=1)
