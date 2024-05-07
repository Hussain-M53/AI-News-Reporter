from src.data_pipeline.models import embedder,index

def vectorize_category(category):
    return embedder.encode(category, convert_to_tensor=False).tolist()

def fetch_articles_by_date_and_category(date, category):
    category_vector = vectorize_category(category)

    base_query_response = index.query(
        vector=category_vector,
        filter={"date": {"$eq": date}},
        top_k=1,
        include_metadata=True
    )

    articles = {}
    if base_query_response['matches']:
        base_chunk = base_query_response['matches'][0]
        metadata = base_chunk['metadata']
        url = metadata['url']
        base_chunk_id = int(metadata['chunk_id'])

        all_chunks = []
        for i in range(0, 1000): 
            if i != base_chunk_id:
                id = f"{url}_{i}"
                chunk_query = index.query(
                    id=id,
                    top_k=1,
                    include_metadata=True
                )
                if not chunk_query['matches']:
                    break
                all_chunks.append((i, chunk_query['matches'][0]['metadata']['content']))

        all_chunks.sort(key=lambda x: x[0])
        articles[url] = ' '.join([chunk[1] for chunk in all_chunks])

    for key, value in articles.items():
        return key,value
