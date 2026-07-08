# Prompt Engineering Cheat Sheet

## Structure a prompt
```
SYSTEM: role + constraints + output format   ← stable, cacheable
FEW-SHOT: example input → example output      ← optional, locks format
USER: the task + context                       ← varies per request
```

## Techniques
| Technique | When | How |
|-----------|------|-----|
| Zero-shot | simple tasks | just ask clearly |
| Few-shot | need a specific format/label | show 2–5 input→output examples |
| Chain-of-thought | multi-step reasoning | "think step by step" or enable model thinking |
| Role/system prompt | control tone & behavior | set persona + constraints in `system` |
| Structured output | machine-readable result | request a JSON schema, not free text |

## Anthropic SDK (Claude) — basics
```python
import anthropic
client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY from env

resp = client.messages.create(
    model="claude-opus-4-8",             # capable default; claude-fable-5 = most capable
    max_tokens=1024,
    system="You are a concise assistant. Answer in one sentence.",
    messages=[{"role": "user", "content": "What is RAG?"}],
)
print(next(b.text for b in resp.content if b.type == "text"))
```

## Structured JSON output (Claude)
```python
resp = client.messages.create(
    model="claude-opus-4-8", max_tokens=512,
    messages=[{"role": "user", "content": "Extract: Jane, jane@x.com, Pro plan."}],
    output_config={"format": {"type": "json_schema", "schema": {
        "type": "object",
        "properties": {"name": {"type": "string"}, "email": {"type": "string"},
                        "plan": {"type": "string"}},
        "required": ["name", "email", "plan"], "additionalProperties": False,
    }}},
)
```

## Reasoning (adaptive thinking)
```python
resp = client.messages.create(
    model="claude-opus-4-8", max_tokens=2048,
    thinking={"type": "adaptive"},        # model decides how much to reason
    messages=[{"role": "user", "content": "Solve this multi-step problem…"}],
)
```

## Do / Don't
- ✅ State role, task, constraints, and output format explicitly.
- ✅ Use JSON schema / tool calling instead of regex on free text.
- ✅ Test prompts against an eval set; version them.
- ✅ Load API keys from the environment; never hardcode.
- ❌ Over-aggressive "CRITICAL: YOU MUST…" — modern models follow it too literally.
- ❌ Assuming one good-looking output means the prompt is reliable.

## Cost levers
- Fewer tokens (trim context), cheaper model tier for easy tasks, prompt caching for large
  fixed context, structured outputs (less ret/parse overhead), batch API for non-urgent jobs.
