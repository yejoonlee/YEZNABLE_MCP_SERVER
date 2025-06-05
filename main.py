from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

class FileRequest(BaseModel):
    path: str  # 절대 또는 상대 경로 포함
    content: str

class FolderRequest(BaseModel):
    path: str  # 만들고 싶은 폴더 경로

@app.get("/ping")
def ping():
    return {"status": "awake"}

@app.post("/create-folder")
def create_folder(req: FolderRequest):
    try:
        os.makedirs(req.path, exist_ok=True)
        return {"message": f"Folder created at {req.path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/write-file")
def write_file(req: FileRequest):
    folder = os.path.dirname(req.path)
    try:
        os.makedirs(folder, exist_ok=True)
        with open(req.path, "w") as f:
            f.write(req.content)
        return {"message": f"File written to {req.path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-files")
def list_files(folder: str = Query("/tmp")):
    if not os.path.exists(folder):
        return {"files": []}
    try:
        files = os.listdir(folder)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-files-recursive")
def list_files_recursive(folder: str = Query("/tmp")):
    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail="Folder not found")
    try:
        file_tree = {}
        for root, dirs, files in os.walk(folder):
            rel_root = os.path.relpath(root, folder)
            file_tree[rel_root] = files
        return {"file_tree": file_tree}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read-file")
def read_file(path: str = Query(...)):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with open(path, "r") as f:
            content = f.read()
        return {"path": path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-file")
def delete_file(path: str = Query(...)):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        os.remove(path)
        return {"message": f"Deleted {path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear-folder")
def clear_folder(folder: str = Query(...)):
    if not os.path.exists(folder):
        return {"message": "Folder does not exist, nothing to clear"}
    try:
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            if os.path.isfile(path):
                os.remove(path)
        return {"message": "All files deleted in folder"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 로컬 실행용 코드 (Render 배포 시 필요 없음)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
