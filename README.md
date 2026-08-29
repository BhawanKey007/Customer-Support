# Point-Response Layer — Concept Demo

A small, dependency-light Streamlit app built to accompany the product
strategy document *"From AI Chatbot to Customer Operations Platform."*

It's built to actually **use**, not just look at: pick a use case, pick a
customer, ask a question, and see two answers side by side —

- **Generic policy-lookup response** — what most support tools produce today
  (a policy paragraph, no case-specific detail).
- **Point response** — a single, precise sentence generated from a live,
  unified "state layer" that simulates pulling from a client's CRM, order
  system, ticketing system, and payments/ops backend.

## Use cases included

| Use case | Try asking... | What it pulls from |
|---|---|---|
| 📦 Order status | "Where is my order? Has it shipped yet?" | Mock order-management system (carrier, tracking number, stage, expected delivery) |
| 💸 Refund status | "What's the status of my refund?" | Mock payments/ops backend (refund stage, amount, expected completion) |
| 🎫 Support ticket status | "Any update on my support ticket?" | Mock ticketing system (severity, SLA clock, current stage, owner) |

All three mock customers (switchable in the sidebar) have full records for
all three use cases, so you can compare how the same question resolves
differently depending on whose data is behind it — including one
deliberately imperfect case (a delayed order, a near-SLA-breach ticket) so
the demo doesn't only show the happy path.

This is a **concept demo, not a production system**. There's no external
LLM call and no real integrations — `state_layer.py` mocks the kind of
data a real deployment would pull live from a client's own systems. The
point is to make the *state-awareness* difference visible and explainable
in a couple of minutes, which is what makes it useful for a Loom
walkthrough or for someone to click through on their own.

## Project structure

```
ops_layer_demo/
├── app.py            # Streamlit UI
├── engine.py         # query classification + generic vs. point response
├── state_layer.py    # mocked unified CRM / order / ticketing / payments state
├── requirements.txt
└── README.md
```

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Deploy it so others can use it externally

**Step 1 — push this folder to GitHub:**

```bash
git init
git add .
git commit -m "Point-response layer concept demo"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

**Step 2 — pick a free host and point it at the repo:**

- **Streamlit Community Cloud (recommended, ~2 minutes, made for this):**
  Go to [share.streamlit.io](https://share.streamlit.io), sign in with
  GitHub, click **New app**, select your repo, branch `main`, and file
  `app.py`. Deploy — you'll get a public `https://<something>.streamlit.app`
  URL you can share or drop into your assignment submission.

- **Hugging Face Spaces (alternative):** create a new Space, choose the
  **Streamlit** SDK, and either push this repo's contents to the Space's
  git remote or connect it to your GitHub repo. Free tier is sufficient
  for a demo like this.

- **Render.com (alternative, more general-purpose):** create a new **Web
  Service** from your GitHub repo, set the start command to
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`,
  and deploy. Useful if you outgrow Streamlit Cloud's free tier later.

Any of the three gives you a public URL — Streamlit Community Cloud is the
path of least resistance since no configuration beyond the repo itself is
needed.

## Extending the demo

The mocked data lives entirely in `state_layer.py` — add more customers,
orders, refunds, or tickets there to try different scenarios (e.g. a
cancelled order, a rejected refund, an escalated ticket). The
classification logic in `engine.py` is intentionally simple keyword
matching; swapping it for a real model or an actual CRM/order/ticketing
API call is the natural next step past this concept demo.
