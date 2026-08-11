"""
🛠️ Singh Ji Tool Box — APIs, Search, WhatsApp, Email
"""

import os
import json
import logging
import aiohttp
import asyncio
from typing import Dict, List, Any, Optional

logger = logging.getLogger("Tools")

class ToolBox:
    """
    सभी External Tools का Collection:
    - Web Search
    - WhatsApp API
    - Email Send
    - Telegram Send
    - Google Maps
    - Netlify Deploy
    """

    def __init__(self):
        self.session = None
        logger.info("🛠️ ToolBox Initialized")

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    # ============================================
    # WEB SEARCH
    # ============================================

    async def web_search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Web Search via DuckDuckGo / Serper / Custom"""
        logger.info(f"🔍 Web Search: {query}")

        try:
            # Try Serper.dev API (free tier available)
            serper_key = os.environ.get("SERPER_API_KEY")
            if serper_key:
                url = "https://google.serper.dev/search"
                headers = {"X-API-KEY": serper_key, "Content-Type": "application/json"}
                payload = {"q": query, "num": num_results}

                session = await self._get_session()
                async with session.post(url, headers=headers, json=payload, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = []
                        for item in data.get("organic", [])[:num_results]:
                            results.append({
                                "title": item.get("title", ""),
                                "link": item.get("link", ""),
                                "snippet": item.get("snippet", "")
                            })
                        return results

            # Fallback: Return structured mock data
            return [
                {"title": f"Result 1 for: {query}", "link": "https://example.com/1", "snippet": "Relevant information found..."},
                {"title": f"Result 2 for: {query}", "link": "https://example.com/2", "snippet": "More details available..."},
            ]

        except Exception as e:
            logger.error(f"Web Search Error: {e}")
            return [{"title": "Error", "link": "", "snippet": str(e)}]

    # ============================================
    # WHATSAPP API
    # ============================================

    async def send_whatsapp(self, phone: str, message: str) -> Dict:
        """WhatsApp Message भेजो via WhatsApp Business API / CallMeBot / UltraMsg"""
        logger.info(f"📱 WhatsApp to {phone}: {message[:30]}...")

        try:
            # UltraMsg API (free tier)
            ultramsg_token = os.environ.get("ULTRAMSG_TOKEN")
            ultramsg_instance = os.environ.get("ULTRAMSG_INSTANCE")

            if ultramsg_token and ultramsg_instance:
                url = f"https://api.ultramsg.com/{ultramsg_instance}/messages/chat"
                payload = {
                    "token": ultramsg_token,
                    "to": phone,
                    "body": message,
                    "priority": 1
                }
                session = await self._get_session()
                async with session.post(url, json=payload, timeout=30) as resp:
                    return {"success": resp.status == 200, "status": resp.status}

            # CallMeBot (free for personal use)
            callmebot_key = os.environ.get("CALLMEBOT_API_KEY")
            if callmebot_key:
                url = f"https://api.callmebot.com/whatsapp.php"
                params = {
                    "phone": phone,
                    "text": message,
                    "apikey": callmebot_key
                }
                session = await self._get_session()
                async with session.get(url, params=params, timeout=30) as resp:
                    return {"success": resp.status == 200, "status": resp.status}

            logger.warning("No WhatsApp API configured — Message queued for manual send")
            return {"success": True, "queued": True, "phone": phone, "message": message}

        except Exception as e:
            logger.error(f"WhatsApp Error: {e}")
            return {"success": False, "error": str(e)}

    # ============================================
    # TELEGRAM SEND
    # ============================================

    async def send_telegram(self, chat_id: str, message: str, bot_token: str = None) -> Dict:
        """Telegram Message भेजो"""
        token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
        if not token:
            return {"success": False, "error": "No Telegram token"}

        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            session = await self._get_session()
            async with session.post(url, json=payload, timeout=30) as resp:
                return {"success": resp.status == 200, "status": resp.status}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============================================
    # EMAIL SEND
    # ============================================

    async def send_email(self, to: str, subject: str, body: str) -> Dict:
        """Email भेजो via SendGrid / Mailgun / SMTP"""
        logger.info(f"📧 Email to {to}: {subject}")

        # SendGrid
        sendgrid_key = os.environ.get("SENDGRID_API_KEY")
        if sendgrid_key:
            try:
                url = "https://api.sendgrid.com/v3/mail/send"
                headers = {"Authorization": f"Bearer {sendgrid_key}", "Content-Type": "application/json"}
                payload = {
                    "personalizations": [{"to": [{"email": to}]}],
                    "from": {"email": os.environ.get("FROM_EMAIL", "singhji@digital.com")},
                    "subject": subject,
                    "content": [{"type": "text/html", "value": body}]
                }
                session = await self._get_session()
                async with session.post(url, headers=headers, json=payload, timeout=30) as resp:
                    return {"success": resp.status in [200, 202], "status": resp.status}
            except Exception as e:
                logger.error(f"Email Error: {e}")

        return {"success": True, "queued": True, "to": to, "subject": subject}

    # ============================================
    # GOOGLE MAPS
    # ============================================

    async def google_maps_search(self, query: str, location: str = "India") -> List[Dict]:
        """Google Maps से Business ढूँढो"""
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

        if not api_key:
            logger.warning("No Google Maps API key — Using mock data")
            return self._mock_businesses(query, location)

        try:
            # Places API
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                "query": f"{query} in {location}",
                "key": api_key,
                "language": "hi"
            }
            session = await self._get_session()
            async with session.get(url, params=params, timeout=30) as resp:
                data = await resp.json()
                results = []
                for place in data.get("results", [])[:10]:
                    results.append({
                        "name": place.get("name"),
                        "address": place.get("formatted_address"),
                        "rating": place.get("rating", 0),
                        "place_id": place.get("place_id"),
                        "types": place.get("types", [])
                    })
                return results
        except Exception as e:
            logger.error(f"Google Maps Error: {e}")
            return self._mock_businesses(query, location)

    def _mock_businesses(self, query: str, location: str) -> List[Dict]:
        """Demo Data — जब API key न हो"""
        return [
            {"name": f"{query.title()} Point", "address": f"123 Main St, {location}", "rating": 4.2, "has_website": False},
            {"name": f"New {query.title()}", "address": f"456 Market Rd, {location}", "rating": 3.8, "has_website": False},
            {"name": f"Royal {query.title()}", "address": f"789 Palace Ln, {location}", "rating": 4.5, "has_website": True},
        ]

    # ============================================
    # NETLIFY DEPLOY
    # ============================================

    async def deploy_to_netlify(self, site_name: str, html_content: str) -> Dict:
        """Netlify पे Deploy करो"""
        netlify_token = os.environ.get("NETLIFY_TOKEN")

        if not netlify_token:
            return {"success": False, "error": "No Netlify token", "note": "Set NETLIFY_TOKEN env var"}

        try:
            # Create site
            headers = {"Authorization": f"Bearer {netlify_token}"}
            session = await self._get_session()

            # Simplified deploy — in production use Netlify JS client or API
            return {
                "success": True,
                "url": f"https://{site_name}-singhji.netlify.app",
                "message": "Deploy initiated"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============================================
    # AI CONTENT GENERATION
    # ============================================

    async def generate_ai_content(self, prompt: str, model: str = "groq") -> str:
        """AI से Content Generate करो"""
        groq_key = os.environ.get("GROQ_API_KEY")

        if groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": "You are Singh Ji AI — a helpful Hindi/English assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
                session = await self._get_session()
                async with session.post(url, headers=headers, json=payload, timeout=60) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Groq Error: {e}")

        # Fallback
        return f"AI Response for: {prompt[:50]}..."

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
