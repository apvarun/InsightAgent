from agno.agent import Agent
from agno.models.nvidia import Nvidia
from .tools.get_transactions import get_transactions

insight_agent = Agent(
    model=Nvidia(
        id="nvidia/llama-3.1-nemotron-nano-8b-v1",
    ),
    tools=[get_transactions],
    instructions="""
    You are an AI assistant that helps with getting insights from bunq transactions.
    """,
    show_tool_calls=True,
    markdown=True,
    use_json_mode=True,
)
