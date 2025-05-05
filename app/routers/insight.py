from fastapi import APIRouter
from fastapi import Request
from bunq.sdk.model.generated.endpoint import InsightApiObject, PaymentApiObject

from app.utils.bunq_api import init_api_context

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
    user_id = request.query_params.get("user_id") or 1
    session_id = request.query_params.get("session_id") or 1

    print(f"Running the query: {query}")
    response = insight_agent.run(query, user_id=user_id, session_id=session_id)

    # Remove from <thinking> to </thinking> tags
    split_text = response.content.split("</thinking>")
    response.content = split_text[1] if len(split_text) > 1 else split_text[0]

    # Remove json code block markers and strip whitespace
    cleaned_content = response.content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned_content)
    except json.JSONDecodeError:
        return cleaned_content

    return cleaned_content


@router.get("/overview")
async def get_insight_data(request: Request):
    # get query from request params
    init_api_context()

    insights = InsightApiObject.list(
        {
            "time_start": "2025-05-01",
            "time_end": "2025-05-03",
        }
    ).value

    transactions = len(PaymentApiObject.list().value)

    return {"insights": insights, "transactions": transactions}
