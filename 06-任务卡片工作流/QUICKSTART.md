# 🚀 3-Minute Quick Start

## Step 1: Clone & Init

```bash
git clone https://github.com/YOUR_USERNAME/cerebella-task-flow.git
cd cerebella-task-flow
bash SETUP/init.sh ~/my-project/task-cards
```

## Step 2: Tell your AI about it

Copy the content of `AI-INTEGRATION/SYSTEM-PROMPT.md` to your AI.

**Hermes**: paste into personality config
**Claude Code**: paste into CLAUDE.md
**Any AI**: paste as first instruction in chat

## Step 3: Create your first card

```bash
cp PROTOCOL/card-template.md task-cards/cards/active/TFC-001-first-task.md
# Edit TFC-001-first-task.md with your task details
```

## Step 4: Verify

```bash
bash SETUP/verify.sh
```

## You're ready.

Ask your AI: "What am I working on?" — it will check HOT-INDEX and answer in <1s.
