from dataclasses import dataclass
import ast
import operator


@dataclass
class ToolResult:
    tool: str
    success: bool
    result: str


def word_count(text: str) -> ToolResult:
    words = text.split()

    return ToolResult(
        tool="word_count",
        success=True,
        result=f"Word count: {len(words)}",
    )


def uppercase(text: str) -> ToolResult:
    return ToolResult(
        tool="uppercase",
        success=True,
        result=text.upper(),
    )


def calculator(expression: str) -> ToolResult:
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
    }

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant) and isinstance(
                node.value, (int, float)
            ):
                return node.value

            if isinstance(node, ast.BinOp):
                operation = allowed_operators.get(type(node.op))

                if operation is None:
                    raise ValueError("Operator not allowed.")

                return operation(
                    evaluate(node.left),
                    evaluate(node.right),
                )

            raise ValueError("Expression not allowed.")

        result = evaluate(tree)

        return ToolResult(
            tool="calculator",
            success=True,
            result=f"Calculation result: {result}",
        )

    except Exception:
        return ToolResult(
            tool="calculator",
            success=False,
            result="Invalid or unsupported calculation.",
        )


SAFE_TOOLS = {
    "word_count": word_count,
    "uppercase": uppercase,
    "calculator": calculator,
}