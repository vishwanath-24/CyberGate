from decision_patterns.security_policy import build_security_policy_pattern


def build_security_decision(state: str) -> dict:
    """Build the reusable CyberGate security-policy decision."""
    return build_security_policy_pattern(state)