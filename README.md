# WAGYU AI Backend

WAGYU AI Backend는 반려견 정보를 기반으로 사용자의 질문에 답변하는 AI 챗봇 백엔드입니다.  
FastAPI 서버에서 GGUF 형식의 로컬 LLM을 로드하고, 사용자의 반려견 정보와 질문을 프롬프트에 반영하여 답변을 생성합니다.

## 주요 기능

- FastAPI 기반 AI 챗봇 API 제공
- llama.cpp 기반 GGUF 모델 로컬 추론
- 반려견 이름, 견종, 나이, 기존 질병 정보를 프롬프트에 반영
- `/ai/ask` 엔드포인트를 통한 AI 답변 생성
- `/` 엔드포인트를 통한 서버 상태 확인

## 기술 스택

- Python 3.12
- FastAPI
- Uvicorn
- llama-cpp-python
- Pydantic
- GGUF Model

## 프로젝트 구조

```bash
WAGYU_aiback/
├── main.py                 # FastAPI 서버 진입점
├── pyproject.toml          # 프로젝트 의존성 및 Python 버전 설정
├── uv.lock                 # uv 패키지 잠금 파일
├── prompt/
│   └── prompt.py           # AI 시스템 프롬프트 생성 로직
├── utils/
│   ├── ask.py              # 요청/응답 Pydantic 스키마
│   └── threadupdate.py     # 사용자 정보 DB 초기화 로직
└── README.md
```

## 실행 준비

### 1. 저장소 클론

```bash
git clone https://github.com/capstone-WAGYU/WAGYU_aiback.git
cd WAGYU_aiback
```

### 2. Python 버전 확인

이 프로젝트는 Python 3.12 이상을 사용합니다.

```bash
python --version
```

### 3. 패키지 설치

`uv`를 사용하는 경우:

```bash
uv sync
```

또는 `pip`를 사용하는 경우:

```bash
pip install fastapi "uvicorn[standard]" llama-cpp-python requests
```

### 4. 모델 파일 준비

GGUF 모델 파일을 준비한 뒤, 모델 경로를 환경변수로 설정합니다.

```bash
mkdir models
```

Linux / macOS:

```bash
export MODEL_PATH="./models/capstone-q4-k-m.gguf"
```

Windows PowerShell:

```powershell
$env:MODEL_PATH="./models/capstone-q4-k-m.gguf"
```

> 모델 파일은 용량이 크기 때문에 Git에 포함하지 않습니다.  

## 서버 실행

```bash
uvicorn main:APP --host 0.0.0.0 --port 8000 --reload
```

서버가 실행되면 아래 주소에서 확인할 수 있습니다.

```text
http://localhost:8000
```

## API 명세

### Health Check

서버 상태를 확인합니다.

```http
GET /
```

#### Response

```json
{
  "status": "ok"
}
```

---

### AI 질문 요청

반려견 정보와 질문을 전달하면 AI가 답변을 생성합니다.

```http
POST /ai/ask
```

#### Request Body

```json
{
  "userid": "user-1",
  "species": "말티즈",
  "name": "뽀삐",
  "age": 5,
  "disease": ["슬개골 탈구"],
  "text": "산책을 얼마나 자주 시켜야 하나요?"
}
```

| 필드 | 타입 | 필수 여부 | 설명 |
|---|---|---|---|
| userid | string | 선택 | 사용자 ID |
| species | string | 필수 | 반려견 견종 |
| name | string | 필수 | 반려견 이름 |
| age | integer | 필수 | 반려견 나이 |
| disease | string[] | 필수 | 기존 질병 또는 유전병 목록 |
| text | string | 필수 | 사용자 질문 |

#### Response

```json
{
  "userid": "user-1",
  "text": "AI가 생성한 답변"
}
```

## 요청 예시

### curl

```bash
curl -X POST "http://localhost:8000/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "userid": "user-1",
    "species": "말티즈",
    "name": "뽀삐",
    "age": 5,
    "disease": ["슬개골 탈구"],
    "text": "산책을 얼마나 자주 시켜야 하나요?"
  }'
```

## 환경변수

| 이름 | 설명 | 예시 |
|---|---|---|
| MODEL_PATH | 로드할 GGUF 모델 파일 경로 | `./models/capstone-q4-k-m.gguf` |

## 모델 로딩 방식

서버 시작 시 FastAPI lifespan에서 `MODEL_PATH` 환경변수를 읽고, 해당 경로의 GGUF 모델을 `llama-cpp-python`으로 로드합니다.

현재 설정값은 다음과 같습니다.

```python
n_ctx = 4096
n_gpu_layers = 24
chat_format = "qwen2"
```

## 개발 참고사항

현재 `/ai/ask` 엔드포인트는 요청으로 받은 반려견 정보를 시스템 프롬프트에 포함한 뒤, 사용자의 질문을 LLM에 전달하는 구조입니다.

프롬프트에 반영되는 정보는 다음과 같습니다.

- 반려견 이름
- 견종
- 나이
- 기존 질병 및 유전병
- 사용자 질문

## 주의사항

이 서비스는 AI 챗봇 기반 답변을 제공하는 백엔드입니다.  
반려견의 실제 질병 진단이나 치료는 반드시 수의사의 진료를 통해 판단해야 합니다.

## License

별도 라이선스가 명시되어 있지 않습니다.
