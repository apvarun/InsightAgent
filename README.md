# InsightAgent

InsightAgent is a Python-based application that provides transaction insights by integrating with the Bunq banking API. It leverages FastAPI for exposing endpoints, Agno for agentic workflow, Google's Gemini for AI-powered analysis, and Pinecone for efficient vector storage and retrieval. This combination enables sophisticated transaction data querying and intelligent insight generation.

Developed as part of the Bunq Hackthon 6.0.

## Features

- Integration with Bunq API for transaction data
- RESTful API endpoints for querying insights
- Sandbox environment support for testing
- Transaction analysis and overview capabilities
- AI-powered insight generation
- Vector-based knowledge search and similarity matching

## Prerequisites

- Python 3.12 or higher
- Bunq API Key (Sandbox or Production)
- Pinecone API Key
- Google Cloud API Key (for Gemini)

## Environment Setup

1. Copy the example environment configuration:
   ```bash
   cp .envrc.example .envrc
   ```

2. Edit `.envrc` with your API keys:
   ```bash
   export BUNQ_API_KEY="your_bunq_api_key_here"
   export PINECONE_API_KEY="your_pinecone_api_key_here"
   export GOOGLE_API_KEY="your_google_api_key_here"
   ```

3. Load environment variables:
   ```bash
   source .envrc
   ```

## API Endpoints

### Get Insight

```http
GET /insight?query={query}&user_id={user_id}&session_id={session_id}
```

Generates insights based on the provided query parameters.

#### Parameters

- `query` (string, required): The natural language query for insight generation
- `user_id` (string, required): Unique identifier for the user
- `session_id` (string, required): Session identifier for tracking requests


### Get Overview

```http
GET /insight/overview
```

Returns an overview of insights and transaction count for a specified time period.

#### Parameters

- `start_date` (string, optional): Start date for the overview (YYYY-MM-DD)
- `end_date` (string, optional): End date for the overview (YYYY-MM-DD)

## Dependencies

- agno >= 1.4.3
- bunq-sdk >= 1.28.0
- fastapi[standard] >= 0.112.1
- google-genai >= 1.13.0
- ollama >= 0.4.8
- openai >= 1.77.0
- uvicorn >= 0.30.6
- And more (see pyproject.toml)

## Development

### Local Development Setup

1. Set up environment variables (see Environment Setup section)

2. Run the development server:
   ```bash
   uv run fastapi dev
   ```

3. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs


### Docker Development

```bash
docker build -t insightagent .
docker run -p 8000:8000 insightagent
```


## Project Status

This project was initially developed for the Bunq Hackthon 6.0. It is currently in a proof-of-concept stage and may not be suitable for production use.

## Reference Implementation

This project serves as a reference implementation for integrating banking APIs with AI-powered analytics. While developed during a hackathon, the architecture and patterns demonstrated here can be adapted for similar financial technology applications.

Feel free to use this codebase as inspiration or a starting point for your own projects, while keeping in mind its proof-of-concept nature.


## License


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
