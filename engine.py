"""
engine.py

Three usable use cases, each with two response modes for the same
incoming query:

- generic_response(): what a policy-lookup / generic chatbot answer
  looks like today (the "before" in the strategy doc's before/after
  table).
- point_response(): a single, precise, state-grounded sentence,
  generated from the unified state layer (the "after").

Classification is deliberately simple (keyword-based) — the point of
this demo is to make the STATE-AWARENESS contrast visible and
explainable in a Loom walkthrough, not to ship a production NLU stack.
"""

from state_layer import (
    get_customer,
    get_order_state,
    get_refund_state,
    get_ticket_state,
    sla_remaining_hours,
)

ORDER_KEYWORDS = ["order", "package", "delivery", "shipment", "shipping", "track"]
REFUND_KEYWORDS = ["refund", "money back", "reimburse"]
TICKET_KEYWORDS = ["ticket", "issue", "bug", "access", "not working", "request", "support case"]

USE_CASES = {
    "order": {
        "label": "\ud83d\udce6 Order status",
        "example": "Where is my order? Has it shipped yet?",
    },
    "refund": {
        "label": "\ud83d\udcb8 Refund status",
        "example": "What's the status of my refund?",
    },
    "ticket": {
        "label": "\ud83c\udfab Support ticket status",
        "example": "Any update on my support ticket?",
    },
}


def classify(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ORDER_KEYWORDS):
        return "order"
    if any(k in q for k in REFUND_KEYWORDS):
        return "refund"
    if any(k in q for k in TICKET_KEYWORDS):
        return "ticket"
    return "unknown"


def generic_response(category: str) -> str:
    if category == "order":
        return (
            "Thank you for your order. Standard delivery takes 5\u20137 business "
            "days. You will receive an email once your order ships. For "
            "further query, please press \u201cConnect to agent.\u201d"
        )
    if category == "refund":
        return (
            "Apologies for the inconvenience. As per our policy, refunds take "
            "15 days to process. Please wait till then. For further query, "
            "please press \u201cConnect to agent.\u201d"
        )
    if category == "ticket":
        return (
            "Thank you for reaching out. Your request has been logged and a "
            "support representative will get back to you as soon as possible. "
            "We appreciate your patience."
        )
    return (
        "Thanks for your message. A support representative will review your "
        "query and respond shortly."
    )


def point_response(category: str, customer_id: str) -> tuple[str, dict]:
    """Returns (response_text, state_used) — state_used is shown in the demo
    UI so it's visible *why* the answer is precise, not just that it is."""
    customer = get_customer(customer_id)
    name = customer.get("name", "there")

    if category == "order":
        state = get_order_state(customer_id)
        if not state:
            return generic_response(category), {}
        text = (
            f"Hi {name}, your order {state['order_id']} ({state['items']}) is "
            f"currently \u201c{state['stage']}\u201d via {state['carrier']} "
            f"(tracking {state['tracking_number']}), expected by "
            f"{state['expected_date'].strftime('%d %b %Y')}."
        )
        return text, state

    if category == "refund":
        state = get_refund_state(customer_id)
        if not state:
            return generic_response(category), {}
        text = (
            f"Hi {name}, apologies for the inconvenience \u2014 your refund "
            f"({state['refund_id']}, {state['amount']}) is currently at the "
            f"\u201c{state['stage']}\u201d stage and should complete by "
            f"{state['expected_date'].strftime('%d %b %Y')}."
        )
        return text, state

    if category == "ticket":
        state = get_ticket_state(customer_id)
        if not state:
            return generic_response(category), {}
        remaining = sla_remaining_hours(state)
        urgency = (
            f"{remaining}h remaining on your {state['severity']} SLA"
            if remaining >= 0
            else f"SLA breached by {abs(remaining)}h \u2014 escalating"
        )
        text = (
            f"Hi {name}, your ticket {state['ticket_id']} "
            f"({state['category']}, {state['severity']}) is currently: "
            f"\u201c{state['stage']}.\u201d Owner: {state['owner']}. {urgency}."
        )
        return text, state

    return generic_response(category), {}
