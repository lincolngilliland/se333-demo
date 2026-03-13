# se333-demo

## Overview

This repository contains an AI-assisted testing workflow built around MCP tools,
coverage-driven iteration, and Git traceability.

The project includes:

- a testing-agent prompt for iterative Java test improvement,
- GitHub MCP integration for repository and PR workflows,
- a local MCP extension for specification-based test generation,
- a starter Java application (`spring-petclinic`) used for demonstration.

## Main Components

### 1. Tester workflow

- [.github/prompts/tester.prompt.md](.github/prompts/tester.prompt.md)
- [spring-petclinic/test-improvement-loop.ps1](spring-petclinic/test-improvement-loop.ps1)

These files define and automate a test-improvement loop using:

- JaCoCo coverage parsing,
- repeated test generation and execution,
- Git commit/push traceability.

### 2. GitHub MCP integration

- [.vscode/mcp.json](.vscode/mcp.json)
- [.github/prompts/github-mcp-check.prompt.md](.github/prompts/github-mcp-check.prompt.md)

This enables GitHub-aware agent workflows such as repository discovery, branch workflows, and PR automation.

### 3. Spec TestGen MCP extension

- [mcp/spec-testgen/server.py](mcp/spec-testgen/server.py)
- [mcp/spec-testgen/README.md](mcp/spec-testgen/README.md)
- [.github/prompts/spec-testgen.prompt.md](.github/prompts/spec-testgen.prompt.md)

This extension generates boundary-value and equivalence-class test cases from a JSON method specification and can emit JUnit 5 test code.

## Quick Setup

### Prerequisites

- Git
- Python 3.10+
- Java 17+
- VS Code

### Install local extension

```bash
cd mcp/spec-testgen
python -m pip install -r requirements.txt
python server.py
```

Important:
- Run `python server.py` from `mcp/spec-testgen`, not the workspace root.

### Run starter project tests

```bash
cd spring-petclinic
./mvnw.cmd test
./mvnw.cmd jacoco:report
```

## Demo Artifacts

The project includes a concrete demo of specification-based generation in the starter repo:

- Demo class: [spring-petclinic/src/main/java/org/springframework/samples/petclinic/system/SpecDemoValidator.java](spring-petclinic/src/main/java/org/springframework/samples/petclinic/system/SpecDemoValidator.java)
- Generated test: [spring-petclinic/src/test/java/org/springframework/samples/petclinic/system/SpecDemoValidatorSpecGeneratedTests.java](spring-petclinic/src/test/java/org/springframework/samples/petclinic/system/SpecDemoValidatorSpecGeneratedTests.java)
- Demo spec: [mcp/spec-testgen/examples/spec-demo-validator-spec.json](mcp/spec-testgen/examples/spec-demo-validator-spec.json)

Measured class-level result from the demo:

- Line coverage: 0% to 100%
- Branch coverage: 0% to 85.71%
- Method coverage: 0% to 100%

## Documentation

- Extension-specific documentation: [mcp/spec-testgen/README.md](mcp/spec-testgen/README.md)
- Homework report / PDF-ready writeup: [HOMEWORK_REPORT.md](HOMEWORK_REPORT.md)

## Useful Commands

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