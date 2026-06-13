# Week 5 Interview Questions: AI Automation with n8n

## n8n Fundamentals
1. What is n8n, and how does it compare to Zapier/Make and to writing code?
2. Explain triggers vs regular nodes. Name three trigger types.
3. How does data flow between nodes (items, `$json`, expressions)?
4. How does n8n handle multiple items — does a node run once or per item?
5. How are credentials managed in n8n, and why never put keys in node fields?

## Building Workflows
6. How do IF and Switch nodes differ? When would you use each?
7. What does the Code node let you do that built-in nodes don't?
8. How would you parse and validate an LLM's JSON output inside a workflow?
9. How do you test a webhook workflow locally?
10. How do you make a workflow run on a schedule?

## AI in Workflows
11. How do you add an LLM step to a workflow, and how do you pass it dynamic input?
12. What is the AI Agent node, and how do tools and memory attach to it?
13. Why might you choose an n8n AI Agent over hand-coding an agent in Python?
14. How would you keep an agent workflow from looping forever?

## Reliability & Security
15. How do you handle errors so a failed step doesn't silently drop data?
16. What's the purpose of an Error Trigger workflow?
17. Why should secrets never live in exported workflow JSON?
18. How would you make a messaging bot ignore its own outbound messages?

## Use Cases & Design
19. Design an email-triage automation: which nodes, in what order?
20. Design a lead-qualification pipeline from web form to CRM with an AI score.
21. When is a multi-agent workflow worth the extra LLM cost vs a single prompt?
22. How would you add human-in-the-loop approval before a workflow sends an external message?

## Scenario
23. A scheduled enrichment workflow occasionally double-processes records. What causes this and
    how do you make it idempotent?
24. Your auto-reply bot replied to a spam email and started a loop. Diagnose and fix.
25. Stakeholders want analytics on how many leads the workflow qualifies per week. How would you
    add that without changing the core flow?
