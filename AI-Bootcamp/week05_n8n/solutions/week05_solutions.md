# Week 5 Solutions

Reference solutions/notes for `../assignments/week05_assignments.md`. The `../workflows/` JSON
exports are complete reference implementations you can import directly — build your own first,
then compare.

---

## Solution 1 — n8n Basics
Reference: `../workflows/01_beginner_workflow.json`. Add an **IF** node after **Set**:
- Condition: `{{$json.week}}` equals `5` → true branch NoOp "Week 5", false branch NoOp "Other".
Key idea: data flows item-by-item; each node transforms `$json`.

---

## Solution 2 — Email Automation
Reference: `../workflows/02_email_automation.json`.
- The **Switch** routes on the lowercased, trimmed classifier output.
- Auto-reply only on the `support` output index.
- Error handling: attach an **Error Trigger** workflow, or wrap risky nodes and route failures
  to a logging node. Production must not silently drop emails.

---

## Solution 3 — Lead Qualification
Reference: `../workflows/03_lead_qualification.json`.
- The **Code** node parses the LLM's JSON (`JSON.parse($input.first().json.text)`) and merges
  it with the original webhook body.
- **IF** branches on `score >= 70`; qualified → Airtable create; both paths respond.
- Test:
  ```bash
  curl -X POST http://localhost:5678/webhook-test/lead-intake \
    -H "Content-Type: application/json" \
    -d '{"name":"Jane","company":"Acme","company_size":"500","budget":">100k","message":"Need a demo"}'
  ```

---

## Solution 4 — AI Agent
Reference: `../workflows/04_ai_agent_workflow.json`.
- Connect the **Anthropic Chat Model**, **Window Memory**, and **Calculator Tool** to the
  **AI Agent** via the `ai_languageModel`, `ai_memory`, and `ai_tool` ports (not the main flow).
- Add an **HTTP Request Tool** for the second tool. Memory enables the name-recall test.

---

## Solution 5 — CRM Automation
Reference: `../workflows/05_crm_automation.json`.
- Add a filter (IF or the search query's `where`) so only records missing `industry` proceed.
- Document required credentials: Airtable token + Anthropic + HubSpot (or Sheets + Anthropic).

---

## Solution 6 — WhatsApp Automation
Reference: `../workflows/06_whatsapp_automation.json`.
- System prompt instructs the model to ask for an order ID (format `ORD-#####`) if absent.
- Loop guard: ignore messages where `from` equals your own business number, or check a flag, so
  the bot never replies to its own outbound messages.

---

## Solution 7 — Multi-Agent Workflow
Reference: `../workflows/07_multi_agent_workflow.json`.
- Three sequential Anthropic nodes (researcher → writer → reviewer), each consuming the prior
  node's `text` output.
- Add a 4th node prompting the model to list claims needing citations.
- Trade-off: the pipeline yields higher-quality, reviewed output but costs ~4× the tokens/latency
  of a single call — worth it for published content, overkill for a quick internal note.
