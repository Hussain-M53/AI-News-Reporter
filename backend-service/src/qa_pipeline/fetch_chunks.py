from src.data_pipeline.models import index
from langchain_core.prompts import PromptTemplate

def generate_queries(model,prompt, num_queries):
  query_generation_prompt = PromptTemplate.from_template("Given the prompt: '{prompt}', generate {num_queries} questions that are better articulated. Return in the form of an list. For example: ['question 1', 'question 2', 'question 3']")
  query_generation_chain = query_generation_prompt | model
  return str_to_json(query_generation_chain.invoke({"prompt": prompt, "num_queries": num_queries}).content)


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
    if len(query_response['matches']) > 0 and query_response['matches'][0]['score'] >= 0.5:
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
        
        return [prev_chunk, query_response ,next_chunk],url
    else:
        return "","";