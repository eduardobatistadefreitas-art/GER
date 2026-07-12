#!/usr/bin/env python3
"""
=========================================================
GER TOOLS

Auditoria dos imports do CORE.

Confirma que nenhum arquivo do CORE depende
de GER_CORE.
=========================================================
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "GER" / "CORE"

errors = []

print("=" * 60)
print("CORE IMPORT AUDIT")
print("=" * 60)

for py in sorted(CORE.glob("*.py")):

    text = py.read_text(encoding="utf8")

    if "GER_CORE." in text:

        errors.append(py.name)

        print(f"[FAIL] {py.name}")

if not errors:

    print("Nenhum import antigo encontrado.")
    print()
    print("Resultado: OK")

else:

    print()
    print(f"Resultado: {len(errors)} arquivo(s) precisam de migração.")

print("=" * 60)
