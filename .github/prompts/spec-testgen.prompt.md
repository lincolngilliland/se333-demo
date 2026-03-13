---
name: spec-testgen
description: "Generate boundary-value and equivalence-class tests from a method specification using the local Spec TestGen MCP tool."
agent: agent
---

Use the local `spec-testgen` MCP server tools to generate tests from a method specification.

Workflow:
1. Read a JSON spec (method contract, constraints, examples).
2. Call `spec_testgen_generate_cases` and summarize:
- boundary matrix
- equivalence partitions
- generated cases
3. Call `spec_testgen_generate_junit5` to generate deterministic JUnit 5 test source.
4. Write the generated test class to the appropriate package under `src/test/java`.
5. Run tests and coverage.
6. Report measurable impact:
- tests added
- pass/fail
- line and branch coverage delta

Output format:
- Target: <class>#<method>
- Cases generated: <n>
- Boundary coverage summary: <short>
- Equivalence coverage summary: <short>
- Test file: <path>
- Validation: <pass/fail>
- Coverage delta: line <x%>, branch <y%>
