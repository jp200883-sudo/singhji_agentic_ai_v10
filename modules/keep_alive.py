"""
💓 Singh Ji Keep-Alive — Render को सोने नहीं देगा!
Every 30 min ping — 24x7 Active
"""

import os
import time
import asyncio
import logging
import threading
import aiohttp
from datetime import datetime

logger = logging.getLogger("KeepAlive")

class KeepAliveManager:
    """
    Render 15 min में सो जाता है — यह Manager हर 30 min में
    self-ping करके awake रखेगा!
    """

    def __init__(self, interval_minutes: int = 30):
        self.interval = interval_minutes * 60  # seconds
        self.running = False
        self.thread = None
        self.ping_count = 0
        self.last_ping = None

        # URLs to ping (self + external)
        self.urls = [
            os.environ.get("RENDER_EXTERNAL_URL", ""),
            os.environ.get("RAILWAY_STATIC_URL", ""),
            "https://singhji-api.onrender.com/ping",
        ]
        self.urls = [u for u in self.urls if u]

        logger.info(f"💓 KeepAlive Manager: {self.interval//60} min interval")

    def start(self):
        """Start Keep-Alive Thread"""
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("💓 Keep-Alive Started — Render will NEVER sleep!")

    def stop(self):
        """Stop Keep-Alive"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("🛑 Keep-Alive Stopped")

    def is_running(self) -> bool:
        return self.running

    def _run(self):
        """Background Thread — Ping Loop"""
        # Wait 5 min before first ping (let server start)
        time.sleep(300)

        while self.running:
            try:
                self._ping_all()
                self.ping_count += 1
                self.last_ping = datetime.now().isoformat()
            except Exception as e:
                logger.error(f"Keep-Alive Error: {e}")

            # Sleep until next ping
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)

    def _ping_all(self):
        """Ping all URLs"""
        for url in self.urls:
            try:
                import urllib.request
                req = urllib.request.Request(
                    f"{url}/ping" if not url.endswith('/ping') else url,
                    headers={'User-Agent': 'SinghJi-KeepAlive/1.0'},
                    method='GET'
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    logger.info(f"💓 Ping {url}: {resp.status}")
            except Exception as e:
                logger.warning(f"Ping failed {url}: {e}")

    def get_status(self) -> dict:
        """Current Status"""
        return {
            "running": self.running,
            "ping_count": self.ping_count,
            "last_ping": self.last_ping,
            "interval_minutes": self.interval // 60,
            "urls": self.urls
        }
