"""
📸 Singh Ji Instagram Agent — Auto Post, Auto Caption, Auto Schedule
No Laptop Needed — Render पे 24x7 चलेगा
"""

import os
import io
import base64
import logging
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger("InstagramAgent")

class InstagramAgent:
    """
    Instagram Automation Agent:
    - AI Image Generate (FLUX.1 / Stable Diffusion / Pollinations)
    - AI Caption Generate (Groq / Gemini)
    - Auto Post to Instagram (Instagram Graph API)
    - Schedule Posts
    - Monitor Engagement
    """

    def __init__(self, memory=None):
        self.memory = memory
        self.posts_today = 0
        self.max_posts_per_day = 5
        self.last_post_time = None

        # Instagram API Credentials
        self.ig_user_id = os.environ.get("INSTAGRAM_USER_ID", "")
        self.ig_access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")

        # AI APIs
        self.groq_key = os.environ.get("GROQ_API_KEY", "")

        logger.info("📸 Instagram Agent Initialized")

    async def create_and_post(self, topic: str = "daily") -> Dict:
        """
        Full Pipeline: Generate Image + Caption → Post to Instagram
        """
        logger.info(f"📸 Creating Instagram post for topic: {topic}")

        # Step 1: Generate Caption
        caption = await self._generate_caption(topic)

        # Step 2: Generate Image
        image_url = await self._generate_image(topic)

        # Step 3: Post to Instagram
        if self.ig_access_token and self.ig_user_id:
            result = await self._post_to_instagram(image_url, caption)
        else:
            # Queue for manual post
            result = {
                "success": True,
                "queued": True,
                "caption": caption,
                "image_url": image_url,
                "message": "Instagram credentials not set — Content generated, ready to post manually"
            }

        # Save to memory
        if self.memory:
            await self.memory.save_task_step(
                f"instagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                {"action": "instagram_post", "topic": topic},
                result
            )

        self.posts_today += 1
        self.last_post_time = datetime.now().isoformat()

        logger.info(f"✅ Instagram Post Complete: {result.get('status', 'done')}")
        return result

    async def _generate_caption(self, topic: str) -> str:
        """AI से Caption Generate करो"""

        prompts = {
            "daily": "Write an inspiring Hindi caption for Instagram about success and hard work. Add relevant hashtags. Keep it under 150 words.",
            "business": "Write a business growth tip in Hindi for Instagram. Add call-to-action. Add hashtags. Keep it under 150 words.",
            "tech": "Write a tech tip about AI/Automation in Hindi for Instagram. Add hashtags. Keep it under 150 words.",
            "motivation": "Write a powerful motivational quote in Hindi for Instagram. Add hashtags. Keep it under 100 words.",
            "festival": "Write a festive greeting in Hindi for Instagram. Add warm wishes and hashtags. Keep it under 150 words."
        }

        prompt = prompts.get(topic, prompts["daily"])

        # Try Groq API
        if self.groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.groq_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": "You are Singh Ji AI — Write engaging Hindi Instagram captions."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 500
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload, timeout=60) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            caption = data["choices"][0]["message"]["content"]
                            return caption.strip()
            except Exception as e:
                logger.warning(f"Groq caption error: {e}")

        # Fallback captions
        fallbacks = {
            "daily": "🚀 आज का दिन नई शुरुआत का है!\n\nहर मुश्किल एक मौका है आगे बढ़ने का। कभी हार मत मानो! 💪\n\n#Motivation #Success #HindiQuotes #SinghJiAI #DailyInspiration",
            "business": "💼 Business में Growth चाहिए?\n\nWebsite = 24x7 Showcase\nAI = 10x Faster\nAutomation = Scale\n\nआज ही Digital बनें! 🚀\n\n#BusinessGrowth #DigitalIndia #Website #AI #SinghJiDigital",
            "tech": "🤖 AI ने काम करना आसान बना दिया!\n\n10 घंटे का काम = 1 घंटे में\nCost = 90% कम\nQuality = 10x बेहतर\n\n#AI #Automation #Tech #Future #SinghJiAI",
            "motivation": "🔥 सपने वो नहीं जो नींद में आएं,\nसपने वो हैं जो नींद उड़ा दें!\n\n#Motivation #DreamBig #NeverGiveUp #SinghJiAI",
            "festival": "🙏 सभी को शुभकामनाएं!\n\nखुशियां बरसें, सफलता मिले,\nहर दिन नया उत्साह लाए! 🎉\n\n#Festival #Celebration #Blessings #SinghJiAI"
        }

        return fallbacks.get(topic, fallbacks["daily"])

    async def _generate_image(self, topic: str) -> str:
        """AI Image Generate करो — Pollinations (Free, No API Key)"""

        prompts = {
            "daily": "Inspirational sunrise over Indian city, golden light, motivational atmosphere, cinematic, high quality, vibrant colors",
            "business": "Modern digital business office, laptop with website on screen, Indian entrepreneur, professional, clean design, tech aesthetic",
            "tech": "Futuristic AI robot brain, neural network visualization, blue and purple colors, technology, high tech, digital art",
            "motivation": "Lion standing on mountain peak, sunrise background, powerful, majestic, golden light, motivational, cinematic",
            "festival": "Colorful Indian festival celebration, diyas, flowers, vibrant colors, warm lighting, traditional, beautiful"
        }

        prompt = prompts.get(topic, prompts["daily"])

        # Pollinations AI (FREE — No API Key needed)
        try:
            encoded_prompt = prompt.replace(" ", "%20")
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true&seed={datetime.now().timestamp()}"

            # Verify image is accessible
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=60) as resp:
                    if resp.status == 200:
                        logger.info(f"🎨 Image generated via Pollinations")
                        return image_url
        except Exception as e:
            logger.warning(f"Pollinations error: {e}")

        # Fallback: Return placeholder service
        return f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1080&height=1080"

    async def _post_to_instagram(self, image_url: str, caption: str) -> Dict:
        """Instagram Graph API से Post करो"""

        if not self.ig_access_token or not self.ig_user_id:
            return {"success": False, "error": "Instagram credentials missing"}

        try:
            base_url = "https://graph.facebook.com/v18.0"

            # Step 1: Create Media Container
            media_url = f"{base_url}/{self.ig_user_id}/media"
            media_params = {
                "image_url": image_url,
                "caption": caption,
                "access_token": self.ig_access_token
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(media_url, params=media_params, timeout=60) as resp:
                    media_data = await resp.json()

                    if "id" not in media_data:
                        return {"success": False, "error": media_data.get("error", "Unknown error")}

                    creation_id = media_data["id"]

                    # Step 2: Publish Media
                    publish_url = f"{base_url}/{self.ig_user_id}/media_publish"
                    publish_params = {
                        "creation_id": creation_id,
                        "access_token": self.ig_access_token
                    }

                    async with session.post(publish_url, params=publish_params, timeout=60) as resp:
                        publish_data = await resp.json()

                        if "id" in publish_data:
                            return {
                                "success": True,
                                "post_id": publish_data["id"],
                                "image_url": image_url,
                                "caption": caption[:50] + "...",
                                "posted_at": datetime.now().isoformat()
                            }
                        else:
                            return {"success": False, "error": publish_data.get("error", "Publish failed")}

        except Exception as e:
            logger.error(f"Instagram Post Error: {e}")
            return {"success": False, "error": str(e)}

    async def get_status(self) -> Dict:
        """Agent Status"""
        return {
            "agent": "InstagramAgent",
            "posts_today": self.posts_today,
            "max_posts_per_day": self.max_posts_per_day,
            "last_post_time": self.last_post_time,
            "credentials_set": bool(self.ig_access_token and self.ig_user_id),
            "status": "active"
        }
