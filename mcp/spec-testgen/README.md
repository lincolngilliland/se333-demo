# Spec TestGen MCP Extension

This extension adds specification-based test generation to your testing agent.
It addresses a real workflow gap: boundary and equivalence-case design is often
manual, inconsistent, and hard to scale.

## What It Solves

- Finds boundary-value cases systematically (min-1, min, min+1, max-1, max, max+1)
- Builds equivalence partitions (valid and invalid classes)
- Generates deterministic, reviewable JUnit 5 test code from the same spec
- Produces machine-readable output for iteration metrics and coverage loops

## Tools

1. `spec_testgen_generate_cases`
- Input: `spec_json` (JSON string)
- Output: boundary matrix, equivalence partitions, generated case list

2. `spec_testgen_generate_junit5`
- Input: `spec_json`, `package_name`, `test_class_name`
- Output: generated JUnit 5 test source and metadata

## Quick Start

1. Install dependencies:

```bash
cd mcp/spec-testgen
python -m pip install -r requirements.txt
```

2. Register the server in workspace MCP config (`.vscode/mcp.json`):

```json
{
  "servers": {
    "spec-testgen": {
      "command": "python",
      "args": ["${workspaceFolder}/mcp/spec-testgen/server.py"]
    }
  }
}
```

3. Restart VS Code or reload MCP servers.

## Example Spec

Use `examples/visit-age-spec.json` as starter input.

## Example MCP Usage

### Generate cases

- Tool: `spec_testgen_generate_cases`
- Input: stringified JSON from `examples/visit-age-spec.json`

### Generate JUnit

- Tool: `spec_testgen_generate_junit5`
- Inputs:
  - `spec_json`: stringified spec
  - `package_name`: `org.springframework.samples.petclinic.owner`
  - `test_class_name`: `VisitServiceSpecGeneratedTests`

## Integration With Existing Test Loop

You can integrate this into `spring-petclinic/test-improvement-loop.ps1` by setting
`-TestGenerationCommand` to call your MCP-driven generation step before each iteration.

Suggested flow:
1. Generate spec cases and JUnit source
2. Write tests to `src/test/java/...`
3. Run `mvn test jacoco:report`
4. Parse coverage and iterate
5. Auto-commit and push iteration artifacts (already supported in the loop)

## Measurable Value Template

Track these metrics per iteration:

| iteration | target_method | generated_cases | new_tests_passed | line_delta | branch_delta | commit_sha |
|---|---|---:|---:|---:|---:|---|
| 1 | scheduleVisit | 12 | 12 | +1.3% | +2.4% | abc1234 |

Recommended acceptance checks:
- Increase branch coverage on targeted class by at least 5%
- Keep generated tests deterministic (0 flaky failures across 3 reruns)
- Preserve green build on full suite

## Notes

- This scaffold is intentionally conservative and deterministic.
- Extend type support and assertion generation rules as your domain evolves.
