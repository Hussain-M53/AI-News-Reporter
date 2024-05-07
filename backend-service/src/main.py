from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI,Query
from src.data_pipeline.index import collect_data
from src.qa_pipeline.index import generate_qa
from src.summary_pipeline.index import generate_summary
from datetime import datetime
    
load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello World"}

@app.get("/gather")
def gather_data():
    collect_data()
    return {"data scraped successfully"}

@app.get("/qa") 
def get_qa(query: str = Query(..., description="Query to generate QA from"),
           date: str = Query(..., description="Date associated with the query")):
    res = generate_qa(query, date)
    return {
        "Status Code" : 200,
        "Response" : res
    }

@app.get("/summarize") 
def get_summary(category: str = Query(..., description="Category to summarize"),
                date: str = Query(..., description="Date for the category summary")):
    res = generate_summary(date, category)
    return {
        "Status Code" : 200,
        "Response" : res
    }