# OI-002 Option B Proof Report — DEL-03-06

## Scope

- Deliverable: `DEL-03-06_Outbound_Network_Guardrails`
- Ruling under proof: OI-002 Option B (layered enforcement + repeatable verification)
- Required proof standard: 3 independent runs covering startup, session boot, turn execution, 10-minute idle window, and shutdown

## Execution Command

```bash
cd frontend && npm run proof:network-policy -- \
  --runs 3 \
  --idle-seconds 600 \
  --idle-sample-seconds 60 \
  --output-dir ../execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6
```

## Evidence Bundle

- Root: `execution/PKG-03_Harness_Runtime_Core/1_Working/DEL-03-06_Outbound_Network_Guardrails/Evidence/OI-002_PROOF_OPTIONB_2026-02-23_PASS6/`
- Aggregate summary:
  - `SUMMARY.md`
  - `summary.json`
- Per-run artifacts:
  - `run-01/`, `run-02/`, `run-03/`
  - each run includes `next.log`, `electron.log`, `session_create.json`, `session_boot.json`, `turn_events.json`, `turn_sse.txt`, `tcp_snapshots.ndjson`, `summary.json`

## Results

| Run | Scenario coverage complete | Blocked renderer diagnostics observed | Probe payload observed | Non-allowlisted outbound endpoints (TCP summary) | Verdict |
|---|---|---|---|---|---|
| run-01 | Yes | 1 | 1 | 0 | PASS |
| run-02 | Yes | 1 | 1 | 0 | PASS |
| run-03 | Yes | 1 | 1 | 0 | PASS |

Aggregate verdict from `summary.json`: `passed=true`, `failedRunCount=0`.

## Key Observations

1. Renderer egress policy blocked non-allowlisted host attempts (`example.com`) in all three runs with explicit `REQ-NET-001` diagnostics in `electron.log`.
2. Probe payloads in all three runs recorded:
   - blocked non-allowlisted request (`https://example.com/...`, `ok=false`)
   - allowlisted Anthropic request (`https://api.anthropic.com/v1/messages`, `ok=true`)
   - allowlisted loopback request (`http://127.0.0.1:3000/`, `ok=true`)
3. Session flow completed in all three runs with successful `process:exit` events from the turn pipeline.

## Remaining Caveat

- `CONF-002` (OCSP/CRL infrastructure traffic carve-out wording) remains unresolved in deliverable governance text. This proof run records no explicit non-allowlisted outbound TCP endpoints in snapshots, but final normative wording for infrastructure TLS exceptions is still pending human resolution.
