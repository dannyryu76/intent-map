import os

# ==========================================
# 1. GCP 및 프로젝트 설정 (본인 환경에 맞게 수정)
# ==========================================
CONFIG = {
    # GCP 프로젝트 ID와 Vertex AI 리전
    "PROJECT_ID": "your-gcp-project-id",
    "LOCATION": "asia-northeast3",  # 서울 리전 (원하는 리전으로 변경 가능)
    
    # 서비스 계정 JSON 파일 경로 (절대 경로 혹은 상대 경로)
    # 보안을 위해 이 경로는 .gitignore에 추가되어 GitHub에 올라가지 않습니다.
    "JSON_KEY_PATH": "credentials/service-account.json",
    
    # BigQuery 테이블 정보
    "BQ_TABLE_ID": "your-project.your_dataset.your_table",
    
    # 분석 대상 컬럼명 (데이터에 맞게 수정)
    "COL_KEYWORD": "keyword",        # 키워드 텍스트 컬럼
    "COL_VOLUME": "search_volume",   # 검색량 컬럼 (없을 경우 임의 값 세팅 필요)
    
    # [NEW] 추가 메타데이터 컬럼
    "COL_METADATA": ["country", "product", "category", "cej"], 
    
    # 분석 파라미터
    "NUM_TOPICS": 300,               # 생성할 토픽(클러스터)의 개수 (200~500 권장)
    "EMBED_BATCH_SIZE": 250,         # Vertex AI 임베딩 API 배치 크기
    "MAX_CONCURRENCY": 10,           # Gemini API 동시 호출 제한 (비동기 속도 조절)
    
    # 모델 설정
    "EMBEDDING_MODEL": "text-embedding-004",
    "GENAI_MODEL": "gemini-1.5-flash", # 인텐트 분석을 위한 모델 (Flash 권장)
    
    # 결과 출력 설정
    "OUTPUT_DIR": "data",
    "OUTPUT_FILE": "intent_analysis_result.xlsx",
    
    # [NEW] 복구(Restore) 및 체크포인트 설정
    "USE_RESTORE": True,              # True일 경우 중간 저장된 파일이 있으면 활용
    "CACHE_BQ_DATA": "data/bq_raw_data.csv",
    "CACHE_EMBEDDINGS": "data/embeddings.npy",
    "CACHE_CLUSTERS": "data/clustered_data.csv"
}

# 출력 폴더 자동 생성
if not os.path.exists(CONFIG["OUTPUT_DIR"]):
    os.makedirs(CONFIG["OUTPUT_DIR"])
