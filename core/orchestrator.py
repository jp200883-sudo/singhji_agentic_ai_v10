"""
🧠 Singh Ji Orchestrator — Master Brain of Agentic AI
Goal → Plan → Delegate → Execute → Reflect → Memory
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
    Master Brain — Goal को Tasks में तोड़ता है,
    Agents को Delegate करता है,
    Results को Memory में Save करता है
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
        logger.info("🧠 Orchestrator Initialized")

    async def execute_goal(self, goal: str) -> Dict[str, Any]:
        """
        Main Entry Point — कोई भी Goal यहाँ से शुरू होता है
        """
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"🎯 NEW GOAL: {goal} | Task ID: {task_id}")

        # Step 1: Plan बनाओ
        plan = await self._create_plan(goal)
        logger.info(f"📋 Plan Created: {len(plan)} steps")

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

        # Final Summary
        summary = {
            "task_id": task_id,
            "goal": goal,
            "total_steps": len(plan),
            "completed_steps": sum(1 for r in results if r.get('success')),
            "failed_steps": sum(1 for r in results if not r.get('success')),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }

        if self.memory:
            await self.memory.save_task_summary(task_id, summary)

        logger.info(f"✅ GOAL COMPLETE: {goal} | Success: {summary['completed_steps']}/{summary['total_steps']}")
        return summary

    async def _create_plan(self, goal: str) -> List[Dict]:
        """
        Goal को Steps में तोड़ो — AI Planning
        """
        goal_lower = goal.lower()

        # Auto-Sell Pattern Detection
        if "sell" in goal_lower or "client" in goal_lower or "lead" in goal_lower:
            return self._plan_auto_sell(goal)

        # Instagram Pattern
        elif "instagram" in goal_lower or "post" in goal_lower or "social" in goal_lower:
            return self._plan_instagram(goal)

        # Research Pattern
        elif "research" in goal_lower or "find" in goal_lower or "search" in goal_lower:
            return self._plan_research(goal)

        # Build Pattern
        elif "build" in goal_lower or "website" in goal_lower or "create" in goal_lower:
            return self._plan_build(goal)

        # Default Plan
        else:
            return [
                {"action": "analyze_goal", "agent": "research", "params": {"goal": goal}},
                {"action": "execute_primary", "agent": "research", "params": {"goal": goal}},
                {"action": "save_results", "agent": "support", "params": {"goal": goal}}
            ]

    def _plan_auto_sell(self, goal: str) -> List[Dict]:
        """Auto Client Acquisition Plan"""
        return [
            {"action": "research_businesses", "agent": "research", "params": {"goal": goal, "source": "google_maps"}},
            {"action": "filter_prospects", "agent": "research", "params": {"filter": "no_website", "rating_min": 3.5}},
            {"action": "generate_outreach", "agent": "sales", "params": {"channel": "whatsapp", "personalized": True}},
            {"action": "send_messages", "agent": "sales", "params": {"batch_size": 10, "delay": 30}},
            {"action": "schedule_followup", "agent": "sales", "params": {"delay_hours": 48}},
            {"action": "save_leads", "agent": "support", "params": {"status": "outreach_sent"}}
        ]

    def _plan_instagram(self, goal: str) -> List[Dict]:
        """Instagram Automation Plan"""
        return [
            {"action": "generate_content", "agent": "research", "params": {"type": "image_caption", "topic": goal}},
            {"action": "create_image", "agent": "build", "params": {"style": "social_media", "size": "1080x1080"}},
            {"action": "schedule_post", "agent": "sales", "params": {"platform": "instagram", "optimal_time": True}},
            {"action": "monitor_engagement", "agent": "support", "params": {"track": ["likes", "comments", "shares"]}}
        ]

    def _plan_research(self, goal: str) -> List[Dict]:
        """Research Plan"""
        return [
            {"action": "web_search", "agent": "research", "params": {"query": goal, "results": 10}},
            {"action": "analyze_data", "agent": "research", "params": {"extract": "key_points"}},
            {"action": "summarize", "agent": "research", "params": {"format": "structured"}},
            {"action": "save_report", "agent": "support", "params": {"format": "json"}}
        ]

    def _plan_build(self, goal: str) -> List[Dict]:
        """Build/Create Plan"""
        return [
            {"action": "gather_requirements", "agent": "research", "params": {"goal": goal}},
            {"action": "generate_code", "agent": "build", "params": {"type": "auto_detect"}},
            {"action": "test_output", "agent": "build", "params": {"validate": True}},
            {"action": "deploy", "agent": "build", "params": {"platform": "netlify"}},
            {"action": "notify_client", "agent": "sales", "params": {"channel": "whatsapp"}}
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
        if action == "research_businesses":
            return await agent.research_businesses(params)
        elif action == "filter_prospects":
            return await agent.filter_prospects(params)
        elif action == "generate_outreach":
            return await agent.generate_outreach(params)
        elif action == "send_messages":
            return await agent.send_messages(params)
        elif action == "schedule_followup":
            return await agent.schedule_followup(params)
        elif action == "generate_content":
            return await agent.generate_content(params)
        elif action == "create_image":
            return await agent.create_image(params)
        elif action == "web_search":
            return await agent.web_search(params)
        elif action == "generate_code":
            return await agent.generate_code(params)
        elif action == "deploy":
            return await agent.deploy(params)
        elif action == "save_leads":
            return await agent.save_leads(params)
        elif action == "save_report":
            return await agent.save_report(params)
        elif action == "monitor_engagement":
            return await agent.monitor_engagement(params)
        else:
            return await agent.execute(action, params)

    async def _retry_or_fix(self, step: Dict, error: str) -> Dict:
        """गलती हुई? Retry करो या Alternative तरीका अपनाओ"""
        logger.info(f"🔧 Retrying step: {step['action']} | Error: {error}")

        # Try once more with modified params
        modified_step = step.copy()
        modified_step['params']['retry'] = True
        modified_step['params']['fallback'] = True

        try:
            return await self._execute_step(modified_step)
        except Exception as e:
            logger.error(f"❌ Retry failed: {str(e)}")
            return {"success": False, "error": str(e), "retried": True}
