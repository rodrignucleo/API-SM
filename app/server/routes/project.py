from fastapi import APIRouter, Body, Depends, Request
from server.auth.auth_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from server.auth.auth_handler import get_user_id_from_token

from server.database import (
    add_project,
    delete_project,
    retrieve_project,
    retrieve_projects,
    update_project,
)
from server.models.project import (
    ErrorResponseModel,
    ResponseModel,
    ProjectSchema,
    UpdateProjectModel,
)

router = APIRouter()


@router.post("/", dependencies=[Depends(JWTBearer())], response_description="Project data added into the database")
async def add_project_data(request: Request, project: ProjectSchema = Body(...)):
    user_id = await get_user_id_from_token(request.headers["authorization"][7:])
    if (user_id):
        project = jsonable_encoder(project)
        new_project = await add_project(project, user_id)
        return ResponseModel(new_project, "Project added successfully.")
    else: 
        return ResponseModel({
            "status_code": 401,
            "message": "User not authorized"
        }, "Project added successfully.")



@router.get("/", dependencies=[Depends(JWTBearer())], response_description="Projects retrieved")
async def get_projects(request: Request):
    # print(request.headers["authorization"])
    user_id = await get_user_id_from_token(request.headers["authorization"][7:])
    # print(user_id)
    projects = await retrieve_projects(user_id)
    if projects:
        return ResponseModel(projects, "Projects data retrieved successfully")
    return ResponseModel(projects, "Empty list returned")


@router.get("/{id}", dependencies=[Depends(JWTBearer())], response_description="Project data retrieved")
async def get_project_data(id):
    project = await retrieve_project(id)
    if project:
        return ResponseModel(project, "Project data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Project doesn't exist.")


@router.put("/{id}")
async def update_project_data(id: str, req: UpdateProjectModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_project = await update_project(id, req)
    if updated_project:
        return ResponseModel(
            "Project with ID: {} name update is successful".format(id),
            "Project name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the project data.",
    )


@router.delete("/{id}", response_description="Project data deleted from the database")
async def delete_project_data(id: str):
    deleted_project = await delete_project(id)
    if deleted_project:
        return ResponseModel(
            "Project with ID: {} removed".format(id), "Project deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Project with id {0} doesn't exist".format(id)
    )
