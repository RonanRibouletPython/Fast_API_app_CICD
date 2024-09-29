from app.schemas.activity import DateIdeas
import fastapi
from fastapi import Path, Query
from typing import List


users = [
    
]

router = fastapi.APIRouter()

@router.get("/users", response_model=List[DateIdeas])
async def get_posts():
    return users

@router.post("/users")
async def create(data: DateIdeas):
    users.append(data.model_dump())
    return {"data": data}	

@router.get("/users/{id}")
# the id is a path parameter and must match the first parameter of the endpoint function
async def get_by_id(id: int):
    return {f"activities": users[id]}