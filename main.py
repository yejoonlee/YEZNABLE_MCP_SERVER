from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import shutil
import os
from dotenv import load_dotenv

from openapi_schema import schema  # 별도 파일로 저장된 스키마 import

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

app = FastAPI(openapi_url=None)

# CORS 설정: GPT 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요시 도메인 제한 가능
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

# 📘 /openapi.json → Custom GPT에서 참조
@app.get("/openapi.json", dependencies=[Depends(verify_token)])
def serve_openapi_schema():
    return JSONResponse(content=schema)


# 🛠️ Models
class Command(BaseModel):
    command: str

class PathInput(BaseModel):
    path: str

class PathWithContent(BaseModel):
    path: str
    content: str = ""

class PathWithNewPath(BaseModel):
    path: str
    new_path: str


# 🔧 /run
@app.post("/run", dependencies=[Depends(verify_token)])
def run_command(data: Command):
    subprocess.Popen(data.command, shell=True)
    return {"status": "Command executed"}

# 🔧 /run-and-capture
@app.post("/run-and-capture", dependencies=[Depends(verify_token)])
def run_command_and_capture(data: Command):
    try:
        result = subprocess.run(data.command, shell=True, capture_output=True, text=True, timeout=600)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

# 🔧 /file/create
@app.post("/file/create", dependencies=[Depends(verify_token)])
def create_file(data: PathWithContent):
    try:
        with open(data.path, "w") as f:
            f.write(data.content)
        return {"status": f"File created at {data.path}"}
    except Exception as e:
        return {"error": str(e)}

# 🔧 /file/delete
@app.post("/file/delete", dependencies=[Depends(verify_token)])
def delete_path(data: PathInput):
    try:
        if os.path.isdir(data.path):
            shutil.rmtree(data.path)
        elif os.path.isfile(data.path):
            os.remove(data.path)
        else:
            return {"error": "Path does not exist"}
        return {"status": f"Deleted {data.path}"}
    except Exception as e:
        return {"error": str(e)}

# 🔧 /file/rename
@app.post("/file/rename", dependencies=[Depends(verify_token)])
def rename_path(data: PathWithNewPath):
    try:
        os.rename(data.path, data.new_path)
        return {"status": f"Renamed to {data.new_path}"}
    except Exception as e:
        return {"error": str(e)}

# 🔧 /file/copy
@app.post("/file/copy", dependencies=[Depends(verify_token)])
def copy_path(data: PathWithNewPath):
    try:
        if os.path.isdir(data.path):
            shutil.copytree(data.path, data.new_path)
        elif os.path.isfile(data.path):
            shutil.copy2(data.path, data.new_path)
        else:
            return {"error": "Source path does not exist"}
        return {"status": f"Copied to {data.new_path}"}
    except Exception as e:
        return {"error": str(e)}
