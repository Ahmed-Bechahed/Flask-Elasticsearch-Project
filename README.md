# Flask Elasticsearch Project

A web application that allows users to search for movies dynamically using Elasticsearch. This project is containerized using Docker and managed with Docker Compose for easy deployment and scalability.

## Features
- **Dynamic Movie Search**: Search for movies by title, cast, year, or genres.
- **Flask Backend**: A lightweight and robust Python web framework.
- **Elasticsearch Integration**: High-performance search engine for querying movie data.
- **Dockerized Deployment**: Easily run the application using Docker Compose.
- **Preloaded Dataset**: Includes a sample `movies.json` dataset for Elasticsearch ingestion.

---

## Project Structure

```plaintext
flask-elasticsearch-project/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # Application routes
│   ├── templates/
│   │   ├── base.html         # Base HTML template
│   │   ├── index.html        # Search form template
│   │   └── results.html      # Results page template
│   ├── static/
│   │   └── style.css         # Application styles
├── elasticsearch/
│   ├── config.py             # Elasticsearch configuration
│   └── ingest.py             # Script for ingesting movie data
├── dataset/
│   └── movies.json           # Sample movie dataset
├── Dockerfile                # Dockerfile for building the app container
├── docker-compose.yml        # Docker Compose configuration
├── run.py                    # Main entry point for the app
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

---

## Prerequisites

Ensure the following tools are installed on your system:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/flask-elasticsearch-project.git
   cd flask-elasticsearch-project
2. **Build and Run Containers:**:
 ```bash
 docker-compose up --build

3. **Access the Application:** :

Open your browser and navigate to: http://localhost:5000
Ingest Data into Elasticsearch:

The elasticsearch/ingest.py script is run automatically as part of the docker-compose.yml setup. This ingests the movies.json dataset into Elasticsearch.

Technologies Used
Backend: Flask
Search Engine: Elasticsearch
Frontend: HTML, CSS
Containerization: Docker, Docker Compose
