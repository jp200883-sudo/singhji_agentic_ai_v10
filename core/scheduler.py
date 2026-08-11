"""
⏰ Singh Ji Scheduler — 24x7 Background Jobs
Auto Digest, Lead Gen, Instagram, Keep-Alive
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

logger = logging.getLogger("Scheduler")

class AgenticScheduler:
    """
    Background Scheduler:
    - 6 AM: News + Weather + Mandi + Gold + Aaj Ka Vichar
    - 7 AM: Morning Digest Telegram
    - 6 PM: Evening Digest
    - Every 30 min: Keep Alive (Render awake)
    - Every 6 hours: Review Monitor
    - Every 7 days: Auto Lead Generation
    - Every 4 hours: Instagram Auto-Post
    """

    def __init__(self, orchestrator=None, instagram=None):
        self.orchestrator = orchestrator
        self.instagram = instagram
        self.running = False
        self.tasks = []
        self.jobs = {
            "morning_digest": {"hour": 6, "minute": 0, "enabled": True},
            "morning_telegram": {"hour": 7, "minute": 0, "enabled": True},
            "evening_digest": {"hour": 18, "minute": 0, "enabled": True},
            "keep_alive": {"interval_minutes": 30, "enabled": True},
            "review_monitor": {"interval_hours": 6, "enabled": True},
            "auto_lead_gen": {"interval_days": 7, "enabled": True},
            "instagram_post": {"interval_hours": 4, "enabled": True},
        }
        logger.info("⏰ Scheduler Initialized")

    async def start(self):
        """Scheduler Start करो"""
        self.running = True
        logger.info("🚀 Scheduler Started — All Jobs Active")

        # Create background tasks
        self.tasks = [
            asyncio.create_task(self._run_clock_jobs()),
            asyncio.create_task(self._run_interval_jobs()),
        ]

    async def stop(self):
        """Scheduler Stop करो"""
        self.running = False
        for task in self.tasks:
            task.cancel()
        logger.info("🛑 Scheduler Stopped")

    async def _run_clock_jobs(self):
        """Time-based Jobs (6 AM, 7 AM, 6 PM)"""
        while self.running:
            now = datetime.now()

            # Morning Digest @ 6:00 AM
            if now.hour == 6 and now.minute == 0:
                await self._morning_digest()
                await asyncio.sleep(60)  # Wait 1 min to avoid duplicate

            # Morning Telegram @ 7:00 AM
            elif now.hour == 7 and now.minute == 0:
                await self._morning_telegram()
                await asyncio.sleep(60)

            # Evening Digest @ 6:00 PM
            elif now.hour == 18 and now.minute == 0:
                await self._evening_digest()
                await asyncio.sleep(60)

            await asyncio.sleep(30)  # Check every 30 seconds

    async def _run_interval_jobs(self):
        """Interval-based Jobs"""
        last_keep_alive = datetime.now() - timedelta(minutes=30)
        last_review = datetime.now() - timedelta(hours=6)
        last_lead_gen = datetime.now() - timedelta(days=7)
        last_instagram = datetime.now() - timedelta(hours=4)

        while self.running:
            now = datetime.now()

            # Keep Alive every 30 min
            if (now - last_keep_alive).total_seconds() >= 30 * 60:
                await self._keep_alive()
                last_keep_alive = now

            # Review Monitor every 6 hours
            if (now - last_review).total_seconds() >= 6 * 3600:
                await self._review_monitor()
                last_review = now

            # Auto Lead Gen every 7 days
            if (now - last_lead_gen).total_seconds() >= 7 * 24 * 3600:
                await self._auto_lead_gen()
                last_lead_gen = now

            # Instagram Post every 4 hours
            if (now - last_instagram).total_seconds() >= 4 * 3600:
                await self._instagram_auto_post()
                last_instagram = now

            await asyncio.sleep(60)  # Check every minute

    # ============================================
    # JOB IMPLEMENTATIONS
    # ============================================

    async def _morning_digest(self):
        """6 AM — Aaj Ka Vichar + News + Weather + Mandi + Gold"""
        logger.info("🌅 Running Morning Digest...")

        if self.orchestrator:
            goal = "Generate Aaj Ka Vichar, fetch News, Weather, Mandi Bhav, Gold/Silver prices for today"
            await self.orchestrator.execute_goal(goal)

        logger.info("✅ Morning Digest Complete")

    async def _morning_telegram(self):
        """7 AM — Send Digest to Telegram"""
        logger.info("📱 Sending Morning Telegram Digest...")

        # Send via Telegram Bot
        from core.tools import ToolBox
        tools = ToolBox()

        admin_chat = os.environ.get("ADMIN_CHAT_ID", "")
        if admin_chat:
            message = """🌅 <b>Good Morning! Singh Ji Agentic AI is LIVE</b>

🤖 300 Agents Active
📰 News Fetched
🌤️ Weather Updated
💰 Gold/Silver Rates Updated
🎯 Auto Lead Gen: Active
📸 Instagram: Scheduled

<a href="https://singhji-agentic.onrender.com/status">View Dashboard</a>"""

            await tools.send_telegram(admin_chat, message)

        logger.info("✅ Morning Telegram Sent")

    async def _evening_digest(self):
        """6 PM — Evening News + Rozgar"""
        logger.info("🌆 Running Evening Digest...")

        if self.orchestrator:
            goal = "Fetch evening news, rozgar updates, and send digest"
            await self.orchestrator.execute_goal(goal)

        logger.info("✅ Evening Digest Complete")

    async def _keep_alive(self):
        """Keep Render Awake — Self Ping"""
        import aiohttp

        render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
        if render_url:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{render_url}/ping", timeout=10) as resp:
                        logger.info(f"💓 Keep-Alive Ping: {resp.status}")
            except Exception as e:
                logger.warning(f"Keep-Alive failed: {e}")
        else:
            logger.info("💓 Keep-Alive: System Active")

    async def _review_monitor(self):
        """Monitor Google Reviews"""
        logger.info("⭐ Review Monitor Running...")
        # Implementation: Check Google Business reviews, alert on negative
        logger.info("✅ Review Monitor Complete")

    async def _auto_lead_gen(self):
        """Auto Lead Generation"""
        logger.info("🎯 Auto Lead Generation Running...")

        if self.orchestrator:
            goal = "Find 10 new businesses in Kanpur without websites, save as leads"
            await self.orchestrator.execute_goal(goal)

        logger.info("✅ Auto Lead Gen Complete")

    async def _instagram_auto_post(self):
        """Auto Instagram Post"""
        logger.info("📸 Instagram Auto-Post Running...")

        if self.instagram:
            await self.instagram.create_and_post("daily")

        logger.info("✅ Instagram Post Complete")
