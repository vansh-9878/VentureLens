from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from main import startSearching

class Node(BaseModel):
    title: str
    description:str

app=FastAPI()

@app.get("/")
def status():
    return {
        "status":"Live.."
    }
    
@app.post("/api/getResults")
def solve(query:Node):
    results=startSearching(query.title,query.description)
    return{
        "status":"Successful",
        "results":results
    }
    
if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8080)