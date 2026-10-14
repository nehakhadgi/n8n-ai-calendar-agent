# 📅 AI Calendar Automator: Intelligent Scheduling Agent via n8n

An enterprise-grade, low-code **AI Agent workflow** built on n8n that acts as an intelligent personal assistant. The agent understands natural language scheduling requests via chat, dynamically parses target dates/times based on local user contexts, and automatically manages bookings using the Google Calendar API.

---

## 🏗️ System Architecture

The workflow leverages a modular agentic design:

1. **Trigger Interface (`On Chat Message`):** Serves as the user-facing natural language terminal.
2. **AI Agent Core (`AI Agent` Node):** An advanced reasoning model operating in a loop to parse intents and orchestrate dynamic execution.
3. **Large Language Model (`OpenAI Chat Model`):** Powered by `gpt-4o-mini` for fast, efficient semantic understanding and dynamic parameter extraction.
4. **Dynamic Contextualizer (System Prompt & Expressions):** Injecting native `Luxon` time-zone evaluations (`Asia/Kolkata`) to keep the LLM strictly aligned with local system time.
5. **Dynamic Tool integration (`Google Calendar`):** Custom dynamic integrations mapping schema properties (`start_time` and `end_time`) natively between the AI agent and the external Google Calendar API.

```
 [User Chat] ──> [AI Agent (gpt-4o-mini)] ──> [Google Calendar API (Create Event)]
                      │
              [System Time Zone]
```

---

## 🚀 How to Import and Deploy

To run this workflow yourself, follow these quick steps:

### Prerequisites
* A running **n8n instance** (Cloud or Local).
* An **OpenAI API Key** (to power the Chat Model).
* A **Google Cloud Project** with the Calendar API enabled (or simple n8n OAuth authorization credentials).

### Setup Instructions
1. Download the `workflow.json` file from this repository.
2. In your n8n workspace, click **Import from File** in your menu options.
3. Import the `workflow.json` file.
4. Double-click the **OpenAI Chat Model** node and select your credentials.
5. Double-click the **Google Calendar** node, click **Sign in with Google**, and authorize your calendar account.
6. Hit **Active** or open the chat terminal at the bottom of the canvas and say: *"Book a lunch meeting tomorrow at 1:00 PM for one hour."*

---

## 🛠️ Tech Stack & Key Concepts
* **Automation Engine:** n8n (Advanced AI workflows)
* **LLM Engine:** OpenAI (gpt-4o-mini)
* **API Integrations:** Google Calendar API, Google Cloud Console OAuth 2.0
* **Development Patterns:** Tool Calling (Function Calling), Chat Memory, Context Injection via Luxon expressions
