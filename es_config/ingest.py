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
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "year": {"type": "integer"},
                        "cast": {"type": "text"},
                        "genres": {"type": "keyword"}  # Added genres as an array of keywords

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
