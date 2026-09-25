"""Small dependency-free validator for the JSON Schema subset used by this skill."""
from __future__ import annotations

from typing import Any


def _resolve(root: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported external ref: {ref}")
    value: Any = root
    for part in ref[2:].split("/"):
        value = value[part.replace("~1", "/").replace("~0", "~")]
    return value


def _matches_type(value: Any, expected: str) -> bool:
    checks = {
        "null": lambda x: x is None,
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str),
        "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
        "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        "boolean": lambda x: isinstance(x, bool),
    }
    return expected in checks and checks[expected](value)


def validate_instance(instance: Any, schema: dict) -> list[str]:
    errors: list[str] = []

    def walk(value: Any, rule: dict, path: str) -> None:
        if "$ref" in rule:
            walk(value, _resolve(schema, rule["$ref"]), path)
            return
        if "oneOf" in rule:
            matches = 0
            collected: list[list[str]] = []
            for option in rule["oneOf"]:
                before = len(errors)
                walk(value, option, path)
                option_errors = errors[before:]
                del errors[before:]
                collected.append(option_errors)
                if not option_errors:
                    matches += 1
            if matches != 1:
                errors.append(f"{path}: expected exactly one oneOf match; found {matches}")
            return

        expected = rule.get("type")
        if expected is not None:
            types = expected if isinstance(expected, list) else [expected]
            if not any(_matches_type(value, kind) for kind in types):
                errors.append(f"{path}: expected type {types}; found {type(value).__name__}")
                return

        if "enum" in rule and value not in rule["enum"]:
            errors.append(f"{path}: value {value!r} is not in enum")

        if isinstance(value, dict):
            properties = rule.get("properties", {})
            for key in rule.get("required", []):
                if key not in value:
                    errors.append(f"{path}: missing required property {key}")
            if rule.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        errors.append(f"{path}: unexpected property {key}")
            for key, child in value.items():
                if key in properties:
                    walk(child, properties[key], f"{path}.{key}")

        if isinstance(value, list):
            if len(value) < rule.get("minItems", 0):
                errors.append(f"{path}: fewer than minItems")
            if "maxItems" in rule and len(value) > rule["maxItems"]:
                errors.append(f"{path}: more than maxItems")
            if rule.get("uniqueItems"):
                serialized = [repr(item) for item in value]
                if len(serialized) != len(set(serialized)):
                    errors.append(f"{path}: items are not unique")
            item_rule = rule.get("items")
            if item_rule:
                for index, child in enumerate(value):
                    walk(child, item_rule, f"{path}[{index}]")

        if isinstance(value, str):
            if len(value) < rule.get("minLength", 0):
                errors.append(f"{path}: shorter than minLength")
            if "maxLength" in rule and len(value) > rule["maxLength"]:
                errors.append(f"{path}: longer than maxLength")

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in rule and value < rule["minimum"]:
                errors.append(f"{path}: below minimum")
            if "maximum" in rule and value > rule["maximum"]:
                errors.append(f"{path}: above maximum")

    walk(instance, schema, "$")
    return errors
