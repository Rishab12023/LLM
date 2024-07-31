import os
import json
import argparse
from dotenv import load_dotenv
from db import create_client, create_index, insert, search
from prompt import generate_prompt
from model import generate_response

def read_docs(filepath: str)->list:

    with open(filepath, "rt") as f:
        documents = json.load(f)

    docs = []
    for courses in documents:
        for doc in courses['documents']:
            doc['course'] = courses['course']
            docs.append(doc) 
    
    return docs
    
def main():

    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    

    parser = argparse.ArgumentParser(description='Query RAG Model')
    parser.add_argument('filepath', type=str, help='Json filepath for Knowledge Base')
    parser.add_argument('model_name', type=str, help='Json filepath for Knowledge Base')
    parser.add_argument('question', type=str, help='The question to ask the RAG model')
    args = parser.parse_args()

    question = args.question
    filepath = args.filepath
    model_name = args.model_name

    index_name = 'faq'
    es_client = create_client()
    create_index(es_client=es_client, index_name=index_name)
    docs = read_docs(filepath=filepath)
    insert(es_client=es_client, index_name=index_name, docs=docs)
    query_results = search(es_client=es_client, index_name=index_name, query=question)
    prompt = generate_prompt(query=question, query_res=query_results)
    response = generate_response(model_name=model_name, api_key=api_key, prompt=prompt)

    print("Ai Assitant: ",response)

if __name__ == '__main__':
    main()