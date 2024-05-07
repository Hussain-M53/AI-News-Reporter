from src.qa_pipeline.fetch_chunks import fetch_chunks_for_qa
from src.data_pipeline.models import embedder
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain

template = """
Context: {context}

Question: {query}

Based only on the context provided above, answer the question without using any external knowledge.

Answer:

Please add the below line after the end of response.
If you want to read the full article, please visit: {url}
"""

prompt = PromptTemplate.from_template(template)


def reorder_chunks(chunks):
    contents = []
    for match_group in chunks:
        if 'matches' in match_group:
            for match in match_group['matches']:
                content = match['metadata']['content']
                contents.append(content)
        elif 'content' in match_group:
            contents.append(match_group['content'])

    return " ".join(contents)

def generate_qa(query,date):
    vector = embedder.encode(query, convert_to_tensor=False).tolist()
    print("fetching chunks....")
    chunks,url = fetch_chunks_for_qa(vector=vector, date=date)
    if chunks != "":
        context = reorder_chunks(chunks)
        print("generating text....",context)
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        # repo_id = "google-bert/bert-large-uncased"

        llm = HuggingFaceEndpoint(
            repo_id=repo_id, max_length=128, temperature=0.5, token="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"
        )
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response = llm_chain.run({'query' : query , 'context' :context , 'url' : url})
        return response
    else:
        return "No context related to the query exist in the articles. Is there anything else I can help you with?"