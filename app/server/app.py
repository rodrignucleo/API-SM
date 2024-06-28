from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes.user import router as UserRouter
from server.routes.project import router as ProjectRouter
from server.routes.auth import router as AuthRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(ProjectRouter, tags=["Project"], prefix="/project")
app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Put /docs after the URL in order to access!"}
