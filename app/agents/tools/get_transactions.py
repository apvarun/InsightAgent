# from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import PaymentApiObject
from agno.tools import tool

from app.utils.bunq_api import init_api_context


@tool(
    name="get_user_transactions",  # Custom name for the tool (otherwise the function name is used)
    description="Get User's transactions",  # Custom description (otherwise the function docstring is used)
    show_result=False,  # Show result after function call
)
def get_transactions() -> str:
    """
    Use this function to get all transactions.

    Returns:
        str: JSON string of transactions
    """

    print("Getting transactions...")
    init_api_context()

    payments = PaymentApiObject.list().value

    # Convert payments to JSON format
    transactions = []
    for payment in payments:
        transactions.append(payment.to_json())

    return transactions
