"""
============================================================
GER
L1.13 Compression Potential Observatory
============================================================

Scientific Question
-------------------
What is the theoretical compression potential of the
observed Relational Signature dataset without loss of
statistical information?

Outputs
-------
report/
    compression_report.txt

tables/
    compression_metrics.csv

json/
    compression.json

certificate/
    certificate.json

============================================================
"""
from __future__ import annotations

import json
import numpy as np
import pandas as pd

from GER.CORE.ger_storage import ExperimentStorage

from ...io import load_signatures

from ...statistics.spectrum import (
    compute_frequency_table,
)

from ...statistics.descriptive import (
    compute_entropy,
)

from ...statistics.information import (
    compression_ratio,
    compression_gain,
    compression_efficiency,
    ideal_storage_bits,
    uniform_storage_bits,
    storage_saving,
)


TITLE = (
    "GER\n"
    "L1.13 Compression Potential Observatory"
)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_compression(
    gain: float,
) -> str:

    if gain >= 0.90:
        return "HIGH"

    if gain >= 0.60:
        return "MODERATE"

    return "LOW"


# ============================================================
# ANALYSIS
# ============================================================

def analyse(
    df: pd.DataFrame,
):

    frequency = compute_frequency_table(df)

    values = (
        frequency["Frequency"]
        .values
        .astype(float)
    )

    total_occurrences = int(
        values.sum()
    )

    unique_signatures = len(values)

    entropy_nats = compute_entropy(
        values,
        base="e",
    )

    entropy_bits = compute_entropy(
        values,
        base="bits",
    )

    ratio = compression_ratio(

        total_occurrences,

        unique_signatures,

    )

    gain = compression_gain(

        total_occurrences,

        unique_signatures,

    )

    efficiency = compression_efficiency(

        entropy_nats,

        unique_signatures,

        entropy_base="e",

    )

    ideal_bits = ideal_storage_bits(

        entropy_bits,

        total_occurrences,

    )

    fixed_bits = uniform_storage_bits(

        unique_signatures,

        total_occurrences,

    )

    saving = storage_saving(

        entropy_bits,

        unique_signatures,

    )

    metrics = pd.DataFrame(

        {

            "Metric": [

                "Compression Ratio",

                "Compression Gain",

                "Compression Efficiency",

                "Entropy (bits)",

                "Ideal Storage (bits)",

                "Uniform Storage (bits)",

                "Storage Saving",

            ],

            "Value": [

                ratio,

                gain,

                efficiency,

                entropy_bits,

                ideal_bits,

                fixed_bits,

                saving,

            ],

        }

    )

    summary = {

        "total_occurrences": total_occurrences,

        "unique_signatures": unique_signatures,

        "compression_ratio": ratio,

        "compression_gain": gain,

        "compression_efficiency": efficiency,

        "entropy_bits": entropy_bits,

        "ideal_storage_bits": ideal_bits,

        "uniform_storage_bits": fixed_bits,

        "storage_saving": saving,

        "compression": classify_compression(

            gain,

        ),

        "status": "PASS",

    }

    return {

        "summary": summary,

        "metrics": metrics,

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

    result["metrics"].to_csv(

        tables_folder / "compression_metrics.csv",

        index=False,

    )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    with open(

        json_folder / "compression.json",

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

        "observatory": "L1.13",

        "title": "Compression Potential Observatory",

        "compression_ratio":
            summary["compression_ratio"],

        "compression_gain":
            summary["compression_gain"],

        "compression_efficiency":
            summary["compression_efficiency"],

        "entropy_bits":
            summary["entropy_bits"],

        "ideal_storage_bits":
            summary["ideal_storage_bits"],

        "uniform_storage_bits":
            summary["uniform_storage_bits"],

        "storage_saving":
            summary["storage_saving"],

        "compression":
            summary["compression"],

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
L1.13 Compression Potential Observatory
============================================================

Total Occurrences
{summary['total_occurrences']}

Unique Signatures
{summary['unique_signatures']}

Compression Ratio
{summary['compression_ratio']:.6f}

Compression Gain
{summary['compression_gain']:.6f}

Compression Efficiency
{summary['compression_efficiency']:.6f}

Entropy (bits)
{summary['entropy_bits']:.6f}

Ideal Storage (bits)
{summary['ideal_storage_bits']:.2f}

Uniform Storage (bits)
{summary['uniform_storage_bits']:.2f}

Storage Saving
{summary['storage_saving']:.6f}

Compression
{summary['compression']}

Status
{summary['status']}

============================================================
"""

    with open(

        report_folder / "compression_report.txt",

        "w",

        encoding="utf-8",

    ) as f:

        f.write(report)

    print(report)


# ============================================================
# MAIN
# ============================================================

def run():

    storage = ExperimentStorage(

        experiment="S29_E6_2_L1_13",

        folders=[

            "report",

            "tables",

            "json",

            "certificate",

        ],

    )

    print("=" * 60)
    print(TITLE)
    print("=" * 60)

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
