import json
import os
import urllib.request


DECIDER_ENDPOINT = "https://da25tnxy06gjk.cloudfront.net/v1/decide"


def ask_decider(state: str) -> dict:
    api_key = os.environ["DECIDER_API_KEY"]

    payload = {
        "state": state,
        "model": "StrandsAgents/strands-decider-2B-qwen3.5-v1-2610",
        "questions": {
            "security_policy": {
                "type": "choice",
                "instructions": "What security policy should apply?",
                "criteria": {
                    "ALLOW": "Request is safe and permitted.",
                    "LAB_ONLY": "Request should only be allowed in an authorized lab.",
                    "BLOCK": "Request should be blocked.",
                },
            }
        },
    }

    request = urllib.request.Request(
        DECIDER_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))