from src.data_pipeline.models import embedder,index

def vectorize_category(category):
    return embedder.encode(category, convert_to_tensor=False).tolist()

def fetch_articles_by_date_and_category(date, category):
    category_vector = vectorize_category(category)

    query_response = index.query(
        vector=category_vector,
        filter={"date": {"$eq": date}},
        top_k=1000,  
        include_metadata=True
    )

    articles = {}
    for match in query_response['matches']:
        metadata = match['metadata']
        url = metadata['url']
        if url not in articles:
            articles[url] = []
        articles[url].append((int(metadata['chunk_id']), metadata['content']))

    for url in articles:
        articles[url].sort()
        articles[url] = ' '.join([chunk for _, chunk in articles[url]])

    return articles
