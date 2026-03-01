# Intent-Map Agent 프로젝트 가이드

이 문서는 대량의 구글 검색 키워드를 분석하여 고객 인텐트를 도출하는 'Intent-Map Agent'의 설계 및 진행 상황을 기록합니다.

## 🎯 프로젝트 목적
- 1만~5만 개의 대규모 키워드 데이터를 의미론적으로 그룹화(Topic)하고, 각 그룹의 인텐트를 분석하여 마케팅 인사이트 도출.
- BigQuery 데이터 소스를 활용하고, Vertex AI(Gemini)를 통해 분석 자동화.

## 🏗️ 시스템 아키텍처
1. **데이터 로드:** BigQuery (서비스 계정 JSON 인증)
2. **임베딩:** Vertex AI `text-embedding-004` (Batch 처리)
3. **토픽 생성:** K-Means Clustering (200~500개 토픽)
4. **인텐트 분석:** Gemini 1.5 Flash (Async 비동기 처리)
5. **결과 출력:** Excel (`Topic Summary`, `Full Keyword List` 시트 분리)

## 🛠️ 기술 스택 및 설정 (Config)
- **Language:** Python
- **AI/ML:** Vertex AI (Embedding & Generative AI)
- **Data:** BigQuery, Pandas, Scikit-learn
- **Async:** `asyncio`, `tqdm`
- **Region:** `asia-northeast3` (가변 설정 가능)

## 📌 주요 결정 사항
- **Topic 명명:** '클러스터' 대신 '토픽(Topic)'이라는 용어를 사용함.
- **가중치 산정:** 토픽의 검색량은 해당 토픽에 속한 모든 키워드 검색량의 합계로 계산.
- **유연성:** 키워드 및 검색량 컬럼명이 변경되어도 `config.py`에서 즉시 대응 가능하도록 설계.
- **보안:** 회사 보안 정책에 따라 서비스 계정 JSON 파일을 통한 직접 인증 방식 채택.

## 📂 프로젝트 구조
```text
intent-map/
├── GEMINI.md           # 프로젝트 컨텍스트 및 가이드 (본 파일)
├── config.py           # 모든 환경 설정 정보
├── main.py             # 전체 파이프라인 실행 스크립트
├── requirements.txt    # 의존성 라이브러리
└── data/               # (추천) 중간 결과물 저장 폴더
```

## 📝 다음 작업 아이디어 (To-Do)
- [ ] 실제 BigQuery 테이블 연결 및 데이터 로드 테스트
- [ ] 토픽별 인텐트 분석을 위한 프롬프트 고도화 (산업군 특화)
- [ ] 향후 SERP(검색 결과 페이지) 데이터 수집 및 분석 모듈 추가
