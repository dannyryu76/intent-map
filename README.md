# 🔍 Intent-Map Agent: Large-scale Search Intent Analyzer

**Intent-Map Agent**는 구글 검색 키워드 데이터를 대량으로 수집하고 분석하여 고객의 '숨은 의도(Intent)'를 도출하는 AI 기반 데이터 파이프라인입니다.

Google BigQuery에 저장된 수만 개의 키워드를 **Vertex AI(Gemini)**와 **Clustering(군집화)** 기술을 활용해 의미론적으로 묶고, 각 그룹의 핵심 인텐트를 자동 생성합니다.

---

## 🚀 Key Features
- **Scalable Processing:** 1만~5만 개의 대규모 키워드 데이터를 효율적으로 처리.
- **Cost Efficiency:** 모든 키워드를 개별 분석하는 대신, 임베딩 기반 군집화(Clustering)를 통해 분석 비용을 획기적으로 절감.
- **Async Execution:** `asyncio`와 `Semaphore`를 활용하여 수백 개의 토픽을 고속으로 분석.
- **Deep Insight:** Gemini 1.5 Flash 모델이 각 토픽의 대표 명칭과 구체적인 고객 니즈를 생성.
- **GCP Native:** BigQuery와 Vertex AI(text-embedding-004)를 직접 연동하여 최적의 성능 발휘.

---

## 🛠 Tech Stack
- **Language:** Python 3.10+
- **AI Models:** 
  - Vertex AI `text-embedding-004` (Embedding)
  - Vertex AI `gemini-1.5-flash` (Intent Analysis)
- **Data Engineering:** BigQuery, Pandas, Scikit-learn (K-Means)
- **Operation:** Asyncio, Tqdm (Progress Bar)
- **Output:** Microsoft Excel (xlsx)

---

## 📂 Project Structure
```text
intent-map/
├── config.py           # GCP 프로젝트, 빅쿼리 테이블, 모델 설정
├── main.py             # 전체 분석 파이프라인 실행 스크립트
├── requirements.txt    # 필수 라이브러리 목록
├── GEMINI.md           # 개발 설계 및 상세 가이드
└── .gitignore          # 보안을 위한 설정 (Credentials, Data 제외)
```

---

## ⚙️ Setup & Usage

### 1. 환경 설정 (GCP Credentials)
- GCP 서비스 계정을 생성하고 `BigQuery Data Viewer`, `Vertex AI User` 권한을 부여합니다.
- 서비스 계정 JSON 키 파일을 다운로드하여 `credentials/` 폴더 내에 저장합니다.

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. Config 수정
`config.py` 파일을 열어 본인의 GCP 프로젝트 정보와 빅쿼리 테이블 정보를 입력합니다.
```python
CONFIG = {
    "PROJECT_ID": "your-project-id",
    "BQ_TABLE_ID": "project.dataset.table",
    "COL_KEYWORD": "keyword",
    "JSON_KEY_PATH": "credentials/service-account.json"
}
```

### 4. 실행
```bash
python main.py
```

---

## 📊 Output Result
분석이 완료되면 `data/` 폴더에 엑셀 파일이 생성됩니다.
1. **Topic Summary:** 군집별 대표 명칭, 인텐트 설명, 검색량 합계.
2. **Full Keyword List:** 각 원본 키워드가 어떤 토픽에 속하는지 매핑된 상세 리스트.

---

## 🤝 Contribution
개선 제안이나 버그 리포트는 이슈(Issue)를 통해 남겨주세요!
