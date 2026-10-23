from app.decider_client import ask_decider
from app.policy import enforce_policy
from app.bedrock_client import ask_bedrock


def evaluate_request(user_request: str) -> dict:
    decision = ask_decider(user_request)

    security = decision["answers"]["security_policy"]

    original_policy = security["choice"]
    confidence = security["confidence"]
    probabilities = security["probabilities"]

    policy = original_policy

    # Very low-confidence decisions require additional safety review.
    if confidence < 0.20:
        policy = "SAFETY_REVIEW"

    action = enforce_policy(policy)

    # BLOCK is enforced before Bedrock.
    # Bedrock is not called for blocked requests.
    if policy == "BLOCK":
        response = (
            "CyberGate blocked this request because the Decider "
            "classified it as unauthorized or unsafe."
        )
    else:
        response = ask_bedrock(user_request, policy)

    return {
        "request": user_request,
        "original_policy": original_policy,
        "policy": policy,
        "confidence": confidence,
        "probabilities": probabilities,
        "latency_ms": decision.get("latency_ms"),
        "action": action,
        "response": response,
    }


if __name__ == "__main__":
    request = input("Enter a request: ")

    result = evaluate_request(request)

    print("\nCyberGate")
    print("---------")
    print(f"Request: {result['request']}")
    print(f"Decider Policy: {result['original_policy']}")
    print(f"Final Policy: {result['policy']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Probabilities: {result['probabilities']}")
    print(f"Decider Latency: {result['latency_ms']} ms")
    print(f"Action: {result['action']}")

    print("\nBedrock Response:")
    print(result["response"])