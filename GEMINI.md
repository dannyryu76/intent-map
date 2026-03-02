# Intent-Map Agent 프로젝트 가이드

이 문서는 대량의 구글 검색 키워드를 분석하여 고객 인텐트를 도출하는 'Intent-Map Agent'의 설계 및 진행 상황을 기록합니다.

## 🎯 프로젝트 목적
- 1만~5만 개의 대규모 키워드 데이터를 의미론적으로 그룹화(Topic)하고, 각 그룹의 인텐트를 분석하여 마케팅 인사이트 도출.
- BigQuery 데이터 소스를 활용하고, Vertex AI(Gemini)를 통해 분석 자동화.

## 🏗️ 시스템 아키텍처
1. **데이터 로드:** BigQuery (비용 효율적 단일 스캔, 메타데이터 포함)
2. **복구 시스템:** 단계별 체크포인트 (CSV/NPY 캐싱) 및 Gemini CLI Restore 활성화
3. **임베딩:** Vertex AI `text-embedding-004` (Batch 처리)
4. **토픽 생성:** K-Means Clustering (200~500개 토픽)
5. **인텐트 분석:** Gemini 1.5 Flash (Async 비동기 처리)
6. **결과 출력:** Excel (`Topic Summary`, `Full Keyword List` 시트 분리)

## 🛠️ 기술 스택 및 설정 (Config)
- **Language:** Python
- **AI/ML:** Vertex AI (Embedding & Generative AI)
- **Data:** BigQuery, Pandas, Scikit-learn
- **Async:** `asyncio`, `tqdm`
- **Region:** `asia-northeast3`

## 📌 주요 결정 사항
- **비용 최적화:** 빅쿼리 과금 방식(Columnar)에 맞춰 키워드와 메타데이터를 한 번에 스캔하여 스캔 비용 최소화.
- **안정성(Restore):** 임베딩 및 클러스터링 결과를 로컬에 캐싱하여 중단 시 해당 지점부터 재개 가능.
- **메타데이터 유지:** 국가, 제품, 카테고리, CEJ 등 비즈니스 메타데이터를 로드 시점부터 최종 결과물까지 유지.
- **CLI 복구:** `.gemini/settings.json`을 통해 도구 실행 전 상태 자동 백업 활성화.

## 📂 프로젝트 구조
```text
intent-map/
├── .gemini/
│   └── settings.json   # Gemini CLI 설정 (Checkpointing 활성화)
├── data/               # 중간 결과물(캐시) 및 최종 엑셀 저장
├── config.py           # 모든 환경 설정 및 메타데이터 컬럼 정의
├── main.py             # 전체 파이프라인 실행 스크립트
├── requirements.txt    # 의존성 라이브러리
└── GEMINI.md           # 프로젝트 컨텍스트 및 가이드 (본 파일)
```

## ✅ 완료된 작업
- [x] BigQuery 데이터 로드 및 메타데이터(Country, Product 등) 연동
- [x] 단계별 체크포인트(Restore) 로직 구현 (BQ 데이터, 임베딩, 클러스터링)
- [x] Gemini CLI 복구(Checkpointing) 설정 완료
- [x] 비용 효율적인 단일 스캔 쿼리 적용

## 📝 다음 작업 아이디어 (To-Do)
- [ ] 실제 BigQuery 테이블 연결 및 데이터 로드 테스트
- [ ] 토픽별 인텐트 분석을 위한 프롬프트 고도화 (산업군 특화)
- [ ] 결과 엑셀 파일 내 시각화(차트 등) 자동 생성 모듈 검토
