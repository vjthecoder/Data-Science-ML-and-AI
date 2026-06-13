# Week 5 Lesson Plan: AI Automation with n8n

**Total Duration:** ~15-20 hours over 5 days

| Day | Topics | Workflow(s) | Duration | Deliverable |
|-----|--------|-------------|----------|-------------|
| 1 | n8n basics: nodes, triggers, data flow, credentials | `01_beginner_workflow.json` | 3h | Assignment 1 |
| 2 | Email automation (IMAP → classify → route → reply) | `02_email_automation.json` | 3h | Assignment 2 |
| 3 | Lead qualification (webhook → AI score → CRM) | `03_lead_qualification.json` | 4h | Assignment 3 |
| 4 | AI Agents in n8n + CRM automation | `04_ai_agent_workflow.json`, `05_crm_automation.json` | 4h | Assignments 4-5 |
| 5 | WhatsApp + Multi-agent workflows | `06_whatsapp_automation.json`, `07_multi_agent_workflow.json` | 4h | Assignments 6-7 |

## Setup (Day 0)
```bash
# Self-host n8n with Docker:
docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
# Then open http://localhost:5678  (or use n8n Cloud)
```
Create credentials in n8n's **Credentials** store for: Anthropic, IMAP/SMTP, Airtable/HubSpot,
WhatsApp (as needed). Never put keys in node fields.

## Model note
LLM nodes use Anthropic `claude-opus-4-8` (swap per node; `claude-fable-5` is the most capable).

## Assessment
- 7 assignments (build + export workflows) — see `assignments/week05_assignments.md`
- Reference exports — see `workflows/`
- End-of-week quiz from `../interview-prep/week05_n8n_questions.md`

## Success Criteria
By the end of Week 5, students can:
- Build n8n workflows with triggers, transforms, branching, and credentials
- Integrate LLMs into workflows for classification, scoring, drafting, and enrichment
- Build an AI Agent node with tools and memory
- Automate email, lead-qualification, CRM, and messaging processes
- Design a multi-agent workflow and reason about its cost/quality trade-offs
- Handle errors and keep secrets out of workflow JSON
