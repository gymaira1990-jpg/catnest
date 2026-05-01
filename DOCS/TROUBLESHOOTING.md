# Troubleshooting

## AI doesn't know about the system

**Problem:** AI responds "I don't know what task cards are."

**Fix:** Re-copy SYSTEM-PROMPT.md into your AI's instructions. Verify with "What task tracking system are we using?"

## AI keeps using session_search instead of indexes

**Problem:** Slow responses, high token usage.

**Fix:** The AI's system prompt needs reinforcement. Add to your instructions:
"Remember: always grep tags before full-text search. Mechanical matching is free."

## AI tries to execute without asking you first

**Problem:** AI creates/modifies files without your confirmation.

**Fix:** Ensure the Plan Gate instructions are in the system prompt. Key line:
"Before any multi-step operation involving create/modify/delete/publish: output a plan → wait for user confirmation → only then execute."

## Index entries don't match card files

**Problem:** HOT-INDEX references TFC-001 but the card file is missing.

**Fix:** Find the card in cards/done/ or recreate from WARM-INDEX description. The indexes are the authoritative reference — card files should always exist.

## Tag search returns nothing

**Problem:** You know there's a card about X but grep finds nothing.

**Fix:** Check TAG-REGISTRY.md Merged table for aliases. Try searching by ID or date instead.
