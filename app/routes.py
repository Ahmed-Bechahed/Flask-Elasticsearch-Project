from flask import Blueprint, render_template, request, flash
from elasticsearch import Elasticsearch
from es_config.config import ELASTIC_HOST, ELASTIC_PORT

main = Blueprint('main', __name__)

# Elasticsearch connection

es = Elasticsearch([{'host': ELASTIC_HOST, 'port': ELASTIC_PORT, 'scheme': 'http'}])

INDEX_NAME = 'movies'

@main.route('/', methods=['GET', 'POST'])
def index():

    """
    Render the search form and handle form submissions.
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        cast = request.form.get('cast', '').strip()
        year = request.form.get('year', '').strip()
        genres = request.form.getlist('genres')  # Retrieve selected genres as a list

        if not any([title, cast, year, genres]):
            flash("At least one search field must be filled out.", "error")
            return render_template('index.html')

        # Redirect to the search function with the inputs

        return search(title, cast, year, genres)

    return render_template('index.html')

@main.route('/movie/<movie_id>')
def movie_details(movie_id):
    """
    Show the details of a specific movie.
    """
    if es is None:
        flash("Elasticsearch connection is not available. Please contact the administrator.", "error")
        return render_template('index.html')

    try:
        # Perform the search to get the specific movie details by ID
        response = es.get(index=INDEX_NAME, id=movie_id)

        # Extract the movie details from the response
        movie = response['_source']

        return render_template('movie_details.html', movie=movie)

    except Exception as e:
        flash(f"An error occurred while retrieving movie details: {e}", "error")
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

            must_clauses.append({"match_phrase": {"title": title}})
        if cast:
            must_clauses.append({"match_phrase": {"cast": cast}})
        if year:
            must_clauses.append({"term": {"year": year}})

        # Ensure all selected genres are included in the search (OR condition)
        # if genres:
        #     must_clauses.append({"terms": {"genres": genres}})
            
        # Ensure all selected genres are included in the search (AND condition)
        if genres:
            for genre in genres:
                must_clauses.append({"match": {"genres": genre}})

        query_body = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": must_clauses  # Combine all the search fields using "must"
                }
            },
            "collapse": {
                "field": "title.keyword"  # Collapse based on the unique title
            }
        }

        # Perform the search
        results = es.search(index=INDEX_NAME, body=query_body)

        # Extract results and handle pagination (if needed)
        hits = results.get('hits', {}).get('hits', [])
        total_results = results.get('hits', {}).get('total', {}).get('value', 0)

        if not hits:
            flash("No results found for the provided search criteria.", "info")

        return render_template(
            'results.html',
            title=title,
            cast=cast,
            year=year,
            genres=genres,
            results=hits,
            total_results=total_results
        )
    except Exception as e:
        flash(f"An error occurred while searching: {e}", "error")
        return render_template('index.html')

