# SE333 Final Project Report

## AI-Assisted Test Engineering with MCP Extensions

## 1. Executive Summary

This project operationalizes an AI-assisted testing workflow using Model Context Protocol (MCP) tools, Git automation, and coverage-driven iteration in a Java codebase. The implementation includes:

- a configurable test-improvement loop for repeated test and coverage cycles,
- Git traceability practices with commit and push cadence for meaningful changes,
- GitHub MCP integration for repository and pull request workflows,
- one additional MCP extension: a specification-based test generator.

The extension demonstrates measurable value by generating structured boundary and equivalence-class test cases and producing JUnit 5 test code directly from a machine-readable method specification.

## 2. Project Objectives

The project goals were to:

1. Build an AI-guided automated test improvement pipeline.
2. Integrate MCP tools into a practical software workflow.
3. Ensure every meaningful AI-generated change is traceable and reviewable through Git.
4. Add one additional MCP extension that solves a real development challenge and provides measurable benefit.

## 3. Repository Structure

This workspace contains two Git repositories:

- `se333-demo` (workspace root): prompt, config, and MCP extension orchestration.
- `spring-petclinic` (nested): Java application used for test generation and coverage demonstration.

Key artifacts added or updated:

- `.github/prompts/tester.prompt.md`
- `.github/prompts/github-mcp-check.prompt.md`
- `.github/prompts/spec-testgen.prompt.md`
- `.vscode/mcp.json`
- `mcp/spec-testgen/server.py`
- `mcp/spec-testgen/requirements.txt`
- `mcp/spec-testgen/README.md`
- `mcp/spec-testgen/examples/visit-age-spec.json`
- `mcp/spec-testgen/examples/spec-demo-validator-spec.json`
- `spring-petclinic/test-improvement-loop.ps1`

## 4. Setup Instructions

### 4.1 Prerequisites

- Git
- Python 3.10+
- Java 17+
- Maven Wrapper support included in `spring-petclinic`
- VS Code with GitHub Copilot Agent mode enabled

### 4.2 Clone and open

```bash
git clone https://github.com/lincolngilliland/se333-demo.git
cd se333-demo
```

### 4.3 Configure GitHub MCP in VS Code

The workspace MCP config is in `.vscode/mcp.json`.

It includes:

1. Remote GitHub MCP server
2. Local spec-testgen server

If prompted in VS Code, authorize GitHub for MCP access.

### 4.4 Install and run local spec-testgen server

Important: run from the extension directory, not the workspace root.

```bash
cd mcp/spec-testgen
python -m pip install -r requirements.txt
python server.py
```

If `python server.py` is run from the repo root, it fails because the file path is wrong.

### 4.5 Build and test starter application

```bash
cd spring-petclinic
./mvnw.cmd test
./mvnw.cmd jacoco:report
```

## 5. Core Workflow Documentation

### 5.1 Tester Agent Prompt

The testing prompt defines an iterative workflow that includes:

- test generation,
- test execution,
- JaCoCo parsing,
- iteration strategy,
- bug exposure and fix loop,
- Git traceability requirements.

The workflow was extended to explicitly require:

- commit every meaningful improvement,
- push regularly to GitHub,
- apply subsequent phases equally: testing, iteration, CI, and metrics.

### 5.2 Automated Test Improvement Loop

`spring-petclinic/test-improvement-loop.ps1` supports repeated execution with:

- coverage thresholds,
- generation and failure-fix command hooks,
- per-iteration CSV and JSON output,
- optional auto-commit and auto-push.

Added Git features:

- `-AutoCommit`
- `-AutoPush`
- `-CommitScope`
- `-CommitMessagePrefix`

These ensure iteration-level progress is traceable.

### 5.3 Additional MCP Extension: Spec TestGen

The added MCP server provides two tools:

1. `spec_testgen_generate_cases`
   - Generates boundary-value and equivalence-class test cases from JSON specs.
2. `spec_testgen_generate_junit5`
   - Produces deterministic JUnit 5 test source from the same spec.

This addresses a real challenge: manually deriving complete boundary and equivalence tests is time-consuming and inconsistent.

## 6. Demonstration and Measurable Results

### 6.1 Demo target

Class introduced in starter repo:

- `spring-petclinic/src/main/java/org/springframework/samples/petclinic/system/SpecDemoValidator.java`

Generated test class:

- `spring-petclinic/src/test/java/org/springframework/samples/petclinic/system/SpecDemoValidatorSpecGeneratedTests.java`

### 6.2 Generated output

- Generated case count: 15
- Boundary rows: 8
- Equivalence rows: 6
- Generated tests executed: 15
- Failures: 0
- Errors: 0

### 6.3 Coverage delta (class-level)

Before generated tests:

- Line: 0% (0/8)
- Branch: 0% (0/14)
- Method: 0% (0/2)

After generated tests:

- Line: 100% (8/8)
- Branch: 85.71% (12/14)
- Method: 100% (2/2)

Measured improvement:

- Line: +100%
- Branch: +85.71%
- Method: +100%

## 7. Git and PR Traceability

All meaningful phases were committed and pushed.

PRs created:

- `se333-demo`: https://github.com/lincolngilliland/se333-demo/pull/3
- `spring-petclinic`: https://github.com/lincolngilliland/spring-petclinic/pull/1

This demonstrates reviewability and reproducibility in a trunk-based workflow.

## 8. How to Reproduce the Full Demo

1. Start local MCP extension server:

```bash
cd mcp/spec-testgen
python -m pip install -r requirements.txt
python server.py
```

2. In VS Code Agent mode, run the prompt:

- `.github/prompts/spec-testgen.prompt.md`

3. Use spec:

- `mcp/spec-testgen/examples/spec-demo-validator-spec.json`

4. Run starter tests and coverage:

```bash
cd spring-petclinic
./mvnw.cmd -q -Dtest=SpecDemoValidatorSpecGeneratedTests test
./mvnw.cmd jacoco:report -DskipTests
```

5. Compare class metrics in `target/site/jacoco/jacoco.xml`.

## 9. Reflection

### 9.1 What worked well

- Specification-first generation improved test design consistency.
- MCP tool integration reduced manual context switching.
- Iteration logging and Git automation made progress auditable.

### 9.2 Challenges encountered

- Running `python server.py` from the wrong directory caused startup errors.
- Tool schema mismatch where equivalence rows were missing a `value` field caused runtime errors.
- Mixed workspace with two repositories required careful commit scoping.

### 9.3 What I changed after learning

- Fixed schema mismatch in `server.py` so case generation and JUnit generation use a consistent shape.
- Added explicit Git traceability requirements to prompts and loop script.
- Added comprehensive docs and examples for reproducible usage.

### 9.4 Lessons learned

1. AI-generated tests are best when constrained by explicit specifications.
2. Coverage percentages alone are not enough; branch coverage and deterministic execution matter.
3. Git discipline is essential when AI can generate many rapid changes.

### 9.5 Future improvements

- Add richer assertion synthesis based on expected output contracts.
- Support more parameter types and cross-parameter constraints.
- Integrate CI workflow to automatically run spec generation and coverage checks per PR.

## 10. PDF Export Instructions

Export only this file to PDF.

1. Open `HOMEWORK_REPORT.md` in VS Code.
2. Open Markdown preview.
3. Use Print or Export to PDF.
4. Save as `SE333_Final_Report.pdf`.

## 11. Appendix: Useful Commands

```bash
# Root repo status
git -C . status

# Starter repo status
git -C spring-petclinic status

# Run generated demo tests
cd spring-petclinic
./mvnw.cmd -q -Dtest=SpecDemoValidatorSpecGeneratedTests test

# Generate JaCoCo report
./mvnw.cmd jacoco:report -DskipTests
```
