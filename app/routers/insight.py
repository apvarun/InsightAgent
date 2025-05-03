from fastapi import APIRouter, Depends, HTTPException

from ..agents.insight_agent import insight_agent


router = APIRouter(
    prefix="/insight",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_insight():

    insight_agent.print_response("Summarize the top 5 transactions", stream=False)

    return []

