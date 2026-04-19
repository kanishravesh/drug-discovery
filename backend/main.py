from fastapi import FastAPI, HTTPException,Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from pydantic import BaseModel
from typing import Dict, Any
from app.orchestrator import graph
from sqlalchemy.orm import Session
from .app import models, database
app = FastAPI(
    title=" Drug Discovery ",
    description="Multi-agent system powered by Gemini 2.5 and LangGraph",
    version="1.0.0"
)
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define the Request/Response Models
class ResearchRequest(BaseModel):
    drug_name: str

class ResearchResponse(BaseModel):
    drug: str
    dossier: List[str]
    
class ImpactMetrics(BaseModel):
    time_manual: str
    time_ai: str
    time_impact: str
    cost_manual: str
    cost_ai: str
    cost_impact: str
    hours_manual: str
    hours_ai: str
    hours_impact: str

class ResearchResponse(BaseModel):
    drug: str
    impact_score: int
    verdict: str
    metrics: ImpactMetrics  # This data will populate the table 
    full_dossier: List[str]    

# 3. API Endpoints
@app.get("/")
def read_root():
    return {"status": "Online", "engine": "Gemini 2.5 Flash", "agents": ["Medical", "Patent", "Scorer"]}

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """
    Triggers the full multi-agent research pipeline for a given drug.
    """
    try:

        initial_state = {
            "drug_name": request.drug_name,
            "research_notes": []
        }
        

        final_state = await graph.ainvoke(initial_state)
        
        return {
            "drug": request.drug_name,
            "dossier": final_state["research_notes"]
        }
        
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
    
@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    try:
        initial_state = {"drug_name": request.drug_name, "research_notes": []}
        final_state = await graph.ainvoke(initial_state)
        
        # LOGIC TO EXTRACT THE JSON FROM THE SCORER'S TEXT
        last_note = final_state["research_notes"][-1]
        import json
        import re
        
        # Find JSON block using regex
        json_match = re.search(r'```json\n(.*?)\n```', last_note, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(1))
            return {
                "drug": request.drug_name,
                "impact_score": data["impact_score"],
                "verdict": data["verdict"],
                "metrics": data["metrics"],
                "full_dossier": final_state["research_notes"]
            }
        
        raise Exception("Could not parse metrics from Scorer")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
    
@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(email: str, password: str, db: Session = Depends(database.get_db)):
    # Password hashing and user creation logic here
    new_user = models.User(email=email, hashed_password=password) # simplified
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}