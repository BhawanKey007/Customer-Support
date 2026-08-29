"""
state_layer.py

Simulates the ONE thing the strategy claims incumbents don't have:
a unified, live view of "state" pulled from systems that would normally
be disconnected (CRM, order/fulfillment system, payments/ops backend,
ticketing system).

In a real deployment this module would call out to a client's actual
CRM / order-management / ticketing / payments APIs. Here it's mocked so
the demo runs with zero external dependencies and no API keys.

Three use cases are covered, each with a full record per customer, so
you can switch customers in the sidebar and try any of the three:

  1. Order status   ("where is my order?")
  2. Refund status   ("where is my refund?")
  3. Support ticket status ("what's happening with my ticket?")
"""

from datetime import date, timedelta

TODAY = date(2026, 8, 29)

# ---- Mocked CRM: who is asking -------------------------------------------------
CUSTOMERS = {
    "cust_1001": {"name": "Aditi Sharma", "email": "aditi@example.com", "plan": "Pro"},
    "cust_1002": {"name": "Marco Bellini", "email": "marco@example.com", "plan": "Growth"},
    "cust_1003": {"name": "Wei Chen", "email": "wei@example.com", "plan": "Pro"},
}

# ---- Mocked order/fulfillment system: order tracking state ---------------------
ORDERS = {
    "cust_1001": {
        "order_id": "ORD-70142",
        "items": "Wireless Keyboard, USB-C Hub",
        "stage": "Out for delivery",
        "carrier": "BlueDart",
        "tracking_number": "BD9981223IN",
        "expected_date": TODAY + timedelta(days=0),
        "placed_on": TODAY - timedelta(days=4),
    },
    "cust_1002": {
        "order_id": "ORD-70188",
        "items": "Standing Desk Converter",
        "stage": "Delayed at regional hub \u2014 customs check",
        "carrier": "DHL Express",
        "tracking_number": "DHL5523190EU",
        "expected_date": TODAY + timedelta(days=4),
        "placed_on": TODAY - timedelta(days=9),
    },
    "cust_1003": {
        "order_id": "ORD-70201",
        "items": "Noise-Cancelling Headphones",
        "stage": "Packed \u2014 awaiting carrier pickup",
        "carrier": "FedEx",
        "tracking_number": "FX7712004US",
        "expected_date": TODAY + timedelta(days=2),
        "placed_on": TODAY - timedelta(days=1),
    },
}

# ---- Mocked payments/ops backend: refund pipeline state ------------------------
REFUNDS = {
    "cust_1001": {
        "refund_id": "RF-88213",
        "amount": "\u20b94,200",
        "stage": "Approved \u2014 funds released to bank",
        "expected_date": TODAY + timedelta(days=2),
        "requested_on": TODAY - timedelta(days=6),
    },
    "cust_1002": {
        "refund_id": "RF-88240",
        "amount": "\u20ac89.00",
        "stage": "Under finance review",
        "expected_date": TODAY + timedelta(days=5),
        "requested_on": TODAY - timedelta(days=1),
    },
    "cust_1003": {
        "refund_id": "RF-88265",
        "amount": "$54.00",
        "stage": "Processed \u2014 refund complete",
        "expected_date": TODAY - timedelta(days=1),
        "requested_on": TODAY - timedelta(days=8),
    },
}

# ---- Mocked ticketing system: PwC-style severity/SLA governed tickets ----------
TICKETS = {
    "cust_1001": {
        "ticket_id": "TCK-55266",
        "category": "Billing Question",
        "severity": "P2",
        "sla_hours": 24,
        "opened_hours_ago": 3,
        "stage": "Assigned \u2014 awaiting first response",
        "owner": "Support Engineer: A. Verma",
    },
    "cust_1002": {
        "ticket_id": "TCK-55231",
        "category": "Feature Not Working",
        "severity": "P2",
        "sla_hours": 24,
        "opened_hours_ago": 20,
        "stage": "Change request approved \u2014 deployment scheduled",
        "owner": "Support Engineer: N. Fontana",
    },
    "cust_1003": {
        "ticket_id": "TCK-55210",
        "category": "Access Query",
        "severity": "P1",
        "sla_hours": 8,
        "opened_hours_ago": 5,
        "stage": "Root Cause Analysis in progress \u2014 pending client sign-off",
        "owner": "Support Engineer: R. Iyer",
    },
}


def get_customer(customer_id: str) -> dict:
    return CUSTOMERS.get(customer_id, {})


def get_order_state(customer_id: str) -> dict | None:
    return ORDERS.get(customer_id)


def get_refund_state(customer_id: str) -> dict | None:
    return REFUNDS.get(customer_id)


def get_ticket_state(customer_id: str) -> dict | None:
    return TICKETS.get(customer_id)


def sla_remaining_hours(ticket: dict) -> int:
    return ticket["sla_hours"] - ticket["opened_hours_ago"]
