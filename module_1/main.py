import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import create_client, create_index, insert, search
from prompt import generate_prompt
from model import generate_response


app = FastAPI()

class QueryRequest(BaseModel):
    filepath: str
    model_name: str
    question: str



def read_docs(filepath: str)->list:

    with open(filepath, "rt") as f:
        documents = json.load(f)

    docs = []
    for courses in documents:
        for doc in courses['documents']:
            doc['course'] = courses['course']
            docs.append(doc) 
    
    return docs
    

@app.on_event("startup")
async def startup_event():
    load_dotenv()

@app.post("/query/")
async def query_rag_model(request: QueryRequest):
    try:
        api_key = os.getenv("MISTRAL_API_KEY")
        question = request.question
        filepath = request.filepath
        model_name = request.model_name

        index_name = 'faq'
        es_client = create_client()
        create_index(es_client=es_client, index_name=index_name)
        docs = read_docs(filepath=filepath)
        insert(es_client=es_client, index_name=index_name, docs=docs)
        query_results = search(es_client=es_client, index_name=index_name, query=question)
        prompt = generate_prompt(query=question, query_res=query_results)
        response = generate_response(model_name=model_name, api_key=api_key, prompt=prompt)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))