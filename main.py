from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

BASE_PATH = "/tmp/gpt_mcp"

class FileRequest(BaseModel):
    filename: str
    content: str

class FolderRequest(BaseModel):
    foldername: str

@app.get("/ping")
def ping():
    return {"status": "awake"}

@app.post("/create-folder")
def create_folder(req: FolderRequest):
    path = os.path.join("/tmp", req.foldername)
    os.makedirs(path, exist_ok=True)
    return {"message": f"Folder created at {path}"}

@app.post("/write-file")
def write_file(req: FileRequest):
    os.makedirs(BASE_PATH, exist_ok=True)
    filepath = os.path.join(BASE_PATH, req.filename)
    try:
        with open(filepath, "w") as f:
            f.write(req.content)
        return {"message": f"File written to {filepath}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-files")
def list_files():
    if not os.path.exists(BASE_PATH):
        return {"files": []}
    files = os.listdir(BASE_PATH)
    return {"files": files}

@app.get("/read-file")
def read_file(filename: str = Query(...)):
    filepath = os.path.join(BASE_PATH, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with open(filepath, "r") as f:
            content = f.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-file")
def delete_file(filename: str = Query(...)):
    filepath = os.path.join(BASE_PATH, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        os.remove(filepath)
        return {"message": f"Deleted {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear-folder")
def clear_folder():
    if not os.path.exists(BASE_PATH):
        return {"message": "Folder does not exist, nothing to clear"}
    try:
        for f in os.listdir(BASE_PATH):
            path = os.path.join(BASE_PATH, f)
            if os.path.isfile(path):
                os.remove(path)
        return {"message": "All files deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 로컬 실행용 코드 (Render 배포 시 필요 없음)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
