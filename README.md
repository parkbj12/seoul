# 🏋️ 서울시 피트니스 네트워크

서울 지역의 운동 프로그램 정보를 제공하는 웹사이트입니다.

> 👥 **팀원**: 윤주성, 박병관

## 📸 스크린샷

| 지도 | 검색 | 통계 |
|:---:|:---:|:---:|
| 🗺️ 구별 프로그램 조회 | 🔍 고급 필터 검색 | 📊 차트 대시보드 |

## ✨ 주요 기능

### 🗺️ 지도 보기
- 서울시 25개 구 마커 표시
- 구 클릭 시 해당 구의 프로그램 목록 표시
- 인기 종목 요약 정보

### 🔍 고급 검색
- **지역구** 필터 (25개 구)
- **종목** 필터 (수영, 요가, 헬스 등)
- **대상** 필터 (어르신, 유아, 청소년 등)
- **키워드** 검색 (장소, 내용 등)

### 📊 통계 대시보드
- 지역구별 프로그램 수 (막대 차트)
- 종목별 분포 (도넛 차트)
- 대상별 분포 (도넛 차트)
- TOP 10 인기 장소

### ⭐ 즐겨찾기
- 관심 프로그램 저장
- 로컬스토리지 저장 (브라우저 닫아도 유지)
- 즐겨찾기 개수 뱃지 표시

### 🤖 AI 챗봇
- OpenAI GPT 기반 운동 프로그램 안내
- 자연어로 질문 가능
- 예: "강남구에서 요가 프로그램 알려줘"

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| **Backend** | Flask (Python 3.14 호환) |
| **Frontend** | HTML, CSS, JavaScript |
| **지도** | Leaflet.js |
| **차트** | Chart.js |
| **AI** | OpenAI GPT-3.5 |
| **배포** | Vercel |

## 📊 데이터

- **출처**: 서울시 생활체육포털
- **규모**: 30,000+ 프로그램
- **지역**: 서울시 25개 구
- **정보**: 종목, 대상, 일시, 장소, 연락처 등

## 🚀 로컬 실행

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 데이터 변환 (최초 1회)

```bash
python convert_data.py
```

### 3. 서버 실행

```bash
python api/index.py
```

브라우저에서 `http://localhost:5000` 접속

## ☁️ Vercel 배포

### 1. Vercel CLI 설치

```bash
npm i -g vercel
```

### 2. 배포

```bash
vercel
```

## 📁 폴더 구조

```
fitness-network/
├── api/
│   └── index.py              # Flask API 서버
├── static/
│   └── index.html            # 프론트엔드 (SPA)
├── data/
│   └── sports_data.json      # 운동 프로그램 데이터 (30,000+)
├── convert_data.py           # CSV → JSON 변환 스크립트
├── vercel.json               # Vercel 배포 설정
├── requirements.txt          # Python 패키지
├── seoul_sports.csv          # 원본 데이터 (CSV)
└── README.md
```

## 🔧 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 메인 페이지 |
| GET | `/data/sports_data.json` | 전체 데이터 |
| GET | `/api/data` | 전체 데이터 (API) |
| GET | `/api/data/<district>` | 구별 데이터 |
| GET | `/api/search?q=&district=` | 검색 |
| POST | `/api/chat` | 챗봇 대화 |

## 📝 향후 계획

- [ ] PWA 지원 (오프라인 사용)
- [ ] 프로그램 예약 기능
- [ ] 사용자 리뷰 시스템
- [ ] 위치 기반 추천

---

Made with ❤️ in Seoul
