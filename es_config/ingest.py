import json
import os
from elasticsearch import Elasticsearch, helpers
from config import ELASTIC_HOST, ELASTIC_PORT

# Elasticsearch connection
es = Elasticsearch([{'host': ELASTIC_HOST, 'port': ELASTIC_PORT, 'scheme': 'http'}])

INDEX_NAME = 'movies'

# Get the absolute path to the movies.json file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(CURRENT_DIR, '../dataset/movies.json')
    
def create_index():
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        es.indices.create(
            index=INDEX_NAME,
            body={
                "settings": {
                "index": {
                    "number_of_shards":1,
                    "number_of_replicas": 1 # Default is 1; you can adjust this if needed
                } 
            },
                "mappings": {
                    "properties": {
                        "title": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "year": {"type": "integer"},
                        "cast": {"type": "text"},
                        "genres": {"type": "keyword"} 


                    }
                }
            }
        )
        print(f"Index '{INDEX_NAME}' created.")

def ingest_data():
    try:
        with open(DATASET_PATH, 'r',encoding='utf-8') as file:
            movies = json.load(file)
            actions = [
                {
                    "_index": INDEX_NAME,
                    "_source": movie
                } for movie in movies
            ]
            helpers.bulk(es, actions)
            print("Data ingested successfully.")
    except FileNotFoundError:
        print(f"Error: File not found at path {DATASET_PATH}. Please check the file location.")

if __name__ == "__main__":
    create_index()
    ingest_data()
