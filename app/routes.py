from flask import Blueprint, render_template, request
from elasticsearch import Elasticsearch
from es_config.config import ELASTIC_HOST, ELASTIC_PORT  # Update the import if necessary

main = Blueprint('main', __name__)

# Add the 'scheme' parameter to the Elasticsearch client initialization
es = Elasticsearch([{'host': ELASTIC_HOST, 'port': ELASTIC_PORT, 'scheme': 'http'}])

INDEX_NAME = 'movies'

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract fields from the form
        title = request.form.get('title', '').strip()
        cast = request.form.get('cast', '').strip()
        year = request.form.get('year', '').strip()
        genres = request.form.get('genres', '').strip()
        # If all fields are empty, show an error
        if not any([title, cast, year, genres]):
            flash("At least one search field must be filled out.", "error")
            return render_template('index.html')

        # Redirect to the search function with the inputs
        return search(title, cast, year, genres)

    return render_template('index.html')

def search(title, cast, year, genres):
    """
    Perform a search query on Elasticsearch using the provided fields.
    """
    if es is None:
        flash("Elasticsearch connection is not available. Please contact the administrator.", "error")
        return render_template('index.html')

    try:
        # Build the Elasticsearch query dynamically
        must_clauses = []

        if title:
            must_clauses.append({"match": {"title": title}})
        if cast:
            must_clauses.append({"match": {"cast": cast}})
        if year:
            must_clauses.append({"match": {"year": year}})
        if genres:
            must_clauses.append({"match": {"genres": genres}})

        query_body = {
            "query": {
                "bool": {
                    "must": must_clauses  # Combine all the search fields using "must"
                }
            }
        }

        # Perform the search
        results = es.search(index=INDEX_NAME, body=query_body)

        # Extract results and handle pagination (if needed)
        hits = results.get('hits', {}).get('hits', [])
        if not hits:
            flash("No results found for the provided search criteria.", "info")

        return render_template('results.html', title=title,
            cast=cast,
            year=year,
            genres=genres ,results=hits)
    except Exception as e:
        flash(f"An error occurred while searching: {e}", "error")
        return render_template('index.html')