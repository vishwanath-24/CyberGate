from app.decider_client import ask_decider
from app.policy import enforce_policy
from app.tools import SAFE_TOOLS


def create_plan(goal: str) -> list[dict]:
    goal = goal.strip()

    if not goal:
        return []

    return [
        {
            "step": 1,
            "action": "Understand the user's goal",
            "purpose": goal,
        },
        {
            "step": 2,
            "action": "Determine the required next action",
            "purpose": "Prepare the task for security evaluation.",
        },
        {
            "step": 3,
            "action": "Evaluate the planned action",
            "purpose": "Apply CyberGate security policy before execution.",
        },
        {
            "step": 4,
            "action": "Execute a permitted safe tool",
            "purpose": "Perform the approved action.",
        },
    ]


def choose_tool(goal: str) -> str:
    goal_lower = goal.lower()

    if "count" in goal_lower and "word" in goal_lower:
        return "word_count"

    if "uppercase" in goal_lower or "upper case" in goal_lower:
        return "uppercase"

    if any(symbol in goal for symbol in ["+", "-", "*", "/", "%"]):
        return "calculator"

    return "none"


def extract_calculation(goal: str) -> str:
    """
    Extract a simple arithmetic expression from the goal.
    """
    allowed = set("0123456789+-*/%.() ")

    expression = "".join(
        character for character in goal
        if character in allowed
    ).strip()

    return expression


def execute_tool(tool_name: str, goal: str) -> str:
    if tool_name == "none":
        return "No safe tool matched this request."

    tool = SAFE_TOOLS[tool_name]

    if tool_name == "word_count":
        result = tool(goal)

    elif tool_name == "uppercase":
        result = tool(goal)

    elif tool_name == "calculator":
        expression = extract_calculation(goal)

        if not expression:
            return "No valid calculation found."

        result = tool(expression)

    else:
        return "Unknown tool. Execution blocked."

    return result.result


def evaluate_agent_goal(goal: str) -> dict:
    plan = create_plan(goal)

    decision = ask_decider(goal)
    security = decision["answers"]["security_policy"]

    original_policy = security["choice"]
    confidence = security["confidence"]

    policy = original_policy

    if confidence < 0.20:
        policy = "SAFETY_REVIEW"

    action = enforce_policy(policy)

    if policy == "ALLOW":
        status = "CONTINUE"
        tool_name = choose_tool(goal)
        tool_result = execute_tool(tool_name, goal)
        next_action = "Safe tool execution completed."

    elif policy == "LAB_ONLY":
        status = "RESTRICT"
        tool_name = "none"
        tool_result = (
            "Tool execution requires an authorized lab environment."
        )
        next_action = (
            "Require an authorized lab environment before continuing."
        )

    elif policy == "BLOCK":
        status = "STOP"
        tool_name = "none"
        tool_result = "Tool execution blocked."
        next_action = "Stop the agent and do not execute the request."

    elif policy == "SAFETY_REVIEW":
        status = "REVIEW"
        tool_name = "none"
        tool_result = "Tool execution paused for safety review."
        next_action = "Pause and require additional safety review."

    else:
        status = "STOP"
        tool_name = "none"
        tool_result = "Unknown policy. Tool execution blocked."
        next_action = "Stop because the policy is unknown."

    return {
        "goal": goal,
        "plan": plan,
        "original_policy": original_policy,
        "policy": policy,
        "confidence": confidence,
        "action": action,
        "status": status,
        "next_action": next_action,
        "tool": tool_name,
        "tool_result": tool_result,
    }


if __name__ == "__main__":
    goal = input("Enter an agent goal: ")

    result = evaluate_agent_goal(goal)

    print("\nCyberGate Agent")
    print("----------------")

    print(f"Goal: {result['goal']}")

    print("\nPlan:")
    for item in result["plan"]:
        print(f"{item['step']}. {item['action']}")
        print(f"   {item['purpose']}")

    print("\nSecurity Decision")
    print("-----------------")
    print(f"Original Policy: {result['original_policy']}")
    print(f"Final Policy: {result['policy']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Action: {result['action']}")

    print("\nAgent Control")
    print("-------------")
    print(f"Status: {result['status']}")
    print(f"Next Action: {result['next_action']}")

    print("\nTool Execution")
    print("--------------")
    print(f"Tool: {result['tool']}")
    print(f"Result: {result['tool_result']}")