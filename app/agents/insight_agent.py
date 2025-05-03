from agno.agent import Agent
from agno.models.nvidia import Nvidia
from agno.models.google import Gemini

from agno.tools.reasoning import ReasoningTools

from .tools.get_transactions import get_transactions


insight_agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash",
    ),
    reasoning_model=Nvidia(
        id="deepseek-ai/deepseek-r1-distill-llama-8b",
    ),
    tools=[
        ReasoningTools(add_instructions=True), 
        get_transactions
    ],
    instructions="""
    You are an AI assistant that helps with getting insights from bunq transactions.
    You can use the following tools:
    - get_user_transactions: Get User's transactions

    You should use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Respond in following format as JSON:
    {
        "response": "Response generated based on the user prompt", # Should answer user query here
        "top_transactions": [ # Top 3 Transactions that match the query
            {
                "amount": "amount and currency",
                "created": "created",
                "description": "description",
                "alias": "alias name",
            },
            ...
        ]
    }
    """,
    show_tool_calls=True,
    markdown=False,
    use_json_mode=True,
)
