from src.summary_pipeline.fetch_articles import fetch_articles_by_date_and_category
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


template = """
Context: {context}

Based only on the context provided above, summarize the content.

Summary:

Please add the below line after the end of the summary.
If you want to read the full article, please visit: {url}
"""

prompt = PromptTemplate.from_template(template)


def summarize_articles(content,url):
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    # repo_id = "google-bert/bert-large-uncased"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id, max_length=512, temperature=0.5, token="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"
    )
    streaming_callback = StreamingStdOutCallbackHandler()
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run({'context' :content, 'url' : url})

def generate_summary(date,category):
    url,content = fetch_articles_by_date_and_category(date,category)
    summary = summarize_articles(content=content, url=url)
    return summary