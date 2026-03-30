from opensearchpy import OpenSearch

from src.config.settings import settings

client = OpenSearch(
    hosts=[settings.OPENSEARCH_HOST],
    http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=False,
)
