from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import shutil

app = FastAPI()

class CommandInput(BaseModel):
    command: str

class FileOperation(BaseModel):
    path: str
    content: str = None
    new_path: str = None

@app.post("/run")
def run_command(cmd: CommandInput):
    try:
        subprocess.Popen(cmd.command, shell=True)
        return {"status": "executed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run-and-capture")
def run_command_and_capture(cmd: CommandInput):
    try:
        result = subprocess.run(cmd.command, shell=True, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/create")
def create_file(op: FileOperation):
    try:
        os.makedirs(os.path.dirname(op.path), exist_ok=True)
        with open(op.path, "w") as f:
            f.write(op.content or "")
        return {"status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/delete")
def delete_file(op: FileOperation):
    try:
        if os.path.isfile(op.path):
            os.remove(op.path)
        elif os.path.isdir(op.path):
            shutil.rmtree(op.path)
        else:
            raise FileNotFoundError("Not found")
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/rename")
def rename_file(op: FileOperation):
    try:
        os.rename(op.path, op.new_path)
        return {"status": "renamed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/copy")
def copy_file(op: FileOperation):
    try:
        if os.path.isfile(op.path):
            shutil.copy(op.path, op.new_path)
        elif os.path.isdir(op.path):
            shutil.copytree(op.path, op.new_path)
        else:
            raise FileNotFoundError("Not found")
        return {"status": "copied"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
