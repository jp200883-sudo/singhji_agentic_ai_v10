"""
Singh Ji AI — Agentic AI v10 | main.py
FastAPI Production Server — Render-ready
"""

import os
import asyncio
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import our modules
from tools_production import get_health as tools_health
from agents_production import list_agents
from orchestrator_production import get_orchestrator

# ── Startup / Shutdown ──

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan events."""
    print("🚀 Singh Ji Agentic AI v10 starting...")
    # Warm up orchestrator
    orch = get_orchestrator()
    print(f"✅ Orchestrator ready: {orch.get_status()}")
    yield
    print("🛑 Shutting down...")

# ── FastAPI App ──

app = FastAPI(
    title="Singh Ji AI — Agentic AI v10",
    description="AI-powered business automation with multi-agent orchestration",
    version="10.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request Models ──

class AutoSellRequest(BaseModel):
    product: str = Field(..., min_length=2, max_length=200, description="Product or service to sell")
    industry: str = Field(..., min_length=2, max_length=100, description="Target industry (e.g., FMCG, Real Estate)")
    location: str = Field(default="India", max_length=100, description="Geographic target")
    num_leads: int = Field(default=5, ge=1, le=20, description="Number of leads to find")
    channel: str = Field(default="email", pattern="^(email|whatsapp|sms)$")

class PlanRequest(BaseModel):
    goal: str = Field(..., min_length=5, max_length=500, description="Business goal to achieve")
    context: Optional[dict] = Field(default=None, description="Additional context")

class AgentTaskRequest(BaseModel):
    agent_type: str = Field(..., description="Type of agent to use")
    task: str = Field(..., min_length=5, max_length=500, description="Task description")

# ── Health & Info ──

@app.get("/")
async def root():
    return {
        "name": "Singh Ji AI — Agentic AI v10",
        "version": "10.0.0",
        "status": "live",
        "endpoints": [
            "/ping",
            "/health",
            "/agents",
            "/auto_sell",
            "/plan",
            "/execute"
        ]
    }

@app.get("/ping")
async def ping():
    """Render healthcheck endpoint."""
    return {"status": "ok", "service": "singhji-agentic-ai"}

@app.get("/health")
async def health():
    """Full health check with tool status."""
    return {
        "status": "healthy",
        "tools": tools_health(),
        "agents": list_agents(),
        "orchestrator": get_orchestrator().get_status()
    }

# ── Agent Endpoints ──

@app.get("/agents")
async def get_agents():
    """List all available agents."""
    return {
        "agents": list_agents(),
        "count": len(list_agents())
    }

@app.post("/plan")
async def create_plan(req: PlanRequest):
    """AI-powered task planning."""
    try:
        orch = get_orchestrator()
        plan = await orch.plan(req.goal, req.context)
        return plan.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute")
async def execute_plan(req: PlanRequest):
    """Plan + Execute in one call."""
    try:
        orch = get_orchestrator()
        plan = await orch.plan(req.goal, req.context)
        executed = await orch.execute(plan)
        return executed.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Core Business Endpoints ──

@app.post("/auto_sell")
async def auto_sell(req: AutoSellRequest):
    """
    Complete auto-sell pipeline:
    1. Find leads in industry/location
    2. Qualify leads with AI
    3. Generate personalized outreach
    4. Return ready-to-send campaign
    """
    try:
        orch = get_orchestrator()
        result = await orch.auto_sell(
            product=req.product,
            industry=req.industry,
            location=req.location,
            num_leads=req.num_leads
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto-sell failed: {str(e)}")

@app.post("/find_leads")
async def find_leads(industry: str, location: str = "India", num: int = 10):
    """Find business leads only."""
    from agents_production import get_agent
    try:
        hunter = get_agent("lead_hunter")
        leads = await hunter.find_leads(industry, location, num_results=num)
        return {"industry": industry, "location": location, "leads": leads, "count": len(leads)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/draft_outreach")
async def draft_outreach(company: str, product: str, channel: str = "email"):
    """Draft outreach message only."""
    from tools_production import draft_email, draft_whatsapp_message
    try:
        if channel == "email":
            msg = await draft_email("Business Owner", company, product)
        else:
            msg = await draft_whatsapp_message(company, product)
        return {"channel": channel, "company": company, "message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/competitor_analysis")
async def competitor_analysis(company: str, industry: str):
    """Competitor intelligence."""
    from agents_production import get_agent
    try:
        analyst = get_agent("competitor")
        result = await analyst.full_analysis(company, industry)
        return {"company": company, "industry": industry, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_ad")
async def create_ad(product: str, platform: str = "instagram", tone: str = "fun"):
    """Generate ad content."""
    from agents_production import get_agent
    try:
        content_agent = get_agent("content")
        result = await content_agent.create_ad(product, platform, tone)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Entry Point ──

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
