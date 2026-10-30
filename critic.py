import os
from typing import Literal
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Change this to False once your API credits are ready
USE_MOCK = os.environ.get("USE_MOCK", "true").lower() == "true"

MODEL = "claude-sonnet-5-5"


# ---------- 1. Data shapes ----------
class Finding(BaseModel):
    severity: Literal["high", "medium", "low"]
    quote: str  # exact text from the PRD, or "(missing)"
    issue: str
    suggested_fix: str


class DimensionResult(BaseModel):
    dimension: str
    score: int  # 0-10
    findings: list[Finding]


# ---------- 2. The rubric ----------
RUBRIC = {
    "success_metrics": "Are success metrics measurable, with a baseline, target and timeframe?",
    "requirements_quality": "Is each requirement specific and testable? Flag vague words.",
    "edge_cases": "Which error states, empty states or failure modes are unaddressed?",
    "consistency": "Do any requirements, goals or metrics contradict each other?",
    "scope": "Are non-goals stated? Is anything ambiguous or too large?",
}

# How much each dimension counts toward the overall score
WEIGHTS = {
    "success_metrics": 3,
    "consistency": 3,
    "requirements_quality": 2,
    "edge_cases": 2,
    "scope": 1,
}

SYSTEM = """You are a skeptical senior product manager reviewing a PRD.
Rules:
- Only report issues you can ground in the text. Quote the exact passage, or write "(missing)" if the issue is an omission.
- Every finding needs a concrete suggested fix.
- If the PRD handles this dimension well, return few or no findings. Do not invent problems."""


# ---------- 3. Fake reviewer (no API needed) ----------
def mock_review_dimension(name: str) -> DimensionResult:
    fake = {
        "success_metrics": DimensionResult(
            dimension="success_metrics", score=1,
            findings=[Finding(
                severity="high", quote="Users love the feature.",
                issue="Not measurable: no baseline, target or timeframe.",
                suggested_fix="Increase 7-day repeat-order rate from 22% to 28% within 90 days of launch.")]),
        "requirements_quality": DimensionResult(
            dimension="requirements_quality", score=4,
            findings=[Finding(
                severity="medium", quote="fast and intuitive",
                issue="Vague terms that cannot be tested.",
                suggested_fix="Reorder reaches cart in 2 taps or fewer and under 3 seconds on 4G.")]),
        "edge_cases": DimensionResult(
            dimension="edge_cases", score=2,
            findings=[
                Finding(
                    severity="medium", quote="(missing)",
                    issue="No handling for out-of-stock items or closed restaurants.",
                    suggested_fix="Add a section describing behavior for each case."),
                # This quote is deliberately fake, to show the grounding check dropping it
                Finding(
                    severity="low", quote="Users can pay with cryptocurrency.",
                    issue="This quote does not exist in the PRD.",
                    suggested_fix="n/a")]),
        "consistency": DimensionResult(
            dimension="consistency", score=2,
            findings=[Finding(
                severity="high",
                quote="Reorder must always use the current menu prices.",
                issue="Contradicts requirement 4, which says to charge the original price.",
                suggested_fix="Pick one rule and show a price-change notice before checkout.")]),
        "scope": DimensionResult(
            dimension="scope", score=5,
            findings=[Finding(
                severity="low", quote="(missing)",
                issue="No non-goals listed.",
                suggested_fix="Add an 'Out of scope' list.")]),
    }
    return fake[name]


# ---------- 4. Real reviewer (uses the API) ----------
def real_review_dimension(prd: str, name: str, instruction: str) -> DimensionResult:
    from anthropic import Anthropic
    client = Anthropic()
    tool = {
        "name": "report",
        "description": "Report review findings for one dimension.",
        "input_schema": DimensionResult.model_json_schema(),
    }
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        system=SYSTEM,
        tools=[tool],
        tool_choice={"type": "tool", "name": "report"},
        messages=[{
            "role": "user",
            "content": f"Dimension: {name}\nCriteria: {instruction}\n\nPRD:\n{prd}",
        }],
    )
    block = next(b for b in resp.content if b.type == "tool_use")
    return DimensionResult(**block.input)


def review_dimension(prd: str, name: str, instruction: str) -> DimensionResult:
    if USE_MOCK:
        return mock_review_dimension(name)
    return real_review_dimension(prd, name, instruction)


# ---------- 5. Grounding check ----------
def ground_findings(prd: str, result: DimensionResult) -> DimensionResult:
    """Keep only findings whose quote really appears in the PRD."""
    kept = []
    for f in result.findings:
        if f.quote == "(missing)" or f.quote.lower() in prd.lower():
            kept.append(f)
        else:
            print(f"  [dropped made-up quote: {f.quote!r}]")
    result.findings = kept
    return result


# ---------- 6. Scoring ----------
def overall_score(results: list[DimensionResult]) -> int:
    total = sum(WEIGHTS[r.dimension] * r.score for r in results)
    max_total = sum(WEIGHTS[r.dimension] * 10 for r in results)
    return round(100 * total / max_total)


# ---------- 7. Put it all together ----------
def review_prd(prd: str) -> list[DimensionResult]:
    results = []
    for name, instruction in RUBRIC.items():
        r = review_dimension(prd, name, instruction)
        results.append(ground_findings(prd, r))
    return results


if __name__ == "__main__":
    prd = open("sample_prd.txt", encoding="utf-8").read()
    print("MODE:", "MOCK" if USE_MOCK else "REAL API")
    results = review_prd(prd)

    print(f"\nOVERALL SCORE: {overall_score(results)}/100\n")
    for r in results:
        print(f"== {r.dimension} (score {r.score}/10)")
        for f in r.findings:
            print(f"  [{f.severity.upper()}] \"{f.quote}\"")
            print(f"     Issue: {f.issue}")
            print(f"     Fix:   {f.suggested_fix}")
        print()