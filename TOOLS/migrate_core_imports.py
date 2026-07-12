#!/usr/bin/env python3
"""
=========================================================
GER TOOLS

Migração automática de imports do CORE.

Arquitetura oficial:

GER/CORE      -> núcleo
GER_CORE      -> experimentos

O CORE nunca deve depender de GER_CORE.
=========================================================
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "GER" / "CORE"

OLD = "GER_CORE."
NEW = "GER.CORE."

files = 0
changes = 0

print("=" * 60)
print("CORE IMPORT MIGRATION")
print("=" * 60)

for py in sorted(CORE.glob("*.py")):

    text = py.read_text(encoding="utf8")

    n = text.count(OLD)

    if n:

        text = text.replace(OLD, NEW)

        py.write_text(text, encoding="utf8")

        files += 1
        changes += n

        print(f"[OK] {py.name} ({n} alteração(ões))")

print("-" * 60)
print(f"Arquivos modificados : {files}")
print(f"Imports atualizados  : {changes}")
print("=" * 60)
