from opensearchpy import OpenSearch
import os

client = OpenSearch(
    hosts=[os.getenv("OPENSEARCH_HOST")],
    http_auth=(
        os.getenv("OPENSEARCH_USER"),
        os.getenv("OPENSEARCH_PASSWORD")
    ),
    use_ssl=True,
    verify_certs=False
)