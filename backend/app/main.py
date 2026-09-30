import json
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from app.services.parser import parse_unstructured_jd
from app.services.query_gen import build_boolean_queries
from app.services.scraper import fetch_search_results
from app.services.ranker import rank_candidates

app = FastAPI(title="RecruitAI Intelligence System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "RecruitAI Backend is running. Access API docs at /docs"}

@app.post("/ingest")
async def ingest_jd(raw_text: str = Form(...)):
    # 1. Parse JD using LLM
    structured_data = await parse_unstructured_jd(raw_text)
    
    # 2. Build platform queries
    queries = build_boolean_queries(structured_data)
    
    # 3. Fetch candidate matches from the web
    scraped_candidates = await fetch_search_results(queries["linkedin_dork"])
    
    # 4. Rank candidates using Vector AI
    ranked_candidates = rank_candidates(structured_data.model_dump(), scraped_candidates)
    
    response_payload = {
        "status": "success",
        "parsed_jd": structured_data.model_dump(),
        "generated_queries": queries,
        "ranked_candidates": ranked_candidates
    }

    # Save output to local JSON file
    with open("output_jd.json", "w") as f:
        json.dump(response_payload, f, indent=4)
    
    return response_payload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)