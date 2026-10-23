# CyberGate Security Policy Decision Pattern

## Decision

Choose the security policy for an incoming user request before generating an AI response.

## Question Type

`choice`

## Question

> What security policy should apply?

## Options

| Option | Meaning | Application behavior |
|---|---|---|
| `ALLOW` | Request is safe and permitted. | Send the request to Amazon Bedrock for a response. |
| `LAB_ONLY` | Request should only be handled in an authorized practice lab. | Send the request to Bedrock with the lab-only policy. |
| `BLOCK` | Request is unauthorized or unsafe. | Block the request before calling Bedrock. |

## Wiring

```text
User Request
     |
     v
Strands Decider 2B
     |
     +---- ALLOW ------> Amazon Bedrock
     |
     +---- LAB_ONLY ---> Amazon Bedrock
     |
     +---- BLOCK ------> Stop