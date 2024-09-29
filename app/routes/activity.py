from app.schemas.activity import DateIdeas
import fastapi
from fastapi import Path, Query
from typing import List



activities = [
    
]

router = fastapi.APIRouter()

# @router.get("/activities", response_model=List[DateIdeas])
# async def get_posts():
#     return activities

# @router.post("/activities")
# async def create(data: DateIdeas):
#     activities.append(data.model_dump())
#     return {"data": data}	

# @router.put("/activities/{id}")
# async def update(id: int, data: DateIdeas):
#     activities[id] = data.model_dump()
#     return {"data": data}

# @router.delete("/activities/{id}")
# async def delete(id: int):
#     activities.pop(id)
#     return {"data": activities}

# @router.get("/activities/{id}")
# # the id is a path parameter and must match the first parameter of the endpoint function
# async def get_by_id(id: int):
#     return {f"activities": activities[id]}