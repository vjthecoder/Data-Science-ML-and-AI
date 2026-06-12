# Week 5: AI Automation with n8n

## Learning Objectives
- Build no-code/low-code automation workflows in n8n
- Integrate LLMs into workflows as AI Agent nodes
- Automate common business processes: email, lead qualification, CRM, WhatsApp
- Design multi-agent automation workflows

## Estimated Duration
15-20 hours

## Prerequisites
- Week 3 (LLM basics, prompt engineering, tool calling)
- A running n8n instance (cloud or self-hosted via Docker)

## Modules
1. n8n Basics — nodes, triggers, workflows
2. Email Automation — IMAP trigger -> AI classification -> auto-reply
3. Lead Qualification — webhook -> LLM scoring -> CRM update
4. AI Agents in n8n — AI Agent node, tools, memory
5. CRM Automation — sync leads/contacts with HubSpot/Airtable
6. WhatsApp Automation — WhatsApp Business API integration
7. Multi-Agent Workflows — chained/branching agent workflows

## Theory Notes
See `workflows/README.md` for an explanation of each workflow's architecture and
import instructions.

## Workflow Exports (JSON)
- `workflows/01_beginner_workflow.json`
- `workflows/02_email_automation.json`
- `workflows/03_lead_qualification.json`
- `workflows/04_ai_agent_workflow.json`
- `workflows/05_crm_automation.json`
- `workflows/06_whatsapp_automation.json`
- `workflows/07_multi_agent_workflow.json`

## Mini Projects
- Auto-categorize and respond to support emails
- Lead qualification pipeline: form -> AI scoring -> CRM
- WhatsApp order-status assistant

## Real Industry Examples
- Sales ops: automatic lead enrichment and routing
- Support teams: auto-triage of inbound emails
- Marketing: AI-personalized WhatsApp follow-ups

## Assignments
See `assignments/`

## Interview Questions
See `../interview-prep/week05_n8n_questions.md`

## Common Mistakes
- Storing API keys directly in workflow JSON instead of n8n credentials
- No error-handling branches on HTTP/AI nodes
- Infinite loops in agent workflows without iteration limits

## Best Practices
- Use n8n credentials store for all secrets
- Add error workflows / try-catch nodes for production reliability
- Keep AI Agent prompts and tool lists version-controlled
- Test workflows with mock data before connecting live integrations

## Further Reading
- n8n official documentation
- n8n AI Agent node documentation
- WhatsApp Business Platform API docs
