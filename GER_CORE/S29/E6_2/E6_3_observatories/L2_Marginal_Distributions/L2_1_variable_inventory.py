"""
============================================================
GER
L2.1 Variable Inventory
============================================================

Scientific Objective
--------------------
Build the official inventory of variables present in the
Relational Signature dataset.

This observatory documents the structure of the dataset
without performing statistical inference, providing the
metadata foundation for all subsequent L2 observatories.

Outputs
-------
report/
    variable_inventory_report.txt

tables/
    variable_inventory.csv

json/
    variable_inventory.json

certificate/
    certificate.json
============================================================
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd

from GER.CORE.ger_repository import ExperimentStorage

from GER_CORE.S29.E6_2.io import (
    load_signatures,
)

TITLE = """
GER
L2.1 Variable Inventory
"""


# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    inventory = []

    numeric_variables = 0

    categorical_variables = 0

    complete_variables = 0

    variables_with_missing = 0

    total_observations = len(df)

    for column in df.columns:

        series = df[column]

        dtype = str(series.dtype)

        count = int(series.count())

        missing = int(series.isna().sum())

        missing_percent = (

            100.0 * missing / total_observations

            if total_observations > 0

            else 0.0

        )

        unique = int(series.nunique(dropna=True))

        is_numeric = pd.api.types.is_numeric_dtype(series)

        if is_numeric:

            variable_type = "Numeric"

            numeric_variables += 1

            minimum = float(series.min())

            maximum = float(series.max())

        else:

            variable_type = "Categorical"

            categorical_variables += 1

            minimum = ""

            maximum = ""

        if missing == 0:

            complete_variables += 1

        else:

            variables_with_missing += 1

        inventory.append(

            {

                "Variable": column,

                "Type": variable_type,

                "Dtype": dtype,

                "Count": count,

                "Missing": missing,

                "Missing (%)": missing_percent,

                "Unique": unique,

                "Min": minimum,

                "Max": maximum,

            }

        )

    inventory = pd.DataFrame(

        inventory,

    )

    summary = {

        "total_variables":
            len(df.columns),

        "numeric_variables":
            numeric_variables,

        "categorical_variables":
            categorical_variables,

        "total_observations":
            total_observations,

        "complete_variables":
            complete_variables,

        "variables_with_missing":
            variables_with_missing,

        "status":
            "PASS",

    }

    return {

        "summary": summary,

        "inventory": inventory,

    }


# ============================================================
# SAVE
# ============================================================

def save(
    storage: ExperimentStorage,
    result: dict,
):

    summary = result["summary"]

    storage.create_folder("report")
    storage.create_folder("tables")
    storage.create_folder("json")
    storage.create_folder("certificate")

    report_folder = storage.folder("report")
    tables_folder = storage.folder("tables")
    json_folder = storage.folder("json")
    certificate_folder = storage.folder("certificate")

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    result["inventory"].to_csv(

        tables_folder / "variable_inventory.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "variable_inventory.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            summary,

            f,

            indent=4,

        )

    # --------------------------------------------------------
    # CERTIFICATE
    # --------------------------------------------------------

    certificate = {

        "observatory": "L2.1",

        "title": "Variable Inventory",

        "total_variables":
            summary["total_variables"],

        "numeric_variables":
            summary["numeric_variables"],

        "categorical_variables":
            summary["categorical_variables"],

        "variables_with_missing":
            summary["variables_with_missing"],

        "status":
            summary["status"],

    }

    with open(

        certificate_folder / "certificate.json",

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4,

        )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report = f"""
============================================================
GER
L2.1 Variable Inventory
============================================================

Total Variables
{summary['total_variables']}

Numeric Variables
{summary['numeric_variables']}

Categorical Variables
{summary['categorical_variables']}

Complete Variables
{summary['complete_variables']}

Variables with Missing Values
{summary['variables_with_missing']}

Total Observations
{summary['total_observations']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "variable_inventory_report.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(report)

    print(report)


# ============================================================
# RUN
# ============================================================

def run():

    print("=" * 60)

    print(TITLE)

    print("=" * 60)

    print()

    storage = ExperimentStorage(

        experiment="S29_E6_2_L2_1",

        folders=[

            "report",

            "tables",

            "json",

            "certificate",

        ],

    )

    df = load_signatures()

    result = analyse(df)

    save(

        storage,

        result,

    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run()
