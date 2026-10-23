import boto3


BEDROCK_REGION = "ap-southeast-2"
BEDROCK_MODEL = "amazon.nova-micro-v1:0"


def ask_bedrock(user_request: str, policy: str) -> str:
    client = boto3.client(
        "bedrock-runtime",
        region_name=BEDROCK_REGION,
    )

    prompt = f"""
You are the response layer of CyberGate, an AI security gateway.

User request:
{user_request}

CyberGate security policy:
{policy}

Respond helpfully while respecting the security policy.
If the policy is BLOCK, do not provide instructions that enable the request.
If the policy is LAB_ONLY, explain that the activity belongs in an authorized lab environment.
"""

    response = client.converse(
        modelId=BEDROCK_MODEL,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        inferenceConfig={
            "maxTokens": 300,
            "temperature": 0.2,
        },
    )

    return response["output"]["message"]["content"][0]["text"]