# import minsearch
from typing import List, Dict, Union
from elasticsearch import Elasticsearch
from tqdm import tqdm

def create_index(es_client: Elasticsearch, index_name: str)->None:
    try:
        if not es_client.indices.exists(index=index_name):
            index_settings = {
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    },
                    "mappings": {
                        "properties": {
                            "text": {"type": "text"},
                            "section": {"type": "text"},
                            "question": {"type": "text"},
                            "course": {"type": "keyword"} 
                        }
                    }
                }
            index_name = index_name
            es_client.indices.create(index=index_name, body=index_settings)
            print(f"Index '{index_name}' Created Successfully.")
        else:
            print(f"Index '{index_name}' already exists !!")
    except Exception as e:
        print(f"Exception Raised :'{e}'")

    

def create_client(uri: str="http://localhost:9200")->Elasticsearch:
    es_client = Elasticsearch(uri)
    return es_client

def insert(es_client: Elasticsearch, index_name, docs: Union[List[Dict], List[str]])->None:
    for doc in docs:
        es_client.index(index=index_name, document=doc)


def search(es_client: Elasticsearch, index_name: str, query: str, top_k: int=5)-> List[str]:
    search_query = {
        "size": top_k,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs