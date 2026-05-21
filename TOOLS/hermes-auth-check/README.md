# 🔐 Hermes Auth Check

**检测并修复 Hermes Agent 凭据池中被截断的 API 密钥**
**Detect and fix truncated API keys in your Hermes Agent credential pool.**

---

## 这是什么 · What Is This

如果你遇到 **401 认证失败** 或 DeepSeek V4 的神秘 **400 错误**——真正的元凶可能不是 API bug，而是 **被污染的凭据池**。
If you're getting **401 auth failures** or mysterious **400 errors** with DeepSeek V4 — the real culprit might be a **poisoned credential pool**.

## 问题现象 · The Problem

Hermes Agent 默认启用 `security.redact_secrets: true`。当AI通过 `read_file()` 读取文件时，`redact_sensitive_text()` 会对所有输出进行脱敏处理——**包括 API 密钥**。
Hermes Agent has `security.redact_secrets: true` by default. When your AI reads files, `redact_sensitive_text()` applies to all output — **including API keys**.

```
sk-c25b3bd5a67d461790ecdc575fa2edd4   →   sk-c25...edd4
```

如果截断后的值被写回 `~/.hermes/auth.json` 凭据池，池中存储的就是无效密钥 → API收到截断密钥 → **401认证失败** → 触发跨供应商回滚循环 → 看起来像是 DeepSeek 的 API bug。
If the truncated value gets written to the credential pool, the pool stores an invalid key → 401 auth failure → cross-provider fallback loop → looks like a DeepSeek API bug.

## 检测 · Detection

```bash
hermes-auth-check
```

输出示例 Sample output:
```
  🔐 Hermes Auth Check — Credential Pool Audit
  Total entries:  4  |  Healthy:  3  |  Poisoned:  1
```

## 修复 · Fix

The tool automatically removes poisoned entries. 该工具会自动移除被污染的凭据条目。

```bash
hermes-auth-check --fix
```

## License

MIT


---

# 🔐 Hermes Auth Check

**Detect and fix truncated API keys in your Hermes Agent credential pool.**

If you're getting **401 auth failures** or mysterious **"reasoning_content must be passed back" 400 errors** with DeepSeek V4 — the real culprit might be a **poisoned credential pool**, not the reasoning content bug.

## The Problem

Hermes Agent has `security.redact_secrets: true` by default. When your AI agent reads files via `read_file()` or `search_files()`, the `file_tools.py` layer applies `redact_sensitive_text()` to all output — **including API keys**.

```
sk-c25b3bd5a67d461790ecdc575fa2edd4   →   sk-c25...edd4
                                         (literal '...' bytes in the file!)
```

If the truncated value gets written to `~/.hermes/auth.json` credential pool, the pool stores `sk-c25...edd4` (13 chars with literal `...` bytes). On credential restore, the API receives a truncated key → **401 auth failure** → which triggers a **cross-provider fallback loop** that looks identical to the reasoning_content 400 error.

Many users misdiagnose this as a DeepSeek API bug.

## Detection

```bash
hermes-auth-check
```

Sample output:
```
────────────────────────────────────────────────────────────
  🔐 Hermes Auth Check — Credential Pool Audit
────────────────────────────────────────────────────────────

  Total entries:  4
  Healthy:        3
  Poisoned:       1

  ⚠ custom:deepseek-v4-flash  (2 entries, 1 poisoned)

    ✓  source=model_config  len=35  token=sk-c25...edd4

    │
    ✗ POISONED  source=config:deepseek-v4-flash  len=13  token=sk-c25...edd4
    │  → This key has literal '...' bytes in auth.json
    │  → Will cause 401 auth failures on credential restore
```

## Fix

```bash
# Dry run — see what would be removed
hermes-auth-check --fix --dry-run

# Apply the fix
hermes-auth-check --fix
```

This removes poisoned credential pool entries. The pool re-seeds from the correct key in `config.yaml` on next load.

## Install

```bash
curl -sL https://github.com/gymaira1990-jpg/hermes-auth-check/releases/latest/download/hermes-auth-check \
  -o /usr/local/bin/hermes-auth-check && chmod +x /usr/local/bin/hermes-auth-check
```

Or just copy the script anywhere in your `$PATH`.

## Usage

```
usage: hermes-auth-check [-h] [--path PATH] [--fix] [--dry-run] [--verbose] [--json]

  -h, --help            show this help message
  -p, --path PATH       path to auth.json (default: ~/.hermes/auth.json)
  --fix                 remove poisoned entries from auth.json
  -n, --dry-run         preview fix without modifying files
  -v, --verbose         show detailed entry information
  --json                output results as JSON (for programmatic use)
```

## Upstream Fix

This diagnostic tool is a companion to the upstream code fix in:

➡ **[NousResearch/hermes-agent#16174](https://github.com/NousResearch/hermes-agent/pull/16174)**

Two guards were added to `agent/credential_pool.py`:
1. `PooledCredential.from_dict()` — rejects access tokens with literal `...` + len < 35
2. `_seed_custom_pool()` — skips truncated keys in `custom_providers` config entries

## License

MIT
