import json
import re
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("spec-testgen")


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()


def _build_boundary_values(param: Dict[str, Any]) -> List[Dict[str, Any]]:
    values: List[Dict[str, Any]] = []
    name = param["name"]

    if "min" in param and "max" in param:
        min_v = param["min"]
        max_v = param["max"]
        values.extend(
            [
                {"parameter": name, "case": "below_min", "value": min_v - 1, "valid": False},
                {"parameter": name, "case": "at_min", "value": min_v, "valid": True},
                {"parameter": name, "case": "above_min", "value": min_v + 1, "valid": True},
                {"parameter": name, "case": "below_max", "value": max_v - 1, "valid": True},
                {"parameter": name, "case": "at_max", "value": max_v, "valid": True},
                {"parameter": name, "case": "above_max", "value": max_v + 1, "valid": False},
            ]
        )

    if param.get("nullable", False):
        values.append({"parameter": name, "case": "null", "value": None, "valid": False})

    if "enum" in param:
        enum_values = param["enum"]
        if enum_values:
            values.append(
                {
                    "parameter": name,
                    "case": "enum_valid",
                    "value": enum_values[0],
                    "valid": True,
                }
            )
            values.append(
                {
                    "parameter": name,
                    "case": "enum_invalid",
                    "value": "INVALID_ENUM_VALUE",
                    "valid": False,
                }
            )

    return values


def _build_equivalence_classes(param: Dict[str, Any]) -> List[Dict[str, Any]]:
    classes: List[Dict[str, Any]] = []
    name = param["name"]

    valid_examples = param.get("validExamples", [])
    invalid_examples = param.get("invalidExamples", [])

    if valid_examples:
        classes.append(
            {
                "parameter": name,
                "class": "valid",
                "representative": valid_examples[0],
                "valid": True,
            }
        )

    if invalid_examples:
        classes.append(
            {
                "parameter": name,
                "class": "invalid",
                "representative": invalid_examples[0],
                "valid": False,
            }
        )

    return classes


def _default_value_for_type(type_name: str) -> Any:
    lowered = type_name.lower()
    if lowered in {"int", "integer", "long", "short", "byte"}:
        return 1
    if lowered in {"double", "float", "decimal"}:
        return 1.0
    if lowered in {"boolean", "bool"}:
        return True
    if lowered in {"string", "charsequence"}:
        return "valid"
    return "sample"


def _java_literal(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace('"', '\\"')
    return f'"{escaped}"'


def _generate_cases(spec: Dict[str, Any]) -> Dict[str, Any]:
    parameters = spec.get("parameters", [])

    boundary_matrix: List[Dict[str, Any]] = []
    equivalence_partitions: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []

    baseline_input: Dict[str, Any] = {}
    for p in parameters:
        if p.get("validExamples"):
            baseline_input[p["name"]] = p["validExamples"][0]
        else:
            baseline_input[p["name"]] = _default_value_for_type(p.get("type", "string"))

    candidates.append(
        {
            "id": "valid_baseline",
            "description": "All parameters use representative valid values.",
            "inputs": baseline_input,
            "expected": spec.get("expected", {}).get("validOutcome", "success"),
            "valid": True,
        }
    )

    for p in parameters:
        boundary_rows = _build_boundary_values(p)
        partition_rows = _build_equivalence_classes(p)

        boundary_matrix.extend(boundary_rows)
        equivalence_partitions.extend(partition_rows)

        for row in boundary_rows + partition_rows:
            case_inputs = dict(baseline_input)
            case_inputs[p["name"]] = row["value"]
            candidates.append(
                {
                    "id": f"{_slug(p['name'])}_{_slug(row['case'])}",
                    "description": f"{p['name']} => {row['case']}",
                    "inputs": case_inputs,
                    "expected": spec.get("expected", {}).get(
                        "validOutcome" if row["valid"] else "invalidOutcome",
                        "success" if row["valid"] else "validation_error",
                    ),
                    "valid": row["valid"],
                }
            )

    return {
        "targetClass": spec.get("targetClass"),
        "method": spec.get("method"),
        "boundaryMatrix": boundary_matrix,
        "equivalencePartitions": equivalence_partitions,
        "cases": candidates,
    }


def _render_junit5(spec: Dict[str, Any], generated: Dict[str, Any], package_name: str, test_class_name: str) -> str:
    method = spec["method"]
    target_class = spec["targetClass"]
    params = spec.get("parameters", [])

    lines: List[str] = []
    lines.append(f"package {package_name};")
    lines.append("")
    lines.append("import org.junit.jupiter.api.Test;")
    lines.append("import static org.assertj.core.api.Assertions.assertThatCode;")
    lines.append("import static org.assertj.core.api.Assertions.assertThatThrownBy;")
    lines.append("")
    lines.append(f"class {test_class_name} {{")
    lines.append("")
    lines.append(f"    private final {target_class} subject = new {target_class}();")
    lines.append("")

    for case in generated["cases"]:
        test_name = f"test_{_slug(method)}_{_slug(case['id'])}"
        args: List[str] = []
        for p in params:
            args.append(_java_literal(case["inputs"].get(p["name"])))
        invocation = f"subject.{method}({', '.join(args)})"

        lines.append("    @Test")
        lines.append(f"    void {test_name}() {{")
        if case["valid"]:
            lines.append(f"        assertThatCode(() -> {invocation}).doesNotThrowAnyException();")
        else:
            lines.append(f"        assertThatThrownBy(() -> {invocation}).isInstanceOf(Exception.class);")
        lines.append("    }")
        lines.append("")

    lines.append("}")
    return "\n".join(lines)


@mcp.tool()
def spec_testgen_generate_cases(spec_json: str) -> Dict[str, Any]:
    """Generate boundary-value and equivalence-class test cases from a JSON spec."""
    spec = json.loads(spec_json)
    return _generate_cases(spec)


@mcp.tool()
def spec_testgen_generate_junit5(
    spec_json: str,
    package_name: str,
    test_class_name: str,
) -> Dict[str, Any]:
    """Generate JUnit 5 test source from a JSON spec."""
    spec = json.loads(spec_json)
    generated = _generate_cases(spec)
    source = _render_junit5(spec, generated, package_name, test_class_name)
    return {
        "targetClass": spec.get("targetClass"),
        "method": spec.get("method"),
        "testClassName": test_class_name,
        "caseCount": len(generated["cases"]),
        "source": source,
    }


if __name__ == "__main__":
    mcp.run()
