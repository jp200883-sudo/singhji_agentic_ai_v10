#!/usr/bin/env python3
"""
🦁 Singh Ji Agentic AI v10.0
Fully Autonomous AI System — Render/Railway Deploy Ready
"""

import os
import asyncio
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# Core imports
from core.orchestrator import SinghJiOrchestrator
from core.scheduler import AgenticScheduler
from core.memory import SupabaseMemory
from modules.keep_alive import KeepAliveManager
from modules.instagram_agent import InstagramAgent

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("SinghJiAgentic")

# Global instances
orchestrator = None
scheduler = None
memory = None
keep_alive = None
instagram = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & Shutdown lifecycle"""
    global orchestrator, scheduler, memory, keep_alive, instagram

    logger.info("🦁 Singh Ji Agentic AI v10.0 Starting...")

    # Initialize Memory
    memory = SupabaseMemory()
    await memory.init()

    # Initialize Orchestrator
    orchestrator = SinghJiOrchestrator(memory=memory)

    # Initialize Instagram Agent
    instagram = InstagramAgent(memory=memory)

    # Initialize Scheduler
    scheduler = AgenticScheduler(orchestrator=orchestrator, instagram=instagram)
    await scheduler.start()

    # Initialize Keep-Alive (prevents Render sleep)
    keep_alive = KeepAliveManager()
    keep_alive.start()

    logger.info("✅ All Systems Ready — Agentic AI is LIVE!")
    yield

    # Shutdown
    logger.info("🛑 Shutting down Agentic AI...")
    if scheduler:
        await scheduler.stop()
    if keep_alive:
        keep_alive.stop()
    logger.info("👋 Goodbye!")

app = FastAPI(
    title="Singh Ji Agentic AI v10.0",
    description="Fully Autonomous Multi-Agent AI System",
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

# ============================================
# HEALTH & STATUS ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "name": "Singh Ji Agentic AI v10.0",
        "status": "🦁 LIVE",
        "timestamp": datetime.now().isoformat(),
        "version": "10.0.0",
        "agents": 300,
        "mode": "AUTONOMOUS"
    }

@app.get("/ping")
async def ping():
    """Render/Railway Health Check"""
    return {"status": "ok", "time": datetime.now().isoformat()}

@app.get("/status")
async def system_status():
    """Full System Status"""
    return {
        "orchestrator": orchestrator is not None,
        "scheduler": scheduler is not None if scheduler else False,
        "memory": memory is not None if memory else False,
        "keep_alive": keep_alive.is_running() if keep_alive else False,
        "instagram": instagram is not None,
        "agents_active": 300,
        "mode": "AUTONOMOUS",
        "timestamp": datetime.now().isoformat()
    }

# ============================================
# AGENTIC AI ENDPOINTS
# ============================================

@app.post("/agent/execute")
async def execute_goal(goal: str, background_tasks: BackgroundTasks):
    """Execute any goal autonomously"""
    if not orchestrator:
        return {"error": "Orchestrator not ready"}

    background_tasks.add_task(orchestrator.execute_goal, goal)
    return {
        "status": "accepted",
        "goal": goal,
        "message": "🤖 Agent is working on it... Check /status for progress"
    }

@app.post("/agent/auto-sell")
async def auto_sell(
    business_type: str,
    city: str,
    count: int = 10,
    background_tasks: BackgroundTasks = None
):
    """Auto Client Acquisition"""
    goal = f"Find {count} {business_type} in {city} without websites, send personalized WhatsApp outreach, follow up in 2 days, convert to leads"

    if background_tasks:
        background_tasks.add_task(orchestrator.execute_goal, goal)

    return {
        "status": "🚀 Auto-Sell Activated",
        "target": f"{count} {business_type} in {city}",
        "goal": goal,
        "steps": [
            "1. Research Agent → Find businesses via Google Maps",
            "2. Analysis Agent → Filter those without websites",
            "3. Sales Agent → Send personalized WhatsApp messages",
            "4. Scheduler → Auto follow-up after 2 days",
            "5. Memory → Save all leads to database"
        ]
    }

# ============================================
# INSTAGRAM AUTOMATION ENDPOINTS
# ============================================

@app.post("/instagram/auto-post")
async def instagram_auto_post(
    topic: str = "daily",
    background_tasks: BackgroundTasks = None
):
    """Auto-generate and post to Instagram"""
    if not instagram:
        return {"error": "Instagram Agent not ready"}

    if background_tasks:
        background_tasks.add_task(instagram.create_and_post, topic)

    return {
        "status": "📸 Instagram Auto-Post Scheduled",
        "topic": topic,
        "message": "AI will generate image + caption and post automatically"
    }

@app.get("/instagram/status")
async def instagram_status():
    """Instagram Agent Status"""
    if not instagram:
        return {"error": "Not initialized"}
    return await instagram.get_status()

# ============================================
# MEMORY ENDPOINTS
# ============================================

@app.get("/memory/leads")
async def get_leads():
    """Get all saved leads"""
    if not memory:
        return {"error": "Memory not ready"}
    return await memory.get_leads()

@app.get("/memory/tasks")
async def get_tasks():
    """Get all task history"""
    if not memory:
        return {"error": "Memory not ready"}
    return await memory.get_tasks()

# ============================================
# TELEGRAM WEBHOOK (if needed)
# ============================================

@app.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    """Handle Telegram commands"""
    if not orchestrator:
        return {"error": "Not ready"}

    message = update.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text.startswith("/auto_sell"):
        parts = text.split()
        if len(parts) >= 4:
            business = parts[1]
            city = parts[2]
            count = int(parts[3]) if parts[3].isdigit() else 10
            goal = f"Find {count} {business} in {city} without websites, send personalized WhatsApp outreach, follow up in 2 days"
            asyncio.create_task(orchestrator.execute_goal(goal))
            return {"method": "sendMessage", "chat_id": chat_id, "text": f"🚀 Auto-Sell started for {count} {business} in {city}!"}

    elif text.startswith("/status"):
        return {"method": "sendMessage", "chat_id": chat_id, "text": "🦁 Singh Ji Agentic AI is LIVE! 300 Agents Active."}

    elif text.startswith("/instagram_post"):
        topic = text.replace("/instagram_post", "").strip() or "daily"
        if instagram:
            asyncio.create_task(instagram.create_and_post(topic))
        return {"method": "sendMessage", "chat_id": chat_id, "text": f"📸 Instagram post scheduled: {topic}"}

    return {"method": "sendMessage", "chat_id": chat_id, "text": "🦁 Singh Ji Agentic AI v10.0\nCommands: /auto_sell <business> <city> <count> | /status | /instagram_post <topic>"}

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
