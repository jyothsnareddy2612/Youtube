from src.data.clients.opensearch_client import client

INDEX_NAME = "videos"


def search_videos(query: str):
    response = client.search(
        index=INDEX_NAME,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title"],
                    "fuzziness": "AUTO",
                }
            }
        },
    )

    return [
        {
            "id": hit["_id"],
            "title": hit["_source"]["title"],
            "file_path": hit["_source"]["file_path"],
        }
        for hit in response["hits"]["hits"]
    ]
