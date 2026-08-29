import streamlit as st
from state_layer import CUSTOMERS, get_order_state, get_refund_state, get_ticket_state
from engine import classify, generic_response, point_response, USE_CASES

st.set_page_config(page_title="Point-Response Demo", page_icon="🎯", layout="wide")

st.title("🎯 Point-Response Layer — Concept Demo")
st.caption(
    "Try it as a customer would: pick a use case below, or type your own "
    "question. Same underlying policy, two different answers — one from a "
    "generic policy lookup, one from a live, unified state layer."
)

with st.sidebar:
    st.header("👤 Simulated caller")
    customer_id = st.selectbox(
        "Customer (mock CRM record)",
        options=list(CUSTOMERS.keys()),
        format_func=lambda cid: f"{CUSTOMERS[cid]['name']} — {CUSTOMERS[cid]['plan']} plan",
    )
    st.markdown("---")
    st.markdown("**Use cases in this demo**")
    st.markdown(
        "- 📦 Order status\n"
        "- 💸 Refund status\n"
        "- 🎫 Support ticket status\n\n"
        "Every customer above has a live mock record for all three — "
        "switch customers to see the answer change with the actual state."
    )
    st.markdown("---")
    st.markdown(
        "**What this demo shows**\n\n"
        "This is a concept demo, not a production NLU system. The classifier "
        "is deliberately simple — the point is to make *state-awareness* "
        "visible, not to showcase language understanding.\n\n"
        "Real state (order/refund/ticket data) is mocked here to stand in "
        "for a client's CRM, order-management system, payments backend, and "
        "ticketing system."
    )

st.subheader("1. Ask a question — as a customer would")

use_case = st.radio(
    "Pick a use case to try:",
    options=list(USE_CASES.keys()),
    format_func=lambda k: USE_CASES[k]["label"],
    horizontal=True,
)

col_a, col_b = st.columns([3, 1])
with col_a:
    query = st.text_input(
        "Your question:",
        value=USE_CASES[use_case]["example"],
        key=f"query_{use_case}",
    )
with col_b:
    st.write("")
    st.write("")
    ask = st.button("Ask →", use_container_width=True, type="primary")

if query:
    category = classify(query)

    st.subheader("2. Two ways to answer the same question")
    col_generic, col_point = st.columns(2)

    with col_generic:
        st.markdown("#### ❌ Generic policy-lookup response")
        st.markdown(
            f"<div style='background:#FBE4E4;padding:16px;border-radius:8px;"
            f"min-height:130px'>{generic_response(category)}</div>",
            unsafe_allow_html=True,
        )
        st.caption("What it required: a static policy document. No customer- or case-specific data.")

    with col_point:
        st.markdown("#### ✅ Point response (state-aware)")
        text, state = point_response(category, customer_id)
        st.markdown(
            f"<div style='background:#E2EFDA;padding:16px;border-radius:8px;"
            f"min-height:130px'>{text}</div>",
            unsafe_allow_html=True,
        )
        st.caption("What it required: a live read from the unified state layer below.")

    if state:
        st.subheader("3. The state layer behind the point response")
        st.json(
            {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in state.items()}
        )
        st.caption(
            "In production, this record is assembled live from the client's own "
            "CRM, order-management system, ticketing system, and payments/ops "
            "backend — the point-response layer sits over them, it doesn't "
            "replace them."
        )
    elif category == "unknown":
        st.info(
            "This demo only has mocked state for order, refund, and ticket "
            "status queries — try rephrasing, or pick one of the use cases above."
        )
else:
    st.info("Enter a question above (or use one of the example use cases) to see both responses.")

st.markdown("---")
with st.expander("🔍 See all mock data for the selected customer"):
    st.markdown("This is the full simulated state layer for the customer selected in the sidebar.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**📦 Order**")
        st.json(get_order_state(customer_id) or {}, expanded=False)
    with c2:
        st.markdown("**💸 Refund**")
        st.json(get_refund_state(customer_id) or {}, expanded=False)
    with c3:
        st.markdown("**🎫 Ticket**")
        st.json(get_ticket_state(customer_id) or {}, expanded=False)

st.markdown("---")
st.caption(
    "Built to accompany the product strategy document: *From AI Chatbot to "
    "Customer Operations Platform.* This demo intentionally does not call an "
    "external LLM API — it's a deterministic illustration of the state-layer "
    "concept, kept dependency-free so it's easy to run and deploy."
)
