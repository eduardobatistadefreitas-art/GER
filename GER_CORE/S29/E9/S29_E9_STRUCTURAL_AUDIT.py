"""
=============================================================
S29_E9_STRUCTURAL_AUDIT.py
Part 1 — Structural Scanner
=============================================================

GER Structural Audit

Scans every module inside

GER_CORE/S29/E9/

Collects

    • imports
    • classes
    • functions
    • public API
    • configuration references

No validation is performed in Part 1.

=============================================================
"""

from __future__ import annotations

import ast
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import List

# ============================================================
# Paths
# ============================================================

ROOT = Path(

    "/content/GER/GER_CORE/S29/E9"

)

OUTPUT = Path(

    "/content/drive/MyDrive/GER_RESULTS/S29_E9_AUDIT"

)

OUTPUT.mkdir(

    parents=True,
    exist_ok=True,

)

# ============================================================
# Expected Modules
# ============================================================

EXPECTED_MODULES = [

    "__init__",
    "config",
    "io",
    "models",
    "fitting",
    "selection",
    "statistics",
    "report",
    "dashboard",
    "run",

]

# ============================================================
# Data Structures
# ============================================================

@dataclass
class ImportRecord:

    module: str
    imported_module: str
    symbol: str
    line: int


@dataclass
class FunctionRecord:

    module: str
    function: str
    line: int


@dataclass
class ClassRecord:

    module: str
    cls: str
    line: int


@dataclass
class PublicAPIRecord:

    module: str
    symbol: str


@dataclass
class ConfigReference:

    module: str
    constant: str
    line: int


# ============================================================
# Containers
# ============================================================

IMPORTS: List[ImportRecord] = []

FUNCTIONS: List[FunctionRecord] = []

CLASSES: List[ClassRecord] = []

PUBLIC_API: List[PublicAPIRecord] = []

CONFIG_REFERENCES: List[ConfigReference] = []

# ============================================================
# CSV Helper
# ============================================================

def save_csv(

    filename,
    header,
    rows,

):

    with open(

        OUTPUT / filename,

        "w",

        newline="",

        encoding="utf-8",

    ) as f:

        writer = csv.writer(f)

        writer.writerow(header)

        writer.writerows(rows)

# ============================================================
# Module Scanner
# ============================================================

def scan_module(

    path: Path,

):

    module = path.stem

    source = path.read_text(

        encoding="utf-8"

    )

    tree = ast.parse(

        source

    )

    for node in ast.walk(tree):

        # ----------------------------------------------------
        # import xxx
        # ----------------------------------------------------

        if isinstance(

            node,
            ast.Import,

        ):

            for alias in node.names:

                IMPORTS.append(

                    ImportRecord(

                        module,

                        alias.name,

                        alias.name,

                        node.lineno,

                    )

                )

        # ----------------------------------------------------
        # from xxx import yyy
        # ----------------------------------------------------

        elif isinstance(

            node,
            ast.ImportFrom,

        ):

            origin = node.module or ""

            for alias in node.names:

                IMPORTS.append(

                    ImportRecord(

                        module,

                        origin,

                        alias.name,

                        node.lineno,

                    )

                )

        # ----------------------------------------------------
        # functions
        # ----------------------------------------------------

        elif isinstance(

            node,
            ast.FunctionDef,

        ):

            FUNCTIONS.append(

                FunctionRecord(

                    module,

                    node.name,

                    node.lineno,

                )

            )

        # ----------------------------------------------------
        # classes
        # ----------------------------------------------------

        elif isinstance(

            node,
            ast.ClassDef,

        ):

            CLASSES.append(

                ClassRecord(

                    module,

                    node.name,

                    node.lineno,

                )

            )

        # ----------------------------------------------------
        # __all__
        # ----------------------------------------------------

        elif isinstance(

            node,
            ast.Assign,

        ):

            for target in node.targets:

                if (

                    isinstance(

                        target,

                        ast.Name,

                    )

                    and target.id == "__all__"

                ):

                    if isinstance(

                        node.value,

                        ast.List,

                    ):

                        for elt in node.value.elts:

                            if isinstance(

                                elt,

                                ast.Constant,

                            ):

                                PUBLIC_API.append(

                                    PublicAPIRecord(

                                        module,

                                        elt.value,

                                    )

                                )

        # ----------------------------------------------------
        # CONFIG REFERENCES
        # ----------------------------------------------------

        elif isinstance(

            node,

            ast.Name,

        ):

            if (

                node.id.isupper()

            ):

                CONFIG_REFERENCES.append(

                    ConfigReference(

                        module,

                        node.id,

                        node.lineno,

                    )

                )

# ============================================================
# Scan Project
# ============================================================

def scan_project():

    print()

    print("=" * 70)

    print("GER STRUCTURAL AUDIT")

    print("PART 1 - SCANNING")

    print("=" * 70)

    print()

    for module in EXPECTED_MODULES:

        file = ROOT / f"{module}.py"

        if file.exists():

            print(

                f"[ OK ] {module}.py"

            )

            scan_module(

                file

            )

        else:

            print(

                f"[MISS] {module}.py"

            )

# ============================================================
# Export Inventory
# ============================================================

def export_inventory():

    save_csv(

        "imports.csv",

        [

            "module",
            "origin",
            "symbol",
            "line",

        ],

        [

            [

                r.module,
                r.imported_module,
                r.symbol,
                r.line,

            ]

            for r in IMPORTS

        ],

    )

    save_csv(

        "functions.csv",

        [

            "module",
            "function",
            "line",

        ],

        [

            [

                r.module,
                r.function,
                r.line,

            ]

            for r in FUNCTIONS

        ],

    )

    save_csv(

        "classes.csv",

        [

            "module",
            "class",
            "line",

        ],

        [

            [

                r.module,
                r.cls,
                r.line,

            ]

            for r in CLASSES

        ],

    )

    save_csv(

        "public_api.csv",

        [

            "module",
            "symbol",

        ],

        [

            [

                r.module,
                r.symbol,

            ]

            for r in PUBLIC_API

        ],

    )

    save_csv(

        "config_usage.csv",

        [

            "module",
            "constant",
            "line",

        ],

        [

            [

                r.module,
                r.constant,
                r.line,

            ]

            for r in CONFIG_REFERENCES

        ],

    )

# ============================================================
# Main
# ============================================================

def run():

    scan_project()

    export_inventory()

    print()

    print("=" * 70)

    print("PART 1 COMPLETED")

    print("=" * 70)

    print()

    print("Inventory exported to")

    print()

    print(OUTPUT)

    print()

if __name__ == "__main__":

    run()
