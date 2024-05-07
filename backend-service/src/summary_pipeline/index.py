from src.summary_pipeline.fetch_articles import fetch_articles_by_date_and_category
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain

def summarize_articles(articles,llm):
    summaries = {}
    for url, content in articles.items():
        prompt = [f"summarize: {content}"]  # Note the change here to make it a list
        # Use Hugging Face endpoint to get the summary
        summary_text = llm.generate(prompt)  # Now prompt is a list
        summary = summary_text['choices'][0]['text']
        summaries[url] = f"{summary}\n\nIf you want to read the full article, please visit: {url}"
    return summaries



def generate_summary(date,category):
    repo_id = "google-bert/bert-large-uncased"
    llm = HuggingFaceEndpoint(repo_id=repo_id, token="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", max_length=128)
    
    articles = fetch_articles_by_date_and_category(date,category)

    summaries = summarize_articles(articles,llm)

    for url, summary in summaries.items():
        print(summary)
        print("\n---\n")