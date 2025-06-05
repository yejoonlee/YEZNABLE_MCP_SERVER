from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "awake"}

# 로컬 실행용 코드 (Render 배포 시 필요 없음)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
