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