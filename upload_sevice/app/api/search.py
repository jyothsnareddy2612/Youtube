from fastapi import APIRouter
from app.services.opensearch_service import client, INDEX_NAME

router = APIRouter()

@router.get("/search")
def search(query: str):
    print("🔍 Searching:", query)

    try:
        res = client.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title"],
                        "fuzziness": "AUTO"   # 🔥 KEY FIX
                    }
                }
            }
        )

        hits = res["hits"]["hits"]

        print("🔥 RAW RESULT:", hits)  # debug

        return [
            {
                "id": hit["_id"],
                "title": hit["_source"]["title"],
                "file_path": hit["_source"]["file_path"]
            }
            for hit in hits
        ]

    except Exception as e:
        print("❌ Search Error:", str(e))
        return []