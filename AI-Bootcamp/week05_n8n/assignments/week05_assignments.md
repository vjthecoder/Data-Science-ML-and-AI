# Week 5 Assignments

Build each workflow in n8n, then export it as JSON into this folder named
`assignment<N>_<your_name>.json`. Reference notes are in `../solutions/`.

> **Setup:** run n8n locally with Docker (see `../workflows/README.md`) or use n8n Cloud. Store
> all API keys in n8n credentials — never in node fields or committed JSON.

---

## Assignment 1 — n8n Basics
1. Build a workflow: Manual Trigger → Set (create 3 fields) → IF (branch on one field) → two
   NoOp branches.
2. Execute it and screenshot the execution view.
3. Export the workflow JSON.

---

## Assignment 2 — Email Automation
1. Build IMAP Trigger → Claude classify (support/sales/spam/other) → Switch (4 outputs).
2. Add an auto-reply (Email Send) on the "support" branch only.
3. Add an error branch that logs failures (e.g. to a Google Sheet or NoOp with a note).

---

## Assignment 3 — Lead Qualification
1. Build Webhook → Claude score (return JSON {score, reason}) → Code (parse) → IF (score ≥ 70).
2. On the qualified branch, create a record in Airtable or a Google Sheet.
3. Respond to the webhook with the score. Test it with `curl` posting a sample lead.

---

## Assignment 4 — AI Agent
1. Build a Chat Trigger → AI Agent with an Anthropic chat model, window memory, and the
   calculator tool.
2. Add a second tool (e.g. an HTTP Request tool that hits a public API).
3. Test a multi-turn conversation that requires memory ("My name is X" … "What's my name?").

---

## Assignment 5 — CRM Automation
1. Build Schedule Trigger (every 6h) → fetch new contacts (Airtable/Sheet) → Claude enrich
   (summary + industry) → update the record.
2. Add a filter so only contacts missing an `industry` field are enriched.
3. Export and document which credentials are required.

---

## Assignment 6 — WhatsApp (or Telegram) Automation
1. Build WhatsApp/Telegram Trigger → Claude draft reply → send reply.
2. Make the assistant ask for an order ID if none is present, and confirm lookup if present.
3. Add an iteration guard so the workflow can't loop on its own outbound messages.

---

## Assignment 7 — Multi-Agent Workflow
1. Build Webhook → Researcher → Writer → Reviewer → Respond (3 sequential Claude nodes).
2. Add a 4th "fact-checker" node that flags claims needing citations.
3. Compare the multi-agent output to a single-node "do it all" prompt on the same topic and
   write 3 sentences on the quality vs cost trade-off.
