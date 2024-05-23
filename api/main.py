from fastapi import FastAPI, HTTPException
from src.mongo_db import get_collection
from pydantic import BaseModel

app = FastAPI()


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Say hello to a user
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Say hello to a user with ID
@app.get("/hello/user_{name}/{user_id}")
async def say_hello(user_id: int, name: str):
    response = {
        "message": f"Hello {name}",
        "user_id": user_id
    }
    return response

# Define a model for the content
class Content(BaseModel):
    title: str
    description: str

# Get content from MongoDB
@app.get("/api/content")
async def get_content():
    collection = get_collection()
    content_list = list(collection.find({}, {"_id": 0}))
    return {"content": content_list}

# Create content in MongoDB
@app.post("/api/content")
async def create_content(content: Content):
    collection = get_collection()
    collection.insert_one(content.dict())
    return {"message": "Content created successfully"}

# Update content in MongoDB
@app.put("/api/content/{title}")
async def update_content(title: str, content: Content):
    collection = get_collection()
    result = collection.update_one({"title": title}, {"$set": content.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content updated successfully"}

# Delete content in MongoDB
@app.delete("/api/content/{title}")
async def delete_content(title: str):
    collection = get_collection()
    result = collection.delete_one({"title": title})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content deleted successfully"}

    return {"content": "This is the content of the API" }
