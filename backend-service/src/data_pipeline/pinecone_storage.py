from src.data_pipeline.models import index,embedder,text_splitter

def store_articles_in_pinecone(data):
    upsert_data = []
    print("storing in pinecone ......")
    for idx, article in data.iterrows():
        chunks = text_splitter.split_text(article['content'])
        for chunk_id, chunk_text in enumerate(chunks):
            vector = embedder.encode(chunk_text, convert_to_tensor=False).tolist()

            metadata = { 
                'url': article['url'],
                'title': article['title'],
                'date': str(article['published']),
                'chunk_id': chunk_id,
                'content' : chunk_text  
            }

            single_upsert_data = {
                'id': f"{article['url']}_{chunk_id}",
                'values': vector ,
                'metadata': metadata
            }
            
            upsert_data.append(single_upsert_data)
        print("storing chunk",article['url'])
        index.upsert(vectors=upsert_data, namespace='')
