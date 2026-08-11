"""
🧠 Singh Ji Memory — Long-term Storage
Supabase / Local JSON / Vector DB
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger("Memory")

class SupabaseMemory:
    """
    Long-term Memory System:
    - Tasks History
    - Leads Database
    - Conversation Context
    - Learned Patterns
    """

    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")
        self.local_mode = not (self.supabase_url and self.supabase_key)
        self.local_data = {"tasks": [], "leads": [], "conversations": [], "patterns": {}}
        self.initialized = False
        logger.info(f"🧠 Memory Mode: {'Supabase' if not self.local_mode else 'Local JSON'}")

    async def init(self):
        """Initialize connection"""
        if not self.local_mode:
            try:
                from supabase import create_client
                self.client = create_client(self.supabase_url, self.supabase_key)
                self.initialized = True
                logger.info("✅ Supabase Connected")
            except Exception as e:
                logger.warning(f"Supabase failed: {e} — Using Local JSON")
                self.local_mode = True
        else:
            self.initialized = True
            logger.info("✅ Local JSON Memory Ready")

    # ============================================
    # TASKS
    # ============================================

    async def save_task_step(self, task_id: str, step: Dict, result: Dict):
        """Task Step Save करो"""
        entry = {
            "task_id": task_id,
            "step": step,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }

        if self.local_mode:
            self.local_data["tasks"].append(entry)
            self._save_local()
        else:
            try:
                self.client.table("agent_tasks").insert(entry).execute()
            except Exception as e:
                logger.error(f"Supabase insert error: {e}")
                self.local_data["tasks"].append(entry)

    async def save_task_summary(self, task_id: str, summary: Dict):
        """Task Summary Save करो"""
        entry = {
            "task_id": task_id,
            "summary": summary,
            "completed_at": datetime.now().isoformat()
        }

        if self.local_mode:
            self.local_data["tasks"].append(entry)
            self._save_local()
        else:
            try:
                self.client.table("agent_summaries").insert(entry).execute()
            except:
                self.local_data["tasks"].append(entry)

    async def get_tasks(self) -> List[Dict]:
        """सभी Tasks लाओ"""
        if self.local_mode:
            return self.local_data["tasks"][-50:]  # Last 50
        else:
            try:
                resp = self.client.table("agent_tasks").select("*").order("timestamp", desc=True).limit(50).execute()
                return resp.data
            except:
                return self.local_data["tasks"][-50:]

    # ============================================
    # LEADS
    # ============================================

    async def save_lead(self, lead: Dict):
        """Lead Save करो"""
        lead["created_at"] = datetime.now().isoformat()
        lead["status"] = lead.get("status", "new")

        if self.local_mode:
            self.local_data["leads"].append(lead)
            self._save_local()
        else:
            try:
                self.client.table("agent_leads").insert(lead).execute()
            except:
                self.local_data["leads"].append(lead)

    async def get_leads(self, status: str = None) -> List[Dict]:
        """Leads लाओ"""
        if self.local_mode:
            leads = self.local_data["leads"]
            if status:
                leads = [l for l in leads if l.get("status") == status]
            return leads
        else:
            try:
                query = self.client.table("agent_leads").select("*")
                if status:
                    query = query.eq("status", status)
                resp = query.execute()
                return resp.data
            except:
                return self.local_data["leads"]

    async def update_lead(self, lead_id: str, updates: Dict):
        """Lead Update करो"""
        if self.local_mode:
            for i, lead in enumerate(self.local_data["leads"]):
                if lead.get("id") == lead_id:
                    self.local_data["leads"][i].update(updates)
                    self._save_local()
                    break
        else:
            try:
                self.client.table("agent_leads").update(updates).eq("id", lead_id).execute()
            except:
                pass

    # ============================================
    # CONVERSATIONS
    # ============================================

    async def save_conversation(self, user_id: str, message: str, response: str):
        """Conversation Save करो"""
        entry = {
            "user_id": user_id,
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }

        if self.local_mode:
            self.local_data["conversations"].append(entry)
            self._save_local()
        else:
            try:
                self.client.table("conversations").insert(entry).execute()
            except:
                self.local_data["conversations"].append(entry)

    # ============================================
    # LOCAL JSON HELPERS
    # ============================================

    def _save_local(self):
        """Local JSON File में Save करो"""
        try:
            with open("/tmp/singhji_memory.json", "w", encoding="utf-8") as f:
                json.dump(self.local_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Local save error: {e}")

    def _load_local(self):
        """Local JSON File से Load करो"""
        try:
            with open("/tmp/singhji_memory.json", "r", encoding="utf-8") as f:
                self.local_data = json.load(f)
        except:
            pass
