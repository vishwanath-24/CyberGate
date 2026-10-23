# CyberGate

## AI Security Gateway with Strands Decider

CyberGate is an AI security gateway that makes a security-policy decision **before** an AI response is generated.

It uses **Strands Decider 2B** to classify an incoming request into one of three policies:

- **ALLOW** — the request is safe and permitted.
- **LAB_ONLY** — the request should only be handled in an authorized practice lab.
- **BLOCK** — the request should be blocked.

The selected policy is then passed to the response layer powered by **Amazon Bedrock**.

## Architecture

```text
User Request
     │
     ▼
Strands Decider 2B
     │
     │ Security Policy Decision
     ▼
ALLOW / LAB_ONLY / BLOCK
     │
     ▼
CyberGate Policy Enforcement
     │
     ▼
Amazon Bedrock
     │
     ▼
Safe Response
```
![CyberGate Architecture](docs/architecture.png)
## Why Strands Decider?

A general-purpose LLM is not always the best component for every decision.

CyberGate uses Strands Decider for the small, structured decision:

> "What security policy should apply?"

The Decider returns a selected option together with probabilities and confidence. CyberGate can then use that decision to control the response path.

This separates **decision-making** from **response generation**.

## Reusable Decision Pattern

CyberGate includes a reusable Strands Decider `choice` pattern in:

```text
decision_patterns/security_policy.py
```

### Decision

**Question:**  
What security policy should apply?

### Options

| Option | Meaning |
|---|---|
| ALLOW | Request is safe and permitted. |
| LAB_ONLY | Request belongs in an authorized practice lab. |
| BLOCK | Request should be blocked. |

This pattern can be adapted to other AI security gateways and policy-enforcement systems.

## Example Scenarios

### Safe request

```text
Explain how a firewall protects a web server.
```

CyberGate can classify the request as:

```text
ALLOW
```

### Authorized lab request

```text
I want to learn cybersecurity in an authorized practice lab.
```

CyberGate can classify the request as:

```text
LAB_ONLY
```

### Unsafe request

Requests that could enable unauthorized access are handled conservatively by the gateway and response layer.

## Technology

- Python
- Strands Decider 2B
- Amazon Bedrock
- boto3
- Strands ecosystem

## Project Structure

```text
CyberGate/
├── app/
│   ├── bedrock_client.py
│   ├── decider_client.py
│   ├── decisions.py
│   ├── gateway.py
│   └── policy.py
│
├── decision_patterns/
│   └── security_policy.py
│
├── docs/
│
├── examples/
│
├── .gitignore
└── README.md
```

## Security

Do not commit API keys, AWS credentials, or other secrets to the repository.

Use environment variables for credentials.

## Purpose

CyberGate is designed as a defensive AI-security project for demonstrating policy-based control of AI agent behavior.