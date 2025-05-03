from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ..agents.insight_agent import insight_agent


router = APIRouter(
    prefix="/insight",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)



@router.get("/")
async def get_insight():
    response = insight_agent.run("Summarize the top 5 transactions")
            
    return response.content
