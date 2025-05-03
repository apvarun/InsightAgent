# bunq_tools.py

import datetime
from typing import List, Dict, Optional, Any # Using older typing for broader compatibility if needed
from agno.tools import tool

# --- Placeholder Backend Logic ---
# In a real application, these functions would interact with your service
# that connects to the Bunq API, handles data storage, aggregation,
# and anomaly detection logic.

def _get_dummy_transactions(limit: int = 5) -> List[Dict[str, Any]]:
    """Generates some dummy transaction data."""
    return [
        {
            "id": f"txn_{i}",
            "amount": f"{-10.0 * i - 5.50:.2f}",
            "currency": "EUR",
            "created": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i*2)).isoformat(),
            "description": f"Sample Merchant {i}",
            "category": ["Groceries", "Dining", "Transport", "Shopping", "Utilities"][i % 5],
            "alias": "Main Account",
            "counterparty_alias": { "display_name": f"Merchant {i} BV"},
        } for i in range(limit)
    ]

def _get_dummy_summary(period: str, group_by: str, categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Generates dummy summary data."""
    if group_by == 'category':
        cats_to_use = categories or ["Groceries", "Dining", "Transport"]
        return [
            {"category": cat, "total_spent": (i + 1) * 150.75, "currency": "EUR", "transaction_count": (i + 1) * 5}
            for i, cat in enumerate(cats_to_use)
        ]
    elif group_by == 'month':
         # Simulate fetching for 'last_3_months'
         months = [(datetime.date.today() - datetime.timedelta(days=30*i)).strftime("%Y-%m") for i in range(3, 0, -1)]
         return [
             {"period": month, "total_spent": 1000 + i*150.50, "currency": "EUR"}
             for i, month in enumerate(months)
         ]
    elif group_by == 'month_and_category':
        months = [(datetime.date.today() - datetime.timedelta(days=30*i)).strftime("%Y-%m") for i in range(2, 0, -1)]
        cats_to_use = categories or ["Groceries", "Dining"]
        results = []
        for month in months:
            for j, cat in enumerate(cats_to_use):
                 results.append({
                     "period": month,
                     "category": cat,
                     "total_spent": 200 + j*50,
                     "currency": "EUR",
                     "transaction_count": 5 + j*2
                 })
        return results
    else:
        return [{"error": "Invalid group_by value"}]


def _get_dummy_anomalies(period_to_analyze: str) -> List[Dict[str, Any]]:
    """Generates dummy anomaly data."""
    # Simulate finding one anomaly
    return [
        {
            "type": "High Spending Category",
            "category": "Electronics",
            "period": period_to_analyze if period_to_analyze != "last_month" else (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m"),
            "amount": 850.00,
            "usual_average": 120.00,
            "currency": "EUR",
            "description": "Spending in Electronics was significantly higher than the 6-month average.",
            "relevant_transaction_ids": ["txn_elec_1", "txn_elec_2"]
        }
    ]

# --- Tool Definitions ---

@tool(
    name="get_user_transactions",  # Custom name for the tool (otherwise the function name is used)
    description="Get User's transactions",  # Custom description (otherwise the function docstring is used)
    show_result=False,  # Show result after function call
)
def get_transactions(
    query: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    limit: int = 10,
    sort_by: str = "created",
    sort_order: str = "desc"
) -> List[Dict[str, Any]]:
    """
    Fetches a list of user transactions based on specified criteria. Use this tool
    to find specific transactions based on keywords, date ranges, categories, or amounts,
    or when the user asks for specific transaction examples or searches.

    Args:
        query: Search term for transaction descriptions, notes, or counterparty names.
        start_date: The start date for the transaction search range (YYYY-MM-DD).
        end_date: The end date for the transaction search range (YYYY-MM-DD).
        category: Filter transactions by a specific spending category (e.g., 'Groceries', 'Transport').
        min_amount: Filter transactions greater than or equal to this amount.
        max_amount: Filter transactions less than or equal to this amount.
        limit: The maximum number of transactions to return. Defaults to 10.
        sort_by: Field to sort results by (e.g., 'created', 'amount'). Defaults to 'created'.
        sort_order: Sort order ('asc' for ascending, 'desc' for descending). Defaults to 'desc'.

    Returns:
        A list of dictionaries, each representing a transaction with details like
        id, amount, currency, created date, description, category, alias name, and counterparty alias.
    """
    print(f"--- Tool Call: get_transactions ---")
    print(f"Args: {locals()}")
    # --- Replace with actual backend/API call ---
    # This logic should filter based on all provided arguments
    transactions = _get_dummy_transactions(limit=20) # Get more initially if filtering locally
    
    # Basic filtering examples (implement actual filtering based on args)
    if category:
        transactions = [t for t in transactions if t.get('category') == category]
    if query:
         transactions = [t for t in transactions if query.lower() in t.get('description','').lower() or query.lower() in t.get('counterparty_alias',{}).get('display_name','').lower()]

    # Apply limit *after* filtering and sorting
    transactions = transactions[:limit]
    print(f"Returning {len(transactions)} transactions.")
    return transactions


@tool(
    name="get_spending_summary",
    description="Provides aggregated spending summaries for specified periods and groupings.",  # Custom description (otherwise the function docstring is used)
    show_result=False,  # Show result after function call
)
def get_spending_summary(
    period: str,
    group_by: str,
    categories: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Provides aggregated spending summaries for specified periods and groupings.
    Use this tool for questions about total spending in a period (e.g., 'last_month',
    'last_3_months', 'this_year', 'YYYY-MM'), spending trends over time, or
    spending per category. Requires specifying 'period' and 'group_by'
    (valid options: 'month', 'category', 'month_and_category').

    Args:
        period: The time period for the summary (e.g., 'last_month', 'this_month',
                'last_3_months', 'year_to_date', a specific month 'YYYY-MM',
                or a specific year 'YYYY'). This string is passed to the backend.
        group_by: How to aggregate the spending data ('month', 'category',
                  'month_and_category').
        categories: Optional list of categories to filter by (e.g., ['Groceries', 'Dining']).
                    If None, aggregates across all relevant categories for the period.

    Returns:
        A list of dictionaries containing the aggregated spending data, structured
        according to the group_by parameter. Includes period/category, total spent,
        currency, and potentially transaction count.
    """
    print(f"--- Tool Call: get_spending_summary ---")
    print(f"Args: {locals()}")
    # --- Replace with actual backend/API call ---
    # Backend should parse 'period', fetch data, aggregate, and filter by categories
    summary_data = _get_dummy_summary(period, group_by, categories)
    print(f"Returning summary data.")
    return summary_data


@tool(
    name="detect_spending_anomalies",
    description="Analyzes spending patterns for a given period to detect anomalies compared to historical data.",
    show_result=False,  # Show result after function call
)
def detect_spending_anomalies(
    period_to_analyze: str = "last_month",
    sensitivity: str = "medium"
) -> List[Dict[str, Any]]:
    """
    Analyzes spending patterns for a given period to detect anomalies compared
    to historical data. Use this tool when the user asks about anomalies or
    anything unusual in their spending.

    Args:
        period_to_analyze: The time period to analyze for anomalies
                           (e.g., 'last_month', 'this_month', 'YYYY-MM').
                           Defaults to 'last_month'. Backend resolves this string to dates.
        sensitivity: The sensitivity level for detection ('low', 'medium', 'high').
                     This influences the thresholds used for identifying anomalies.

    Returns:
        A list of dictionaries, each describing a detected anomaly. Includes anomaly type,
        details (like category, amount, comparison to average), description, currency,
        and potentially related transaction IDs. Returns an empty list if no anomalies
        are detected.
    """
    print(f"--- Tool Call: detect_spending_anomalies ---")
    print(f"Args: {locals()}")
    # --- Replace with actual backend/API call ---
    # Backend should parse 'period_to_analyze', fetch historical & current data,
    # run anomaly detection logic based on sensitivity.
    anomalies = _get_dummy_anomalies(period_to_analyze)
    print(f"Returning {len(anomalies)} anomalies.")
    return anomalies