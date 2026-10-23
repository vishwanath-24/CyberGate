def enforce_policy(policy: str) -> str:
    if policy == "ALLOW":
        return "Request permitted."

    if policy == "LAB_ONLY":
        return "Request restricted to an authorized lab environment."

    if policy == "BLOCK":
        return "Request blocked."

    if policy == "SAFETY_REVIEW":
        return "Request requires additional safety review."

    return "Unknown policy. Request blocked for safety."