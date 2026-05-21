# AI Integration Guide

## Option 1: Hermes Agent

Add to `~/.hermes/config.yaml`:

```yaml
clarify:
  timeout: 86400  # Prevent auto-proceed

# In personality or system prompt, add SYSTEM-PROMPT.md content
```

Recommended: create a custom personality that includes the SYSTEM-PROMPT content.

## Option 2: Claude Code

Add to `CLAUDE.md` in your project root (copy SYSTEM-PROMPT.md content):

```markdown
# CLAUDE.md

_(paste SYSTEM-PROMPT.md content here)_
```

## Option 3: Any AI (ChatGPT, Gemini, etc.)

At the start of each conversation, paste SYSTEM-PROMPT.md content as the first message.

## Verify it's working

Ask your AI: "What task tracking system are we using?"
If it says "Cerebella Task Flow" or references the protocol → it's working.

Then ask: "What am I currently working on?"
If it reads HOT-INDEX.md and answers → fully integrated.
