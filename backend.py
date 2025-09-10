from fastapi import FastAPI,Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from main import startSearching
from datetime import datetime,timedelta
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import os,jwt
from dotenv import load_dotenv
load_dotenv()
from slowapi import Limiter
from slowapi.util import get_remote_address


class Node(BaseModel):
    title: str
    description:str
    apiKey:str

class PasswordNode(BaseModel):
    password:str

password=os.getenv("PASSWORD")
app=FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


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
    
    
SECRET_KEY = os.getenv("SECRET")  # use env var in prod
ALGORITHM = "HS256"

@app.post("/auth/token")
def generate_token():
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"exp": expiration, "iat": datetime.utcnow()}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

# --- Step 2: Dependency to verify JWT ---
security = HTTPBearer()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


    
@app.post("/api/getResults")
def solve(query:Node,payload: dict = Depends(verify_jwt)):
    results=startSearching(query.title,query.description)
    print(results)
    return{
        "status":"Successful",
        "results":results,
        "user":payload
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