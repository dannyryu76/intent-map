import asyncio
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account
import vertexai
from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import GenerativeModel
from sklearn.cluster import KMeans
from tqdm.asyncio import tqdm

# 설정 불러오기
from config import CONFIG

# 인증 초기화
if os.path.exists(CONFIG["JSON_KEY_PATH"]):
    credentials = service_account.Credentials.from_service_account_file(CONFIG["JSON_KEY_PATH"])
else:
    print(f"⚠️ 경고: '{CONFIG['JSON_KEY_PATH']}' 경로에 서비스 계정 키 파일이 없습니다.")
    print("환경 변수를 통한 인증을 시도합니다.")
    credentials = None

vertexai.init(
    project=CONFIG["PROJECT_ID"], 
    location=CONFIG["LOCATION"], 
    credentials=credentials
)
bq_client = bigquery.Client(credentials=credentials, project=CONFIG["PROJECT_ID"])

def fetch_bq_data():
    """BigQuery에서 검색 데이터를 로드합니다."""
    query = f"SELECT {CONFIG['COL_KEYWORD']}, {CONFIG['COL_VOLUME']} FROM `{CONFIG['BQ_TABLE_ID']}`"
    print(f"📡 BigQuery 데이터 로드 중: {CONFIG['BQ_TABLE_ID']}")
    return bq_client.query(query).to_dataframe()

def get_embeddings(texts):
    """Vertex AI를 사용하여 키워드 임베딩 벡터를 생성합니다."""
    model = TextEmbeddingModel.from_pretrained(CONFIG["EMBEDDING_MODEL"])
    embeddings = []
    print(f"🧬 키워드 임베딩 생성 중 (Total: {len(texts)})...")
    
    for i in range(0, len(texts), CONFIG["EMBED_BATCH_SIZE"]):
        batch = texts[i : i + CONFIG["EMBED_BATCH_SIZE"]].tolist()
        batch_embeddings = model.get_embeddings(batch)
        embeddings.extend([e.values for e in batch_embeddings])
    
    return np.array(embeddings)

async def analyze_topic_intent(semaphore, model, topic_id, keywords):
    """Gemini를 통해 토픽의 인텐트 및 특징을 비동기로 분석합니다."""
    async with semaphore:
        prompt = f"""
        당신은 검색 트렌드 분석가입니다. 아래 키워드 뭉치는 하나의 공통된 '토픽'으로 분류된 데이터입니다.
        
        [키워드 샘플]:
        {', '.join(keywords[:20])} 
        
        [지시 사항]:
        1. 이 토픽을 대표할 수 있는 직관적인 '토픽명'을 만드세요.
        2. 이 토픽을 검색한 사용자들의 주된 '고객 인텐트(의도)'를 1~2문장으로 분석하세요.
        
        [출력]:
        토픽명: <명칭>
        인텐트: <분석 내용>
        """
        try:
            # Vertex AI SDK는 현재 동기 기반이므로 ThreadPool을 활용해 비동기처럼 처리
            response = await asyncio.to_thread(model.generate_content, prompt)
            res_text = response.text.strip()
            
            name_part = res_text.split("토픽명:")[1].split("인텐트:")[0].strip()
            intent_part = res_text.split("인텐트:")[1].strip()
            return {"topic_id": topic_id, "topic_name": name_part, "intent": intent_part}
        except Exception as e:
            return {"topic_id": topic_id, "topic_name": "Error", "intent": f"분석 오류: {str(e)}"}

async def main():
    # 1. 데이터 로드
    df = fetch_bq_data()
    
    # 2. 임베딩 생성 (5만 개 기준 약 수 분 소요)
    embeddings = get_embeddings(df[CONFIG["COL_KEYWORD"]])
    
    # 3. 토픽(클러스터) 생성
    print(f"🧩 {CONFIG['NUM_TOPICS']}개의 토픽으로 군집화 중...")
    kmeans = KMeans(n_clusters=CONFIG["NUM_TOPICS"], random_state=42, n_init=10)
    df["topic_id"] = kmeans.fit_predict(embeddings)
    
    # 4. 토픽 요약 (검색량 합계 및 대표 키워드 추출)
    topic_summary = df.groupby("topic_id").agg({
        CONFIG["COL_VOLUME"]: "sum",
        CONFIG["COL_KEYWORD"]: lambda x: x.tolist()
    }).reset_index()
    topic_summary.rename(columns={CONFIG["COL_VOLUME"]: "topic_volume"}, inplace=True)
    
    # 5. Gemini 비동기 분석
    print(f"🧠 Gemini 인텐트 분석 시작 (동시성: {CONFIG['MAX_CONCURRENCY']})...")
    gemini_model = GenerativeModel(CONFIG["GENAI_MODEL"])
    semaphore = asyncio.Semaphore(CONFIG["MAX_CONCURRENCY"])
    
    tasks = [
        analyze_topic_intent(semaphore, gemini_model, row["topic_id"], row[CONFIG["COL_KEYWORD"]])
        for _, row in topic_summary.iterrows()
    ]
    
    results = await tqdm.gather(*tasks)
    results_df = pd.DataFrame(results)
    
    # 6. 최종 데이터 병합
    final_topic_df = pd.merge(topic_summary, results_df, on="topic_id")
    final_full_df = pd.merge(df, final_topic_df[["topic_id", "topic_name", "intent", "topic_volume"]], on="topic_id")
    
    # 7. 엑셀 저장
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], CONFIG["OUTPUT_FILE"])
    with pd.ExcelWriter(output_path) as writer:
        # 토픽 요약 시트
        final_topic_df.drop(columns=[CONFIG["COL_KEYWORD"]]).to_excel(writer, sheet_name="Topic Summary", index=False)
        # 전체 키워드 상세 시트
        final_full_df.to_excel(writer, sheet_name="Full Keyword List", index=False)
        
    print(f"
🎉 모든 분석이 완료되었습니다!")
    print(f"📁 결과 파일: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
