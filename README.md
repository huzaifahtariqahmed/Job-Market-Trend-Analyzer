# Job Market Trend Analyzer

An AI-powered system that scrapes job postings, stores them in a vector database, and enables semantic search + trend analysis on skills and roles.

## Features
- Scrapes job postings (Rozee, LinkedIn, Indeed)
- Embeds job descriptions using SentenceTransformers
- Stores embeddings in FAISS/Chroma/AstraDB
- FastAPI endpoints for querying jobs and trends
- Deployable on AWS (EC2 + S3) with Docker

## Tech Stack
- LangChain
- FastAPI
- Vector DBs: FAISS / Chroma / AstraDB
- AWS (EC2, S3)
- Docker

# 🚀 Build Instructions

To set up the project environment:

```bash
# Create a new environment from environment.yml
conda env create -f environment.yml

# Activate the environment (replace 'env_name' with the one in environment.yml)
conda activate env_name

# Update the environment after modifying environment.yml
conda env update -f environment.yml --prune

# (Optional) Update requirements.txt from current environment
make update-reqs