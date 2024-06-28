import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.ProjectAS
project_collection = database.get_collection("projects_collection")
user_collection = database.get_collection("users_collection")

#projects
def project_helper(project) -> dict:
    return {
        "id": str(project["_id"]),  
        "name": project["name"],
        "description": project["description"],
        "owner": str(project["owner"]),
        "team": [(str(user["user_id"]), user["role"]) for user in project["team"]],
        "tasks": [
            {
                "id": str(task["assigned_to"]),
                "title": task["title"],
                "description": task["description"],
                "due_date": task["due_date"],
            } for task in project["tasks"]],
        "documents": [
            {
                "name": doc.get("name",""),
                "file_url": doc.get("file_url","")
            } for doc in project.get("documents", [])],
        "milestones": [
            {
                "name": milestone["name"],
                "due_date": milestone["due_date"]
            } for milestone in project["milestones"]],
        "reminders": [
            {
                "name": reminder["name"],
                "due_date": reminder["due_date"]
            } for reminder in project["milestones"]],
        "budget": {
            "total": project["budget"]["total"],
            "spent": project["budget"]["spent"],
            "remaining": project["budget"]["remaining"]
        }
    }



# Retrieve all projects present in the database
async def retrieve_projects(user_id: str):
    projects = []
    async for project in project_collection.find({
        "$or": [
            {"owner": user_id},
            {"team": {"$elemMatch": {"user_id": user_id}}}
        ]
    }):
        projects.append(project_helper(project))
    return projects


# Add a new project into the database
async def add_project(project_data: dict, user_id: str) -> dict:
    project_data["owner"] = user_id
    project = await project_collection.insert_one(project_data)
    new_project = await project_collection.find_one({"_id": project.inserted_id})
    return project_helper(new_project)


# Retrieve a project with a matching ID
async def retrieve_project(id: str) -> dict:
    project = await project_collection.find_one({"_id": ObjectId(id)})
    if project:
        return project_helper(project)


# Update a project with a matching ID
async def update_project(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    project = await project_collection.find_one({"_id": ObjectId(id)})
    if project:
        updated_project = await project_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_project:
            return True
        return False


# Delete a project from the database
async def delete_project(id: str):
    project = await project_collection.find_one({"_id": ObjectId(id)})
    if project:
        await project_collection.delete_one({"_id": ObjectId(id)})
        return True



#users
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),  
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "projects": [{"project_id": str(project["project_id"]), "role": project["role"]} for project in user["projects"]]
    }


# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into the database
async def add_user(user_data: dict) -> dict:
    user_data["password"] = hash_password(user_data["password"])
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def authenticate_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return user
    return None

# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

# Retrieve a user with a matching email
async def retrieve_user_email(email: str) -> dict:
    user = await user_collection.find_one({"email": email})
    if user:
        return user_helper(user)


# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
