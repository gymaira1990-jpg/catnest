# Changelog

## v1.0.0 (2026-05-01)

### Initial Release — C-level

**Core features:**
- 4-tier index: HOT / WARM / COLD / ARCHIVE
- Tag-first search protocol (mechanical before semantic)
- Memory compression ladder (full → 300 → 150 → 60 → bare)
- Auto-evolving tag dictionary (TAG-REGISTRY)

**Safety features:**
- Plan Gate v2: keywords + behavior scoring
- Pre-publish review gate (show before push)
- Self-evolving review mechanism (meta-layer)

**Tooling:**
- SETUP/init.sh — one-command project init
- SETUP/verify.sh — integrity check + self-test
- AI-INTEGRATION/SYSTEM-PROMPT.md — drop-in AI configuration
- DOCS/WALKTHROUGH.md — complete first-session example

**Performance targets:**
- Session start: ~200 tok fixed
- Most searches: 0 tok (tag grep)
- Worst case: ~5,500 tok (full pyramid traversal)
- vs baseline session_search: -95% time, -95% tokens
