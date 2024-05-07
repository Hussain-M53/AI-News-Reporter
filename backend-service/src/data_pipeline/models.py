from sentence_transformers import SentenceTransformer,models
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
import os

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

word_embedding_model = models.Transformer('sentence-transformers/all-MiniLM-L6-v2')
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
embedder = SentenceTransformer(modules=[word_embedding_model, pooling_model])

pc = Pinecone(api_key='3816b11a-1e90-4da4-8972-d27b6d514fbd')
index = pc.Index("articles-data")  