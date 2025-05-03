from agno.agent import Agent
from agno.models.nvidia import Nvidia
from agno.models.google import Gemini
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.reasoning import ReasoningTools
from pydantic import BaseModel, Field
from agno.knowledge.text import TextKnowledgeBase
from agno.embedder.ollama import OllamaEmbedder
from agno.vectordb.pineconedb import PineconeDb

import os

import asyncio

from .tools.get_transactions import get_transactions
# from .tools.tools import (
#     get_transactions,
#     get_spending_summary,
#     detect_spending_anomalies,
# )

memory_db = SqliteMemoryDb(table_name="memory", db_file="tmp/memory.db")
memory = Memory(db=memory_db)


COLLECTION_NAME = "website-content"


vector_db = PineconeDb(
    name="bunq-help",
    dimension=4096,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
    api_key=os.getenv("PINECONE_API_KEY"),
    use_hybrid_search=True,
    hybrid_alpha=0.5,
    embedder=OllamaEmbedder(id="openhermes"),
)


# Create a knowledge base with the seed URLs
knowledge_base = TextKnowledgeBase(
    path="processed_content",
    # Table name: ai.website_documents
    vector_db=vector_db,
)


class InsightModel(BaseModel):
    response: str = Field(description="Response generated based on the user prompt")
    top_transactions: list[dict] = Field(
        description="Top 3 Transactions that match the query"
    )


insight_agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash",
    ),
    reasoning_model=Nvidia(
        id="deepseek-ai/deepseek-r1-distill-llama-8b",
    ),
    tools=[
        # ReasoningTools(add_instructions=True),
        get_transactions,
        # get_spending_summary,
        # detect_spending_anomalies,
    ],
    memory=memory,
    enable_agentic_memory=True,
    enable_session_summaries=True,
    description="Insight Agent for bunq",
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
        "response": "Response generated based on the user prompt. do not include transactions here. only a readable summary.", # Should answer user query here
        "all_transactions": [  # Should return all transactions that match the query here
            {
                "amount": "amount and currency",
                "created": "created",
                "description": "description",
                "alias": "alias name",
                "id": "id",
                "sub_type": "sub_type",
            },
            ...
        ]
    }
    """,
    knowledge=knowledge_base,
    search_knowledge=True,
    read_chat_history=True,
    show_tool_calls=True,
    markdown=False,
    use_json_mode=True,
    debug_mode=True,
    # response_model=InsightModel,
)


if __name__ == "__main__":
    print("Loading knowledge base...")
    asyncio.run(knowledge_base.aload(recreate=False, upsert=True))
