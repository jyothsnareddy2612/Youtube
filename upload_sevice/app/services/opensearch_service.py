from opensearchpy import OpenSearch
from app.core.config import settings

client = OpenSearch(
    hosts=[settings.OPENSEARCH_HOST],
    http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=False
)

INDEX_NAME = "videos"   # ✅ IMPORTANT


def index_video(video):
    try:
        document = {
            "title": video.title,
            "file_path": video.file_path,
            "id": str(video.id)
        }

        res = client.index(
            index=INDEX_NAME,
            id=str(video.id),
            body=document,
            refresh=True   # 🔥 VERY IMPORTANT
        )

        print("✅ Indexed in OpenSearch:", res)

    except Exception as e:
        print("❌ OpenSearch Index Error:", str(e))