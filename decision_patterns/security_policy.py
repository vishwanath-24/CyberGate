"""
Reusable CyberGate Strands Decider policy pattern.

Decision:
Choose the security policy for an incoming request.

Question type:
choice

Options:
- ALLOW
- LAB_ONLY
- BLOCK
"""

SECURITY_POLICY_QUESTION = "What security policy should apply?"

SECURITY_POLICY_OPTIONS = {
    "ALLOW": "Request is safe and permitted.",
    "LAB_ONLY": "Request should only be handled in an authorized practice lab.",
    "BLOCK": "Request is unauthorized or unsafe and should be blocked.",
}


def build_security_policy_pattern(state: str) -> dict:
    """Build a reusable Strands Decider choice decision."""
    return {
        "state": state,
        "question": SECURITY_POLICY_QUESTION,
        "type": "choice",
        "criteria": SECURITY_POLICY_OPTIONS,
    }