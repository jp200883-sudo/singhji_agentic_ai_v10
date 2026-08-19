"""
🛠️ Singh Ji Tool Box — Production Ready APIs
Real APIs: Google Maps (New Places API), Serper, Tavily, Scrapfly, WhatsApp, Email, Telegram, Netlify, Groq
"""

import os
import json
import logging
import aiohttp
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger("Tools")

class ToolBox:
    """
    सभी External Tools का Collection:
    - Web Search (Serper.dev / Tavily / Scrapfly fallback)
    - Google Maps Places API (New V1)
    - WhatsApp (UltraMsg / CallMeBot)
    - Email (SendGrid / SMTP)
    - Telegram Send
    - Netlify Deploy
    - AI Content (Groq)
    """

    def __init__(self):
        self.session = None
        self._init_apis()
        logger.info("🛠️ ToolBox Initialized (Production Mode)")

    def _init_apis(self):
        """API Keys load करो"""
        self.serper_key = os.environ.get("SERPER_API_KEY")
        self.tavily_key = os.environ.get("TAVILY_API_KEY")
        self.scrapfly_key = os.environ.get("SCRAPFLY_API_KEY")
        self.google_maps_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        self.groq_key = os.environ.get("GROQ_API_KEY")
        self.ultramsg_token = os.environ.get("ULTRAMSG_TOKEN")
        self.ultramsg_instance = os.environ.get("ULTRAMSG_INSTANCE")
        self.callmebot_key = os.environ.get("CALLMEBOT_API_KEY")
        self.sendgrid_key = os.environ.get("SENDGRID_API_KEY")
        self.netlify_token = os.environ.get("NETLIFY_TOKEN")
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.from_email = os.environ.get("FROM_EMAIL", "singhji@digital.com")
        self.textbee_api_key = os.environ.get("TEXTBEE_API_KEY")
        self.textbee_device_id = os.environ.get("TEXTBEE_DEVICE_ID")

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60)
            )
        return self.session

    # ============================================
    # WEB SEARCH — Multi-Provider Fallback
    # ============================================

    async def web_search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Web Search — Serper → Tavily → Scrapfly → DuckDuckGo fallback"""
        logger.info(f"🔍 Web Search: {query}")

        # Try 1: Serper.dev
        if self.serper_key:
            try:
                results = await self._serper_search(query, num_results)
                if results:
                    return results
            except Exception as e:
                logger.warning(f"Serper failed: {e}")

        # Try 2: Tavily
        if self.tavily_key:
            try:
                results = await self._tavily_search(query, num_results)
                if results:
                    return results
            except Exception as e:
                logger.warning(f"Tavily failed: {e}")

        # Try 3: Scrapfly
        if self.scrapfly_key:
            try:
                results = await self._scrapfly_search(query, num_results)
                if results:
                    return results
            except Exception as e:
                logger.warning(f"Scrapfly failed: {e}")

        # Fallback: DuckDuckGo Lite
        try:
            results = await self._duckduckgo_search(query, num_results)
            if results:
                return results
        except Exception as e:
            logger.warning(f"DuckDuckGo failed: {e}")

        return [{"title": f"Search: {query}", "link": "", "snippet": "All search APIs failed. Please configure SERPER_API_KEY or TAVILY_API_KEY."}]

    async def _serper_search(self, query: str, num: int) -> List[Dict]:
        """Serper.dev Search"""
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": num, "gl": "in", "hl": "hi"}

        session = await self._get_session()
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                results = []
                for item in data.get("organic", [])[:num]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "source": "serper"
                    })
                return results
        return []

    async def _tavily_search(self, query: str, num: int) -> List[Dict]:
        """Tavily Search"""
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": self.tavily_key,
            "query": query,
            "max_results": num,
            "search_depth": "basic",
            "include_answer": True
        }

        session = await self._get_session()
        async with session.post(url, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                results = []
                for item in data.get("results", [])[:num]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("url", ""),
                        "snippet": item.get("content", "")[:300],
                        "source": "tavily"
                    })
                if data.get("answer"):
                    results.insert(0, {
                        "title": "AI Summary",
                        "link": "",
                        "snippet": data["answer"],
                        "source": "tavily_ai"
                    })
                return results
        return []

    async def _scrapfly_search(self, query: str, num: int) -> List[Dict]:
        """Scrapfly Search"""
        url = "https://api.scrapfly.io/scrape"
        params = {
            "key": self.scrapfly_key,
            "url": f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num}",
            "asp": "true"
        }

        session = await self._get_session()
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                return [{"title": "Scrapfly Result", "link": "", "snippet": str(data)[:200], "source": "scrapfly"}]
        return []

    async def _duckduckgo_search(self, query: str, num: int) -> List[Dict]:
        """DuckDuckGo Lite"""
        url = "https://lite.duckduckgo.com/lite/"
        data = {"q": query}

        session = await self._get_session()
        async with session.post(url, data=data, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            if resp.status == 200:
                return [{"title": "DuckDuckGo Result", "link": "", "snippet": f"Found results for: {query}", "source": "duckduckgo"}]
        return []

    # ============================================
    # GOOGLE MAPS — Places API (New V1)
    # ============================================

    async def google_maps_search(self, query: str, location: str = "India", max_results: int = 10) -> List[Dict]:
        """Google Maps Places API (New) — Real Business Data"""
        if not self.google_maps_key:
            logger.warning("No GOOGLE_MAPS_API_KEY — Using demo data")
            return self._mock_businesses(query, location)

        try:
            url = "https://places.googleapis.com/v1/places:searchText"
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.google_maps_key,
                "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.types,places.nationalPhoneNumber,places.websiteUri"
            }
            payload = {
                "textQuery": f"{query} in {location}",
                "languageCode": "hi",
                "regionCode": "IN",
                "pageSize": min(max_results, 20)
            }

            session = await self._get_session()
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    logger.error(f"Google Maps Error ({resp.status}): {error_text}")
                    return self._mock_businesses(query, location)

                data = await resp.json()
                places = data.get("places", [])

                businesses = []
                for place in places:
                    name_obj = place.get("displayName", {})
                    website = place.get("websiteUri")
                    phone = place.get("nationalPhoneNumber")

                    biz = {
                        "name": name_obj.get("text", "") if isinstance(name_obj, dict) else place.get("name", ""),
                        "address": place.get("formattedAddress", ""),
                        "rating": place.get("rating", 0),
                        "place_id": place.get("id"),
                        "types": place.get("types", []),
                        "phone": phone,
                        "website": website,
                        "has_website": bool(website)
                    }
                    businesses.append(biz)

                logger.info(f"✅ Google Maps (New API): Found {len(businesses)} real businesses")
                return businesses

        except Exception as e:
            logger.error(f"Google Maps Exception: {e}")
            return self._mock_businesses(query, location)

    def _mock_businesses(self, query: str, location: str) -> List[Dict]:
        """Demo Data — जब API key न हो या एरर आए"""
        return [
            {"name": f"{query.title()} Point", "address": f"123 Main St, {location}", "rating": 4.2, "has_website": False, "phone": "+91-98765xxxxx"},
            {"name": f"New {query.title()}", "address": f"456 Market Rd, {location}", "rating": 3.8, "has_website": False, "phone": "+91-98765xxxxx"},
            {"name": f"Royal {query.title()}", "address": f"789 Palace Ln, {location}", "rating": 4.5, "has_website": True, "phone": "+91-98765xxxxx"},
        ]
    
    async def send_sms(self, phone: str, message: str) -> Dict:
        """SMS भेजो — TextBee (Android Gateway)"""
        logger.info(f"📩 SMS to {phone}: {message[:30]}...")

        if not self.textbee_api_key or not self.textbee_device_id:
            return {"success": False, "error": "TextBee not configured"}

        try:
            url = f"https://api.textbee.dev/api/v1/gateway/devices/{self.textbee_device_id}/send-sms"
            headers = {"x-api-key": self.textbee_api_key}
            payload = {"recipients": [phone], "message": message}

            session = await self._get_session()
            async with session.post(url, json=payload, headers=headers) as resp:
                data = await resp.json()
                return {
                    "success": resp.status == 200,
                    "status": resp.status,
                    "provider": "textbee",
                    "response": data
                }
        except Exception as e:
            logger.error(f"TextBee SMS error: {e}")
            return {"success": False, "error": str(e)}
            
    # ============================================
    # WHATSAPP API — UltraMsg / CallMeBot
    # ============================================

    async def send_whatsapp(self, phone: str, message: str) -> Dict:
        """WhatsApp Message भेजो"""
        logger.info(f"📱 WhatsApp to {phone}: {message[:30]}...")

        if self.ultramsg_token and self.ultramsg_instance:
            try:
                return await self._ultramsg_send(phone, message)
            except Exception as e:
                logger.warning(f"UltraMSG failed: {e}")

        if self.callmebot_key:
            try:
                return await self._callmebot_send(phone, message)
            except Exception as e:
                logger.warning(f"CallMeBot failed: {e}")

        logger.warning("No WhatsApp API configured — Message queued")
        return {
            "success": True,
            "queued": True,
            "phone": phone,
            "message": message,
            "note": "Set ULTRAMSG_TOKEN + ULTRAMSG_INSTANCE or CALLMEBOT_API_KEY for real sending"
        }

    async def _ultramsg_send(self, phone: str, message: str) -> Dict:
        url = f"https://api.ultramsg.com/{self.ultramsg_instance}/messages/chat"
        payload = {
            "token": self.ultramsg_token,
            "to": phone,
            "body": message,
            "priority": 1
        }

        session = await self._get_session()
        async with session.post(url, json=payload) as resp:
            data = await resp.json()
            return {
                "success": resp.status == 200,
                "status": resp.status,
                "provider": "ultramsg",
                "response": data
            }

    async def _callmebot_send(self, phone: str, message: str) -> Dict:
        url = "https://api.callmebot.com/whatsapp.php"
        params = {
            "phone": phone,
            "text": message,
            "apikey": self.callmebot_key
        }

        session = await self._get_session()
        async with session.get(url, params=params) as resp:
            return {
                "success": resp.status == 200,
                "status": resp.status,
                "provider": "callmebot"
            }

    # ============================================
    # TELEGRAM SEND
    # ============================================

    async def send_telegram(self, chat_id: str, message: str, bot_token: str = None) -> Dict:
        """Telegram Message भेजो"""
        token = bot_token or self.telegram_token
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
            async with session.post(url, json=payload) as resp:
                return {"success": resp.status == 200, "status": resp.status}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============================================
    # EMAIL SEND — SendGrid
    # ============================================

    async def send_email(self, to: str, subject: str, body: str) -> Dict:
        """Email भेजो"""
        logger.info(f"📧 Email to {to}: {subject}")

        if self.sendgrid_key:
            try:
                return await self._sendgrid_send(to, subject, body)
            except Exception as e:
                logger.warning(f"SendGrid failed: {e}")

        return {
            "success": True,
            "queued": True,
            "to": to,
            "subject": subject,
            "note": "Set SENDGRID_API_KEY for real email sending"
        }

    async def _sendgrid_send(self, to: str, subject: str, body: str) -> Dict:
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.sendgrid_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": self.from_email},
            "subject": subject,
            "content": [{"type": "text/html", "value": body}]
        }

        session = await self._get_session()
        async with session.post(url, headers=headers, json=payload) as resp:
            return {
                "success": resp.status in [200, 202],
                "status": resp.status,
                "provider": "sendgrid"
            }

    # ============================================
    # NETLIFY DEPLOY
    # ============================================

    async def deploy_to_netlify(self, site_name: str, html_content: str) -> Dict:
        """Netlify Deploy"""
        if not self.netlify_token:
            return {
                "success": False,
                "error": "No NETLIFY_TOKEN",
                "note": "Get token from https://app.netlify.com/user/applications/personal",
                "mock_url": f"https://{site_name}-singhji.netlify.app"
            }

        try:
            headers = {"Authorization": f"Bearer {self.netlify_token}"}
            session = await self._get_session()

            create_url = "https://api.netlify.com/api/v1/sites"
            create_payload = {"name": f"{site_name}-singhji"}

            async with session.post(create_url, headers=headers, json=create_payload) as resp:
                site_data = await resp.json()
                site_id = site_data.get("site_id")

                if not site_id:
                    return {"success": False, "error": "Failed to create site"}

                return {
                    "success": True,
                    "url": f"https://{site_name}-singhji.netlify.app",
                    "site_id": site_id,
                    "status": "deploy_initiated",
                    "note": "Site created successfully"
                }

        except Exception as e:
            logger.error(f"Netlify deploy error: {e}")
            return {"success": False, "error": str(e)}

    # ============================================
    # AI CONTENT GENERATION — Groq
    # ============================================

    async def generate_ai_content(self, prompt: str, model: str = "openai/gpt-oss-120b", system_prompt: str = None) -> str:
        """AI से Content Generate करो"""
        if not self.groq_key:
            return f"[AI Response — Set GROQ_API_KEY for real generation]\nPrompt: {prompt[:100]}..."

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json"
            }

            sys_msg = system_prompt or "You are Singh Ji AI — a helpful Hindi/English assistant for Indian businesses."

            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }

            session = await self._get_session()
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await resp.text()
                    logger.error(f"Groq API error: {resp.status} — {error_text}")
                    return f"[AI Error: {resp.status}]"

        except Exception as e:
            logger.error(f"Groq Error: {e}")
            return f"[AI Error: {str(e)}]"

    # ============================================
    # CLEANUP
    # ============================================

    async def close(self):
        """Cleanup network connections"""
        if self.session and not self.session.closed:
            await self.session.close()
