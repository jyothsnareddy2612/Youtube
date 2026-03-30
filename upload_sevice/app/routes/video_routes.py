from fastapi import APIRouter
from opensearchpy import OpenSearch
import os

router = APIRouter()

client = OpenSearch(
    hosts=[os.getenv("OPENSEARCH_HOST")],
    use_ssl=True,
    verify_certs=False
)

@router.get("/search")
def search_videos(query: str):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "description"]
            }
        }
    }

    response = client.search(
        index="videos",
        body=body
    )

    results = [
        hit["_source"] for hit in response["hits"]["hits"]
    ]

    return results