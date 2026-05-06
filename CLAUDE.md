# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

영수증 이미지를 업로드하면 Upstage Vision LLM으로 OCR 파싱하여 지출 내역을 자동 관리하는 웹 앱. 1일 스프린트로 구축하는 프로젝트로, 상세 요구사항은 `PRD_영수증_지출관리앱.md`에 있다.

- **프론트엔드**: React 18 + Vite 5 + TailwindCSS 3 + Axios (`frontend/` 디렉토리)
- **백엔드**: FastAPI + LangChain + Upstage Vision (`backend/` 디렉토리)
- **데이터 저장**: DB 없이 JSON 파일(`backend/data/expenses.json`)
- **배포**: Vercel (프론트+백엔드 통합)

## 개발 명령어

### 백엔드

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 프론트엔드

```bash
cd frontend
npm install
npm run dev        # 개발 서버 (port 5173)
npm run build      # 프로덕션 빌드
npm run preview    # 빌드 결과 미리보기
```

## 환경 변수

`.env` 파일에 설정 (루트 및 `backend/` 디렉토리):

```
UPSTAGE_API_KEY=...          # Upstage Vision OCR API
GROQ_API_KEY=...             # Groq LLM (보조)
VITE_API_BASE_URL=...        # 프론트엔드에서 백엔드 URL
DATA_FILE_PATH=data/expenses.json
```

## 아키텍처

```
사용자 브라우저 (React)
    ↓ HTTP (Axios)
FastAPI 백엔드
    ↓ LangChain
Upstage Vision LLM (ChatUpstage)
    ↓
JSON 파일 스토리지
```

### 백엔드 구조 (`backend/`)

```
main.py              # FastAPI 앱 진입점, CORS 설정
routers/
  upload.py          # POST /upload - 영수증 이미지 파싱
  expenses.py        # GET/DELETE/PUT /expenses
  summary.py         # GET /summary
services/
  ocr_service.py     # LangChain + Upstage Vision 파싱 로직
  storage_service.py # expenses.json 읽기/쓰기
data/
  expenses.json      # 지출 데이터 저장소
```

**OCR 흐름**: 이미지 수신 → Base64 인코딩 → ChatUpstage 호출 → JSON 추출 → expenses.json 저장

### 프론트엔드 구조 (`frontend/`)

```
src/
  pages/
    Dashboard.jsx    # 대시보드 (요약 + 목록)
    Upload.jsx       # 영수증 업로드 및 파싱 결과 편집
    Detail.jsx       # 지출 상세 보기
  components/        # 공통 컴포넌트
  api/
    client.js        # Axios 인스턴스 및 API 함수
```

## 데이터 스키마

```json
{
  "id": "uuid",
  "created_at": "ISO8601",
  "store_name": "상점명",
  "receipt_date": "YYYY-MM-DD",
  "items": [{"name": "항목명", "quantity": 1, "price": 1000}],
  "total_amount": 10000,
  "category": "식비",
  "payment_method": "신용카드",
  "memo": "메모",
  "image_path": "uploads/uuid.jpg"
}
```

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/upload` | 영수증 이미지 업로드 + OCR 파싱 |
| GET | `/expenses` | 지출 목록 조회 (필터: date, category) |
| GET | `/expenses/{id}` | 지출 상세 조회 |
| PUT | `/expenses/{id}` | 지출 정보 수정 |
| DELETE | `/expenses/{id}` | 지출 삭제 |
| GET | `/summary` | 기간별 합계, 카테고리별 통계 |

## 주요 제약사항

- **파일 업로드**: JPG, PNG, PDF만 허용, 최대 10MB
- **인증 없음**: 단일 사용자 가정
- **Vercel 서버리스 제약**: 파일시스템 `/tmp`만 쓰기 가능 → KV 스토리지 폴백 고려
- **응답 시간**: OCR < 10초, 목록 조회 < 1초

## UI 디자인 시스템

- **폰트**: Pretendard (CDN)
- **색상**: TailwindCSS 기본 팔레트, 주색상 `blue-600`
- **지원 화면**: 모바일(375px) / 태블릿(768px) / 데스크톱(1280px)
- **샘플 이미지**: `images/` 디렉토리에 테스트용 영수증 이미지 11장 포함

## Vercel 배포 설정

`vercel.json`에서 빌드 및 라우팅 설정:
- 프론트엔드: Vite 빌드 → 정적 파일 서빙
- 백엔드: FastAPI → `/api/*` 경로로 라우팅


### Git Push 작업은 반드시 확인을 받고 처리하세요!!!!(매우 중요)
### Source Code가 변경되거나 라이브러리 버전이 변경되면 반드시 @PRD_영수증_지출관리앱.md 같이 업데이트 한 이후 완료 기준의 check box에 완료된 사항들도 모두 체크표시 하세요.

