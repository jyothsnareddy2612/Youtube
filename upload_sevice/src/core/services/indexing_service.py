from src.data.clients.opensearch_client import client

INDEX_NAME = "videos"


def index_video(video):
    try:
        document = {
            "title": video.title,
            "file_path": video.file_path,
            "id": str(video.id),
        }

        response = client.index(
            index=INDEX_NAME,
            id=str(video.id),
            body=document,
            refresh=True,
        )
        print("Indexed in OpenSearch:", response)
    except Exception as exc:
        print("OpenSearch Index Error:", str(exc))
