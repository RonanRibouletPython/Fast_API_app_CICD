from fastapi import FastAPI, Path, Query
from app.schemas.date_ideas import DateIdeas
from typing import List

app = FastAPI()

activities = [
    
]

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/activities", response_model=List[DateIdeas])
async def get_posts():
    return activities

@app.post("/activities")
async def create(data: DateIdeas):
    activities.append(data.model_dump())
    return {"data": data}	

@app.get("/activities/{id}")
# the id is a path parameter and must match the first parameter of the endpoint function
async def get_by_id(
    id: int = Path(..., description="The ID of the activity you wanna retrieve", gt=0, lt=10),
    q: str = Query(None, max_length=5),
    ):
    return {f"activities": activities[id], "q": q}
