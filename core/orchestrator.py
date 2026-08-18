"""
🧠 Singh Ji Orchestrator — Production Ready
Master Brain: Goal → AI Plan → Execute → Reflect → Memory
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

from core.agents import ResearchAgent, SalesAgent, BuildAgent, SupportAgent
from core.tools import ToolBox

logger = logging.getLogger("Orchestrator")

class SinghJiOrchestrator:
    """
    Master Brain:
    1. Goal को समझो (AI Analysis)
    2. Plan बनाओ (AI Planning)
    3. Agents को Delegate करो
    4. Results को Memory में Save करो
    5. Follow-up Schedule करो
    """

    def __init__(self, memory=None):
        self.memory = memory
        self.tools = ToolBox()
        self.agents = {
            'research': ResearchAgent(),
            'sales': SalesAgent(),
            'build': BuildAgent(),
            'support': SupportAgent()
        }
        self.active_tasks = {}
        logger.info("🧠 Orchestrator Initialized (Production Mode)")

    async def execute_goal(self, goal: str) -> Dict[str, Any]:
        """
        Main Entry Point — कोई भी Goal यहाँ से शुरू होता है
        """
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"🎯 NEW GOAL: {goal} | Task ID: {task_id}")

        # Step 1: AI से Plan बनवाओ
        plan = await self._create_ai_plan(goal)
        logger.info(f"📋 AI Plan Created: {len(plan)} steps")

        # Step 2: Step-by-Step Execute
        results = []
        for i, step in enumerate(plan):
            logger.info(f"⚡ Executing Step {i+1}/{len(plan)}: {step['action']}")

            try:
                result = await self._execute_step(step)

                # Check Success
                if not result.get('success', False):
                    logger.warning(f"⚠️ Step {i+1} failed — Attempting fix...")
                    result = await self._retry_or_fix(step, result.get('error'))

                results.append(result)

                # Save to Memory
                if self.memory:
                    await self.memory.save_task_step(task_id, step, result)

            except Exception as e:
                logger.error(f"❌ Step {i+1} Error: {str(e)}")
                results.append({"success": False, "error": str(e)})

        # Final AI Summary
        summary = await self._generate_summary(goal, plan, results)

        if self.memory:
            await self.memory.save_task_summary(task_id, summary)

        logger.info(f"✅ GOAL COMPLETE: {goal} | Success: {summary['completed_steps']}/{summary['total_steps']}")
        return summary

    async def _create_ai_plan(self, goal: str) -> List[Dict]:
        """
        AI से Smart Plan बनवाओ — Goal को analyze करके best approach decide करो
        """
        goal_lower = goal.lower()

        # Pattern Detection (fast path)
        if any(word in goal_lower for word in ['sell', 'client', 'lead', 'outreach', 'prospect']):
            return await self._plan_auto_sell(goal)

        elif any(word in goal_lower for word in ['instagram', 'post', 'social', 'caption']):
            return await self._plan_instagram(goal)

        elif any(word in goal_lower for word in ['research', 'find', 'search', 'data']):
            return await self._plan_research(goal)

        elif any(word in goal_lower for word in ['build', 'website', 'create', 'deploy']):
            return await self._plan_build(goal)

        # AI Planning for unknown goals
        return await self._plan_with_ai(goal)

    async def _plan_with_ai(self, goal: str) -> List[Dict]:
        """AI से custom plan बनवाओ"""
        plan_prompt = f"""Given this goal: "{goal}"

Create a step-by-step plan for an AI agent system with these agents: Research, Sales, Build, Support.

Return ONLY a JSON array like:
[
  {{"action": "action_name", "agent": "agent_name", "params": {{"key": "value"}}}},
  ...
]

Agents available:
- research: web_search, research_businesses, filter_prospects, generate_content, analyze_data
- sales: generate_outreach, send_messages, schedule_followup
- build: generate_code, create_image, deploy
- support: save_leads, save_report, monitor_engagement"""

        try:
            plan_json = await self.tools.generate_ai_content(
                prompt=plan_prompt,
                system_prompt="You are an AI planning expert. Return only valid JSON arrays."
            )

            # Parse JSON from response
            import re
            json_match = re.search(r'\[.*\]', plan_json, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
                if isinstance(plan, list) and len(plan) > 0:
                    return plan
        except Exception as e:
            logger.warning(f"AI planning failed: {e}, using default plan")

        # Fallback to default
        return [
            {"action": "analyze_goal", "agent": "research", "params": {"goal": goal}},
            {"action": "web_search", "agent": "research", "params": {"query": goal}},
            {"action": "save_report", "agent": "support", "params": {"goal": goal}}
        ]

    async def _plan_auto_sell(self, goal: str) -> List[Dict]:
        """Auto Client Acquisition Plan — Real APIs"""
        # Extract parameters from goal
        parts = goal.lower().split()
        count = 10
        city = "Kanpur"
        business_type = "cafe"

        for i, part in enumerate(parts):
            if part.isdigit():
                count = int(part)
            elif part in ['kanpur', 'delhi', 'mumbai', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'pune', 'jaipur', 'lucknow']:
                city = part.title()
            elif part in ['cafe', 'restaurant', 'salon', 'hotel', 'shop', 'clinic', 'hospital', 'school', 'gym', 'store']:
                business_type = part

        return [
            {"action": "research_businesses", "agent": "research", "params": {"goal": goal, "source": "google_maps", "business_type": business_type, "city": city}},
            {"action": "filter_prospects", "agent": "research", "params": {"filter": "no_website", "rating_min": 3.5, "business_type": business_type, "city": city}},
            {"action": "generate_outreach", "agent": "sales", "params": {"channel": "whatsapp", "personalized": True, "business_type": business_type, "city": city}},
            {"action": "send_messages", "agent": "sales", "params": {"batch_size": count, "delay": 30, "channel": "whatsapp"}},
            {"action": "schedule_followup", "agent": "sales", "params": {"delay_hours": 48}},
            {"action": "save_leads", "agent": "support", "params": {"status": "outreach_sent"}}
        ]

    async def _plan_instagram(self, goal: str) -> List[Dict]:
        """Instagram Automation Plan"""
        topic = "daily"
        if "business" in goal.lower():
            topic = "business"
        elif "tech" in goal.lower():
            topic = "tech"
        elif "motivation" in goal.lower():
            topic = "motivation"

        return [
            {"action": "generate_content", "agent": "research", "params": {"type": "caption", "topic": topic}},
            {"action": "create_image", "agent": "build", "params": {"style": "social_media", "size": "1080x1080", "topic": topic}},
            {"action": "schedule_post", "agent": "sales", "params": {"platform": "instagram", "optimal_time": True}},
            {"action": "monitor_engagement", "agent": "support", "params": {"track": ["likes", "comments", "shares"]}}
        ]

    async def _plan_research(self, goal: str) -> List[Dict]:
        """Research Plan — Real Web Search"""
        return [
            {"action": "web_search", "agent": "research", "params": {"query": goal, "results": 10}},
            {"action": "analyze_data", "agent": "research", "params": {"extract": "key_points"}},
            {"action": "save_report", "agent": "support", "params": {"format": "json"}}
        ]

    async def _plan_build(self, goal: str) -> List[Dict]:
        """Build/Create Plan — AI Code + Deploy"""
        return [
            {"action": "generate_code", "agent": "build", "params": {"type": "auto_detect", "goal": goal}},
            {"action": "create_image", "agent": "build", "params": {"type": "website", "style": "hero"}},
            {"action": "deploy", "agent": "build", "params": {"platform": "netlify"}},
            {"action": "save_report", "agent": "support", "params": {"format": "json"}}
        ]

    async def _execute_step(self, step: Dict) -> Dict:
        """Single Step Execute — Agent को Delegate करो"""
        agent_name = step.get('agent', 'research')
        action = step.get('action', 'unknown')
        params = step.get('params', {})

        agent = self.agents.get(agent_name)
        if not agent:
            return {"success": False, "error": f"Agent {agent_name} not found"}

        # Execute based on action type
        action_map = {
            "research_businesses": agent.research_businesses,
            "filter_prospects": agent.filter_prospects,
            "generate_outreach": agent.generate_outreach,
            "send_messages": agent.send_messages,
            "schedule_followup": agent.schedule_followup,
            "generate_content": agent.generate_content,
            "create_image": agent.create_image,
            "web_search": agent.web_search,
            "generate_code": agent.generate_code,
            "deploy": agent.deploy,
            "save_leads": agent.save_leads,
            "save_report": agent.save_report,
            "monitor_engagement": agent.monitor_engagement,
            "analyze_data": agent.analyze_data,
            "analyze_goal": agent.analyze_data,
            "schedule_post": agent.schedule_post
        }

        handler = action_map.get(action)
        if handler:
            return await handler(params)
        else:
            return await agent.execute(action, params)

    async def _retry_or_fix(self, step: Dict, error: str) -> Dict:
        """गलती हुई? Retry करो या Alternative तरीका अपनाओ"""
        logger.info(f"🔧 Retrying step: {step['action']} | Error: {error}")

        # Try once more with modified params
        modified_step = step.copy()
        modified_step['params'] = {**modified_step.get('params', {}), 'retry': True, 'fallback': True}

        try:
            return await self._execute_step(modified_step)
        except Exception as e:
            logger.error(f"❌ Retry failed: {str(e)}")
            return {"success": False, "error": str(e), "retried": True}

    async def _generate_summary(self, goal: str, plan: List[Dict], results: List[Dict]) -> Dict:
        """AI से Final Summary Generate करो"""
        completed = sum(1 for r in results if r.get('success'))
        failed = sum(1 for r in results if not r.get('success'))

        # AI-generated summary
        summary_prompt = f"""Summarize this task completion in Hindi:

Goal: {goal}
Total Steps: {len(plan)}
Completed: {completed}
Failed: {failed}

Write a brief, encouraging summary for the user."""

        try:
            ai_summary = await self.tools.generate_ai_content(
                prompt=summary_prompt,
                system_prompt="You are Singh Ji AI. Write encouraging summaries in Hindi."
            )
        except:
            ai_summary = f"✅ Task Complete: {completed}/{len(plan)} steps successful"

        return {
            "task_id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "goal": goal,
            "total_steps": len(plan),
            "completed_steps": completed,
            "failed_steps": failed,
            "results": results,
            "ai_summary": ai_summary,
            "timestamp": datetime.now().isoformat()
        }
