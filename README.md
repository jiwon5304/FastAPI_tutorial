# FastAPI_tutorial

# 가상환경 설정
python3 -m venv .venv
. .venv/bin/activate

# 설치
pip install fastapi
pip install "uvicorn[standard]"

# 서버실행
uvicorn main:app --reload
