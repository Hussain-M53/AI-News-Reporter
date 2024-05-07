from src.data_pipeline.models import index

def fetch_chunks_for_qa(vector,date):
    query_response = index.query(
                    namespace = '',
                    vector=vector,
                    filter={
                        "date": date
                    },
                    top_k=1,
                    include_values=False,
                    include_metadata=True,
    )
    print(query_response)
    if len(query_response['matches']) <=0:
        return "","";
    curr_chunk = query_response['matches'][0]['metadata']
    chunk_id = int(curr_chunk['chunk_id'])
    url = curr_chunk['url']

    prev_chunk_id = chunk_id - 1
    next_chunk_id = chunk_id + 1

    prev_chunk = index.query(
        namespace = '',
        id = url + "_" + str(prev_chunk_id),
        top_k=1,
        include_metadata=True
    )
    
    next_chunk = index.query(
        namespace = '',
        id = url + "_" + str(next_chunk_id),
        top_k=1,
        include_metadata=True
    )
    
    return [prev_chunk, curr_chunk ,next_chunk],url