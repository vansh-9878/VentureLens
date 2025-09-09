from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from main import startSearching
import os
from dotenv import load_dotenv
load_dotenv()

class Node(BaseModel):
    title: str
    description:str
class PasswordNode(BaseModel):
    password:str

password=os.getenv("PASSWORD")
app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # includes OPTIONS, GET, POST, etc.
    allow_headers=["*"],
)


@app.get("/")
def status():
    return {
        "status":"Live.."
    }
    
@app.post("/api/getResults")
def solve(query:Node):
    results=startSearching(query.title,query.description)
    print(results)
    return{
        "status":"Successful",
        "results":results
    }
    
@app.post("/password")
def checkPassword(auth:PasswordNode):
    if(password==auth.password):
        return {
            "status":True
        }
    else:
        return{
            "status":False
        }
    
    
if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8000)