"""
Singh Ji AI — Agentic AI v10 | main.py
FastAPI Production Server — Render-ready
"""

import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.orchestrator import SinghJiOrchestrator
from core.scheduler import AgenticScheduler

orchestrator: Optional[SinghJiOrchestrator] = None
scheduler: Optional[AgenticScheduler] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator, scheduler
    print("🚀 Singh Ji Agentic AI v10 starting...")
    orchestrator = SinghJiOrchestrator()
    scheduler = AgenticScheduler(orchestrator=orchestrator)
    await scheduler.start()
    print("✅ Orchestrator + Scheduler ready")
    yield
    if scheduler:
        await scheduler.stop()
    print("🛑 Shutting down...")

app = FastAPI(
    title="Singh Ji AI — Agentic AI v10",
    description="AI-powered business automation with multi-agent orchestration",
    version="10.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoalRequest(BaseModel):
    goal: str = Field(..., min_length=5, max_length=500, description="Business goal to achieve")

@app.get("/")
async def root():
    return {
        "name": "Singh Ji AI — Agentic AI v10",
        "version": "10.0.0",
        "status": "live",
        "endpoints": ["/ping", "/health", "/agents", "/execute"]
    }

@app.get("/ping")
async def ping():
    return {"status": "ok", "service": "singhji-agentic-ai"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "agents": list(orchestrator.agents.keys()) if orchestrator else []
    }

@app.get("/agents")
async def get_agents():
    agents = list(orchestrator.agents.keys()) if orchestrator else []
    return {"agents": agents, "count": len(agents)}

@app.post("/execute")
async def execute_goal(req: GoalRequest):
    """Goal दो, Orchestrator पूरा Plan बनाकर Execute करेगा"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not ready")
    try:
        result = await orchestrator.execute_goal(req.goal)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
