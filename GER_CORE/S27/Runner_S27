"""
============================================================
GER

RUN ALL S27

Executa todos os módulos executáveis da Série S27.

============================================================
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

import pandas as pd


# ============================================================
# CONFIG
# ============================================================

INVENTORY = Path(
    "/content/drive/MyDrive/GER_RESULTS/S27_AUDIT/S27_inventory.csv"
)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT = Path(
    f"/content/drive/MyDrive/GER_RESULTS/S27_RUN_ALL/{TIMESTAMP}"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# LOAD INVENTORY
# ============================================================

df = pd.read_csv(INVENTORY)

df = df[
    (df["main()"] == True) |
    (df["__main__"] == True)
]

modules = []

for filename in df["file"]:

    if filename == "__init__.py":
        continue

    module = filename.replace(".py", "")

    modules.append(module)


print("=" * 60)
print("GER")
print("RUN ALL S27")
print("=" * 60)
print()

print("Modules detected :", len(modules))
print()


# ============================================================
# EXECUTION
# ============================================================

summary = []

pass_count = 0
fail_count = 0

global_start = time.perf_counter()

for module in modules:

    print(f"Running {module}")

    module_folder = OUTPUT / module

    module_folder.mkdir(
        exist_ok=True
    )

    start = time.perf_counter()

    process = subprocess.run(

        [

            sys.executable,

            "-m",

            f"GER_CORE.S27.{module}"

        ],

        capture_output=True,

        text=True,

    )

    elapsed = time.perf_counter() - start

    stdout = process.stdout

    stderr = process.stderr

    (module_folder / "stdout.txt").write_text(
        stdout,
        encoding="utf-8",
    )

    (module_folder / "stderr.txt").write_text(
        stderr,
        encoding="utf-8",
    )

    metadata = {

        "module": module,

        "status":
            "PASS"
            if process.returncode == 0
            else "FAIL",

        "return_code": process.returncode,

        "execution_time": elapsed,

        "stdout_lines":
            len(stdout.splitlines()),

        "stderr_lines":
            len(stderr.splitlines()),

    }

    with open(
        module_folder / "metadata.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False,
        )

    summary.append(metadata)

    if process.returncode == 0:

        pass_count += 1

        print("PASS")

    else:

        fail_count += 1

        print("FAIL")


# ============================================================
# SAVE SUMMARY
# ============================================================

summary_df = pd.DataFrame(summary)

summary_df.to_csv(

    OUTPUT / "summary.csv",

    index=False,

)

summary_df.to_json(

    OUTPUT / "summary.json",

    orient="records",

    indent=4,

)

total_time = time.perf_counter() - global_start

with open(

    OUTPUT / "summary.txt",

    "w",

    encoding="utf-8",

) as f:

    f.write("=" * 60 + "\n")
    f.write("GER\n")
    f.write("RUN ALL S27\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Modules : {len(modules)}\n")
    f.write(f"PASS    : {pass_count}\n")
    f.write(f"FAIL    : {fail_count}\n")
    f.write(f"Time(s) : {total_time:.2f}\n")


print()
print("=" * 60)
print("FINISHED")
print("=" * 60)
print()

print("Modules :", len(modules))
print("PASS    :", pass_count)
print("FAIL    :", fail_count)
print()
print("Results saved to:")
print(OUTPUT)
