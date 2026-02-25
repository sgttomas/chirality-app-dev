# POLICY RULING — DEL-03-05 Unsupported Image-Subtype Coverage Saturation (2026-02-23)

## Decision

Unsupported image-subtype boundary expansion for DEL-03-05 is ruled **coverage-saturated** at PASS35.

## Scope

- Deliverable: `DEL-03-05_Anthropic_Provider_Integration`
- Requirement focus: `REQ-05` multimodal content-block formatting boundaries for unsupported resolver-provided `image/*` subtype tokens

## Operational Contract

1. Keep representative invariant coverage as the completion baseline for unsupported subtype behavior:
   - unsupported `image/*` token + image extension -> deterministic extension-derived supported image media type (`image/png`, `image/jpeg`, `image/gif`, `image/webp`)
   - unsupported `image/*` token + non-image extension -> explicit text fallback (no image-mapping drift)
2. Exhaustive subtype-by-subtype enumeration is not required for ongoing DEL-03-05 follow-through.
3. Additional subtype token additions require at least one of:
   - runtime behavior change affecting MIME authority/fallback logic
   - contract change in `Specification.md` / `Procedure.md`
   - explicit human re-ruling
4. WS-3 follow-through focus now shifts toward resolver-integrated interface behavior as DEL-04-01 matures.

## Rationale

Current runtime MIME-authority handling is whitelist-based for authoritative inline image types (`image/png`, `image/jpeg`, `image/gif`, `image/webp`). Unsupported subtypes share the same non-authoritative path, so incremental subtype enumeration beyond PASS35 has diminishing risk-reduction value relative to resolver-integrated coverage.
