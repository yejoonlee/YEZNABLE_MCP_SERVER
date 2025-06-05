from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class EmployeeRequest(BaseModel):
    employee_id: str

@app.post("/get_employee_info")
def get_employee_info(req: EmployeeRequest):
    # 실제 DB 연동 대신 예시 응답
    dummy_db = {
        "E123": {"name": "김지원", "department": "데이터팀", "position": "데이터 엔지니어"},
        "E456": {"name": "박민수", "department": "마케팅팀", "position": "팀장"},
    }
    return dummy_db.get(req.employee_id, {"error": "해당 사번의 직원 정보를 찾을 수 없습니다."})

# 로컬 실행용 코드 (Render 배포 시 필요 없음)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)