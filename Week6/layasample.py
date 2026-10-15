"""
laya_demo.py

Sample script for Laya (https://github.com/NandhaKishorM/laya) — a
non-autoregressive "System 1" decision engine. Instead of generating text,
Laya classifies a state (a dict of facts) against typed questions and
returns calibrated probabilities in a single forward pass (~33ms).

Install first:
    pip install laya

This demo covers a realistic support-ticket triage flow using all three
decision primitives Laya supports:
    - "choice" -> pick one option from a fixed set
    - "score"  -> place the input on an ordered scale
    - "noul"   -> a yes/no probability
"""

import json

import laya
from laya import Router


def build_ticket_state() -> dict:
    """A support ticket, represented as plain data (no prose generation needed)."""
    return {
        "from": "user@acme.com",
        "subject": "Duplicate charge on invoice #4411",
        "body": (
            "Hi, we were billed twice for March. Please refund the extra "
            "charge as soon as possible, this is affecting our accounting."
        ),
    }


def build_questions() -> dict:
    """Typed questions Laya will answer against the ticket state above."""
    return {
        "department": {
            "type": "choice",
            "instructions": "Which department should handle this ticket?",
            "criteria": {
                "billing": "invoices, payments, refunds, duplicate charges",
                "technical": "bugs, outages, system errors",
                "sales": "pricing, new contracts, upgrades",
                "other": "everything else",
            },
        },
        "urgency": {
            "type": "score",
            "instructions": "How urgent is this request?",
            "criteria": ["not urgent", "soon", "critical deadline or blocking issue"],
        },
        "needs_refund": {
            "type": "noul",
            "instructions": "Does the customer appear to be requesting a refund?",
        },
    }


def run_with_router(state: dict, questions: dict) -> dict:
    """Preferred path: let Laya's Router pick the best checkpoint for the input
    (e.g. language/script detection) and preload it for low-latency calls."""
    router = Router(preload=True)
    return router.predict(state, questions)


def run_with_direct_model(state: dict, questions: dict) -> dict:
    """Alternative path: load one specific checkpoint directly, useful when you
    know your workload is single-language/domain and want to skip routing."""
    agent = laya.load("convaiinnovations/laya")
    return agent.predict(state, questions)


def summarize(result: dict) -> None:
    answers = result["answers"]

    department = answers["department"]
    print(f"Department  : {department['choice']} (confidence {department['confidence']:.2f})")

    urgency = answers["urgency"]
    print(f"Urgency     : {urgency['score']}")

    refund = answers["needs_refund"]
    print(f"Needs refund: {refund['probability']:.2f}")

    # Simple automation-vs-escalation gate based on calibrated confidence.
    if department["confidence"] >= 0.85:
        print("-> Auto-routing ticket, no human review needed.")
    else:
        print("-> Confidence too low, escalating to a human for triage.")


def main() -> None:
    state = build_ticket_state()
    questions = build_questions()

    print("=== Router-based prediction (recommended) ===")
    result = run_with_router(state, questions)
    print(json.dumps(result, indent=2))
    summarize(result)

    print("\n=== Direct model prediction ===")
    result_direct = run_with_direct_model(state, questions)
    summarize(result_direct)


if __name__ == "__main__":
    main()