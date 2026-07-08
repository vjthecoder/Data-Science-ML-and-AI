# Week 5 Workflow Exports (n8n)

Importable n8n workflow JSON files. Each demonstrates an AI-automation pattern.

## How to import
1. Open n8n (cloud or self-hosted). Self-host quickly with Docker:
   ```bash
   docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
   ```
2. In the n8n editor: **Workflows → Import from File** (or paste JSON via the `...` menu).
3. Open each node that shows a credential placeholder (`REPLACE_WITH_..._CREDENTIAL_ID`) and
   select/create the matching credential in n8n's **Credentials** store.
4. For webhook/trigger workflows, activate the workflow or use **Execute Workflow** / the test
   webhook URL.

> **Secrets:** credentials live in n8n's encrypted credential store — never paste API keys
> directly into node fields or commit them to these JSON files. The exports intentionally use
> placeholder credential IDs.

## Workflows

| File | Pattern | Key nodes |
|------|---------|-----------|
| `01_beginner_workflow.json` | n8n basics | Manual Trigger → Set → NoOp |
| `02_email_automation.json` | Classify + auto-reply | IMAP Trigger → Claude classify → Switch → Email Send |
| `03_lead_qualification.json` | Webhook → AI score → CRM | Webhook → Claude score → Code parse → IF → Airtable |
| `04_ai_agent_workflow.json` | AI Agent with tools + memory | Chat Trigger → Agent (Anthropic model + window memory + calculator) |
| `05_crm_automation.json` | Scheduled enrichment | Schedule → Airtable search → Claude enrich → HubSpot update |
| `06_whatsapp_automation.json` | WhatsApp AI assistant | WhatsApp Trigger → Claude draft → WhatsApp Send |
| `07_multi_agent_workflow.json` | Multi-agent pipeline | Webhook → Researcher → Writer → Reviewer → Respond |

## Model note
LLM nodes use Anthropic `claude-opus-4-8`. You can swap the model in each node's parameters
(e.g. to `claude-fable-5` for the most capable model, or an OpenAI/Gemini node).

## Common gotchas
- Trigger workflows must be **active** (or run via the test URL) to receive events.
- Add an **Error Trigger** workflow or per-node error handling for production reliability.
- The `Code`/`Switch` nodes assume the LLM returns the expected shape — add validation in
  production (the JSON-parse step in workflow 03 is an example).
