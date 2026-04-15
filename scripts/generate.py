"""Generate pydantic models from the AllToken OpenAPI specs.

Reads from a sibling ``../megaopenrouter/openapi/{chat,anthropic}.yml`` and writes to
``src/alltoken/generated/{chat,anthropic}.py``.

Requires ``datamodel-code-generator`` (install via ``pip install -e ".[dev]"``).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC_DIR = ROOT.parent / "megaopenrouter" / "openapi"
OUT_DIR = ROOT / "src" / "alltoken" / "generated"

SPECS = {
    "chat": SPEC_DIR / "chat.yml",
    "anthropic": SPEC_DIR / "anthropic.yml",
}


def main() -> int:
    if not SPEC_DIR.exists():
        print(f"[generate] ERROR: spec dir not found at {SPEC_DIR}", file=sys.stderr)
        print(
            "[generate] Clone megaopenrouter as a sibling: "
            "`git clone git@gitlab.53site.com:ai-innovation-lab/megaopenrouter.git ../megaopenrouter`",
            file=sys.stderr,
        )
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    init = OUT_DIR / "__init__.py"
    if not init.exists():
        init.touch()

    for name, spec in SPECS.items():
        if not spec.exists():
            print(f"[generate] ERROR: spec not found at {spec}", file=sys.stderr)
            return 1
        out = OUT_DIR / f"{name}.py"
        print(f"[generate] {spec.name} -> {out.relative_to(ROOT)}")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "datamodel_code_generator",
                "--input",
                str(spec),
                "--input-file-type",
                "openapi",
                "--output",
                str(out),
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--target-python-version",
                "3.10",
                "--use-standard-collections",
                "--use-union-operator",
                "--use-annotated",
                "--use-schema-description",
                "--use-field-description",
                "--use-default",
                "--snake-case-field",
                "--formatters",
                "ruff-format",
                "ruff-check",
            ],
            check=True,
        )

    print("[generate] Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
