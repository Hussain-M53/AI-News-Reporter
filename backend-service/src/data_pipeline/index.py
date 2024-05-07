from src.data_pipeline.web_scraping import web_scrape_articles
from src.data_pipeline.pinecone_storage import store_articles_in_pinecone


def collect_data():
    articles = web_scrape_articles()
    store_articles_in_pinecone(articles)
    