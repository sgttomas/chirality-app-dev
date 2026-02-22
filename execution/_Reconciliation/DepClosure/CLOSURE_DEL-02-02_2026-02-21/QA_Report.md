# QA Report -- CLOSURE_DEL-02-02_2026-02-21

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Dependencies.csv found | 1 |
| Dependencies.csv readable | 1 |
| Schema valid (v3.1) | 1 |
| Coverage | 100% |

## Schema Issues

None. The single Dependencies.csv in scope declares RegisterSchemaVersion=v3.1 and contains all 29 required columns.

## Column Validation Detail

The following v3.1 columns were verified present in DEL-02-02's Dependencies.csv:

1. RegisterSchemaVersion
2. DependencyID
3. FromPackageID
4. FromDeliverableID
5. FromDeliverableName
6. DependencyClass
7. AnchorType
8. Direction
9. DependencyType
10. TargetType
11. TargetPackageID
12. TargetDeliverableID
13. TargetRefID
14. TargetName
15. TargetLocation
16. Statement
17. EvidenceFile
18. SourceRef
19. EvidenceQuote
20. Explicitness
21. RequiredMaturity
22. ProposedMaturity
23. SatisfactionStatus
24. Confidence
25. Origin
26. FirstSeen
27. LastSeen
28. Status
29. Notes

All columns present. No missing, extra, or misordered columns detected.

## Direction Ambiguity

All 10 rows specify Direction=UPSTREAM. No UNKNOWN or missing direction values. No ambiguity flagging required for SCC analysis.

## Limits

- MAX_CYCLES=10000: not reached (0 cycles found).
- HUB_THRESHOLD=20: not reached (max degree=2).

## Scope Limitations

This is a single-deliverable run (SCOPE=DEL-02-02). Target nodes DEL-02-01 and DEL-01-01 appear in the graph as edge targets but their own Dependencies.csv files were not parsed. Therefore:

- Bidirectional pair detection is limited to edges declared in DEL-02-02's register only.
- Isolation status of target nodes cannot be determined.
- Cycle detection is limited to edges originating from DEL-02-02.

For full cross-deliverable closure analysis, run with SCOPE=ALL.
