from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import Request

from ..agents.insight_agent import insight_agent

import json

router = APIRouter(
    prefix="/insight",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_insight(request: Request):
    # get query from request params
    query = request.query_params.get("query")

    print(f"Running the query: {query}")
    response = insight_agent.run(query)

    print(response.content)

    # Remove json code block markers and strip whitespace
    cleaned_content = response.content.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned_content)
    except json.JSONDecodeError:
        return cleaned_content

    return cleaned_content
