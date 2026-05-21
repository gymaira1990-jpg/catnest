# INDEX-RULES · Search Protocol

```
Version: 1.0 | License: MIT
```

## Architecture

```
PROTOCOL/
├── HOT-INDEX.md       ≤10 entries, auto-loaded at session start
├── WARM-INDEX.md      ≤100 entries, on-demand grep
├── COLD-INDEX.md      ≤1,000 entries, compressed single-line
├── ARCHIVE-INDEX.md   unlimited, bare minimum
├── TAG-REGISTRY.md    auto-evolving tag dictionary
└── card-template.md   card file template

cards/active/   ← unfinished tasks (active/pending/in_progress)
cards/done/     ← finished tasks (completed/archived)
```

## Search Protocol (Tags First → Description Fallback)

```
1. HOT (in context, 0 token)
   a) grep tags → hit? read card → return
   b) semantic search descriptions → hit? read card → return

2. WARM (read file, grep)
   a) grep tags → hit? read card → return
   b) semantic search descriptions → hit? read card → return

3. COLD (read file, grep)
   a) grep tags → hit? read card → return
   b) semantic search → hit? read card → return

4. ARCHIVE (read file, grep)
   a) grep tags → hit? read card → return

5. All missed → "Expanded to cross-session search?"
```

## Plan Gate v2

Before ANY multi-step operation involving create/modify/delete/publish:

```
Gate 1: Keyword match (0 token)
  grep: create new init share publish upload deploy setup config
  Hit? → STOP → output plan → wait → execute

Gate 2: Behavior scoring (~200 token)
  Score ≥3 → STOP → output plan → wait → execute

Gate 3: Pre-publish review
  Files ready → show user → wait for OK → push
```

## Memory Compression

| Level | Description | Content |
|-------|------------|---------|
| Card file | unlimited | Full context + decisions |
| HOT | ≤300 chars | Who + what + why + state + next |
| WARM | ≤150 chars | Goal + key decisions + result |
| COLD | ≤60 chars | Task name + one-line result |
| ARCHIVE | none | ID + title + status + date + tags |

## Scoring

| Dimension | Weight | Score |
|-----------|--------|-------|
| Efficiency | 25% | /10 |
| Accuracy | 25% | /10 |
| Token Cost | 25% | /10 |
| Storage | 25% | /10 |
| **Total** | | **/40** |
