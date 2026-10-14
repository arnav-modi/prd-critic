from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from critic import review_prd, overall_score, USE_MOCK

BASE = Path(__file__).parent
app = FastAPI()


class PRDIn(BaseModel):
    text: str


@app.get("/")
def home():
    # Shows the web page
    return FileResponse(BASE / "index.html")


@app.get("/example")
def example():
    # Gives the page the sample PRD for the "Try an example" button
    return {"text": (BASE / "sample_prd.txt").read_text(encoding="utf-8")}


@app.post("/review")
def review(body: PRDIn):
    text = body.text.strip()
    if len(text) < 20:
        raise HTTPException(status_code=400, detail="Please paste a longer PRD.")
    if len(text) > 15000:
        raise HTTPException(status_code=400, detail="PRD too long (max 15,000 characters).")

    results = review_prd(text)
    return {
        "mode": "mock" if USE_MOCK else "real",
        "score": overall_score(results),
        "results": [r.model_dump() for r in results],
    }