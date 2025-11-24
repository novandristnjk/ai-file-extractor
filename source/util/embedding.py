from config.base import settings
import requests
import jmespath

def embed_texts(texts: str):
    payload = {
        'input': texts,
        'model': 'ebbge-m3',
    }
    resp = requests.post(f'{settings.EMBEDDING_BASE_URL}/v1/embeddings', json=payload)

    if resp.status_code > 200:
        raise Exception(f"Failed when embedding, error:\n{resp.text}")
    
    return jmespath.search("data[0].embedding", resp.json())
