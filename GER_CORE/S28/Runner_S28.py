"""
=============================================================
RUN ALL S28
=============================================================

Executa automaticamente todos os experimentos da S28.

Lê:

    /content/drive/MyDrive/GER_RESULTS/
        S28_AUDIT/
            S28_inventory.csv

Executa todos os módulos com:

    main == True
    ou
    __main__ == True

Resultados:

/content/drive/MyDrive/GER_RESULTS/
    S28_RUN_ALL/
        <timestamp>/
            summary.csv
            summary.json
            summary.txt

            <modulo>/
                stdout.txt
                stderr.txt
                metadata.json

=============================================================
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys

from datetime import datetime
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

PROJECT_ROOT = Path("/content/GER")

RESULTS = Path("/content/drive/MyDrive/GER_RESULTS")

INVENTORY = RESULTS / "S28_AUDIT" / "S28_inventory.csv"

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT = RESULTS / "S28_RUN_ALL" / TIMESTAMP

OUTPUT.mkdir(parents=True, exist_ok=True)

# ==========================================================
# AMBIENTE
# ==========================================================

os.chdir(PROJECT_ROOT)

print("=" * 70)
print("RUN ALL S28")
print("=" * 70)
print(f"Project : {PROJECT_ROOT}")
print(f"Results : {RESULTS}")
print(f"Working : {Path.cwd()}")
print("=" * 70)
print()

# ==========================================================
# INVENTÁRIO
# ==========================================================

if not INVENTORY.exists():
    raise FileNotFoundError(INVENTORY)

modules = []

with INVENTORY.open(
    "r",
    encoding="utf-8",
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        if (
            row["main"] == "True"
            or row["__main__"] == "True"
        ):

            modules.append(row)

print(f"Modules detected : {len(modules)}")
print()

# ==========================================================
# EXECUÇÃO
# ==========================================================

summary = []

passed = 0
failed = 0

for i, item in enumerate(modules, start=1):

    module = item["module"]

    experiment = f"GER_CORE.S28.{module}"

    folder = OUTPUT / module.replace(".", "_")

    folder.mkdir(parents=True, exist_ok=True)

    print(f"[{i:02d}/{len(modules):02d}] {experiment}")

    result = subprocess.run(

        [
            sys.executable,
            "-m",
            experiment,
        ],

        cwd=PROJECT_ROOT,

        capture_output=True,

        text=True,

    )

    (folder / "stdout.txt").write_text(
        result.stdout,
        encoding="utf-8",
    )

    (folder / "stderr.txt").write_text(
        result.stderr,
        encoding="utf-8",
    )

    metadata = {

        "module": experiment,

        "returncode": result.returncode,

        "status": (
            "PASS"
            if result.returncode == 0
            else "FAIL"
        ),

    }

    (folder / "metadata.json").write_text(

        json.dumps(
            metadata,
            indent=4,
        ),

        encoding="utf-8",

    )

    if result.returncode == 0:

        passed += 1

        status = "PASS"

    else:

        failed += 1

        status = "FAIL"

    summary.append(

        {

            "module": experiment,

            "status": status,

            "returncode": result.returncode,

        }

    )

# ==========================================================
# SUMMARY CSV
# ==========================================================

with (OUTPUT / "summary.csv").open(

    "w",

    newline="",

    encoding="utf-8",

) as f:

    writer = csv.DictWriter(

        f,

        fieldnames=[

            "module",

            "status",

            "returncode",

        ],

    )

    writer.writeheader()

    writer.writerows(summary)

# ==========================================================
# SUMMARY JSON
# ==========================================================

(OUTPUT / "summary.json").write_text(

    json.dumps(

        summary,

        indent=4,

    ),

    encoding="utf-8",

)

# ==========================================================
# SUMMARY TXT
# ==========================================================

with (OUTPUT / "summary.txt").open(

    "w",

    encoding="utf-8",

) as f:

    f.write("=" * 70 + "\n")
    f.write("RUN ALL S28\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Modules detected : {len(modules)}\n")
    f.write(f"PASS             : {passed}\n")
    f.write(f"FAIL             : {failed}\n\n")

    for item in summary:

        f.write(
            f"{item['status']:<6} {item['module']}\n"
        )

# ==========================================================
# CONSOLE
# ==========================================================

print()
print("=" * 70)
print("EXECUTION FINISHED")
print("=" * 70)

print(f"Modules detected : {len(modules)}")
print(f"PASS             : {passed}")
print(f"FAIL             : {failed}")

print()
print("Results saved to:")
print(OUTPUT)
