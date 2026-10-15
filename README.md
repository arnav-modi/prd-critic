# PRD Critic

An AI tool that reviews product requirement documents (PRDs) like a skeptical senior PM.

## How it works
1. Paste a PRD
2. The critic checks 5 dimensions: success metrics, requirements quality, edge cases, consistency, scope
3. Every finding quotes the exact passage and suggests a fix
4. A grounding check removes any finding whose quote isn't in the PRD
5. A weighted score summarizes the result

## Run locally
pip install anthropic fastapi uvicorn pydantic python-dotenv
uvicorn main:app --reload

Set ANTHROPIC_API_KEY in a .env file to use the real reviewer.

## Status
Work in progress. Evaluation set and deployment coming next.
