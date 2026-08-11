# 🦁 Singh Ji Agentic AI v10.0

> **Fully Autonomous Multi-Agent AI System** — Cloud Deployed, 24x7 Active, Zero Laptop Needed

---

## 🤖 क्या है यह?

Singh Ji Agentic AI v10.0 एक **Fully Autonomous AI System** है जो खुद सोचता है, खुद प्लान बनाता है, और खुद काम करता है।

### Normal AI vs Agentic AI

| Normal AI (v9) | Agentic AI (v10) |
|---|---|
| तुम हर Command दो | एक Goal दो, बाकी Agent संभाले |
| `/news` → News आई | `/auto_sell` → Leads + Outreach + Follow-up + Build |
| Single Task | Multi-step, Auto-correct, Loop |
| Reactive (बोलो तो करे) | Proactive (खुद काम करे) |
| 300 Agents Idle | 300 Agents Auto Assign |

---

## 📁 Project Structure

```
singhji_agentic_ai_v10/
├── main.py                    # FastAPI Server — Entry Point
├── core/
│   ├── __init__.py
│   ├── orchestrator.py        # 🧠 Master Brain — Goal → Plan → Execute
│   ├── agents.py              # 🤖 4 Agents: Research, Sales, Build, Support
│   ├── tools.py               # 🛠️ APIs: Search, WhatsApp, Email, Maps, Deploy
│   ├── memory.py              # 🧠 Supabase / Local JSON Memory
│   └── scheduler.py         # ⏰ 24x7 Background Jobs
├── modules/
│   ├── __init__.py
│   ├── keep_alive.py          # 💓 Render को सोने नहीं देगा!
│   └── instagram_agent.py     # 📸 Auto Post, Auto Caption, Auto Image
├── requirements.txt           # Python Dependencies
├── Dockerfile                 # Docker Image
├── render.yaml                # Render Deploy Config
├── .env.example               # Environment Variables Template
└── README.md                  # This File
```

---

## ⚡ Features

### 🤖 Agentic AI System
- **Orchestrator** — Goal को Tasks में तोड़ता है, Agents को Delegate करता है
- **Research Agent** — Google Maps से Business ढूँढना, Web Search, Data Analysis
- **Sales Agent** — WhatsApp Outreach, Email Sequence, Follow-up Scheduling
- **Build Agent** — Auto Website Code, Image Generate, Netlify Deploy
- **Support Agent** — Memory Save, Monitor, Reports

### 📸 Instagram Automation
- AI Image Generate (Pollinations — Free, No API Key)
- AI Caption Generate (Groq / Llama3)
- Auto Post to Instagram (Graph API)
- Schedule: हर 4 घंटे Auto Post

### 💓 Keep-Alive System
- Render 15 min में सोता है → हर 30 min Self-Ping
- 24x7 Awake — कोई Laptop चलाने की ज़रूरत नहीं

### ⏰ Auto Scheduler
| Time | Job |
|---|---|
| 6:00 AM | News + Weather + Mandi + Gold + Aaj Ka Vichar |
| 7:00 AM | Morning Digest Telegram |
| 6:00 PM | Evening Digest + Rozgar |
| Every 30 min | Keep-Alive Ping |
| Every 6 hours | Review Monitor |
| Every 7 days | Auto Lead Generation |
| Every 4 hours | Instagram Auto-Post |

---

## 🚀 Deploy — 3 Steps

### Option 1: Render (Recommended — Free)

1. **GitHub पे Push करो:**
```bash
git init
git add .
git commit -m "Singh Ji Agentic AI v10.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/singhji-agentic.git
git push -u origin main
```

2. **Render पे Connect करो:**
   - [render.com](https://render.com) → New Web Service
   - GitHub Repo Connect करो
   - Environment Variables Add करो (नीचे देखो)
   - Deploy → 24x7 Live!

3. **Telegram Webhook Set करो:**
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-app.onrender.com/telegram/webhook
```

### Option 2: Railway (Free)

1. [railway.app](https://railway.app) → New Project
2. GitHub से Import करो
3. Variables add करो
4. Deploy → Auto Scale → 24x7 Live!

### Option 3: Docker (Anywhere)

```bash
docker build -t singhji-agentic .
docker run -p 8000:8000 --env-file .env singhji-agentic
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | Telegram Bot Token |
| `ADMIN_CHAT_ID` | ✅ Yes | Your Telegram Chat ID |
| `GROQ_API_KEY` | ✅ Yes | AI Content Generation |
| `SUPABASE_URL` | ❌ No | Database (falls back to JSON) |
| `SUPABASE_KEY` | ❌ No | Database Key |
| `INSTAGRAM_ACCESS_TOKEN` | ❌ No | Instagram Auto-Post |
| `INSTAGRAM_USER_ID` | ❌ No | Instagram Account ID |
| `RENDER_EXTERNAL_URL` | ❌ No | Auto-set by Render |

---

## 💬 Telegram Commands

| Command | क्या होगा? |
|---|---|
| `/auto_sell cafe Kanpur 10` | 10 Cafes को Auto Message |
| `/auto_sell salon Kanpur 5` | 5 Salons को Auto Message |
| `/status` | System Status Check |
| `/instagram_post daily` | Instagram Post Schedule |

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | System Info |
| `/ping` | GET | Health Check |
| `/status` | GET | Full Status |
| `/agent/execute` | POST | Execute Any Goal |
| `/agent/auto-sell` | POST | Auto Client Acquisition |
| `/instagram/auto-post` | POST | Instagram Auto-Post |
| `/instagram/status` | GET | Instagram Status |
| `/memory/leads` | GET | All Leads |
| `/telegram/webhook` | POST | Telegram Updates |

---

## 🎯 Real Example

### Scenario: "Kanpur में 10 Cafe को Website बेचनी है"

**तुमने Telegram पे लिखा:**
```
/auto_sell cafe Kanpur 10
```

**Agent ने क्या किया (Auto):**
1. ✅ Google Maps API → Kanpur ke 10 Cafes निकाले
2. ✅ उनकी Websites Check कीं (किसकी नहीं है)
3. ✅ 10 Personalized WhatsApp Messages भेजे
4. ✅ Supabase में Leads Save किए
5. ✅ 2 दिन बाद Auto Follow-up Schedule किया
6. ✅ Reply आई → Sales Agent को Handover
7. ✅ Interested → Quote + Demo Link Auto भेजा
8. ✅ Payment मिली → Build Agent को Trigger
9. ✅ Website Live → Client को Link भेजा
10. ✅ 7 दिन बाद Feedback Agent Activate

**तुम्हें सिर्फ `/auto_sell` लिखना था।** 🚀

---

## 💰 Business Impact

| Without AI | With Agentic AI |
|---|---|
| 1 Client/Week | 10 Clients/Week |
| 10 Hours/Day Work | 2 Hours/Day Work |
| Manual Everything | 80% Auto |
| ₹10,000/Week | ₹80,000/Week |
| Render Sleeps | 24x7 Active |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI + Uvicorn
- **AI:** Groq (Llama3-70B) + Pollinations (Image Gen)
- **Database:** Supabase (PostgreSQL) / Local JSON
- **Deploy:** Render / Railway / Docker
- **Scheduler:** Asyncio Background Tasks
- **Memory:** Supabase + Local JSON Fallback

---

## 📞 Support

**Singh Ji Digital**
- 📱 WhatsApp: 7905 840149
- 🌐 Website: [Coming Soon]
- 🤖 Telegram: @SinghJiUltraBot

---

> *"AI तुम्हारी जगह नहीं लेता — AI तुम्हें Superhuman बनाता है।"* 🦁

**Singh Ji Agentic AI v10.0 — Deploy करो, Goal दो, सो जाओ, सुबह Leads मिलेंगी!** 🚀
