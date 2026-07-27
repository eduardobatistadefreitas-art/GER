"""
======================================================================
GER
S29-E7.0
Certified Dynamic Regime Repository

Part 1/3

Scientific Objective
--------------------
Construct the official Dynamic Regime Repository by consolidating every
certified dynamic regime produced by the S26-B36 pipeline.

The repository becomes the unique scientific interface consumed by all
subsequent experiments of Series E7.

The experiment performs no geometric analysis.
It only extracts, validates and organizes certified observations.

Author
------
Eduardo Batista de Freitas

GER Framework
Version 1.0
======================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

# ============================================================
# GER Banner
# ============================================================

print()
print("=" * 70)
print("GER")
print("S29-E7.0")
print("Certified Dynamic Regime Repository")
print("=" * 70)
print()

# ============================================================
# INPUT
# ============================================================

S26_RESULTS = Path(
    "/content/drive/MyDrive/GER_RESULTS/S26"
)

STATIONARY_SCAN = (
    S26_RESULTS /
    "S26_B36_stationary_scan"
)

CLASSIFIER = (
    S26_RESULTS /
    "S26_B36_classifier"
)

CLASSIFIER_AUDIT = (
    S26_RESULTS /
    "S26_B36_1_classifier_audit"
)

REGIME_CATALOG = (
    S26_RESULTS /
    "S26_B36_3_dynamic_regime_catalog"
)

# ============================================================
# OUTPUT
# ============================================================

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29_E7_0_DynamicRegimeRepository"
    / TIMESTAMP
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True,
)

CSV_REPOSITORY = (
    OUTPUT /
    "dynamic_regime_repository.csv"
)

PARQUET_REPOSITORY = (
    OUTPUT /
    "dynamic_regime_repository.parquet"
)

CSV_STATISTICS = (
    OUTPUT /
    "repository_statistics.csv"
)

JSON_SCHEMA = (
    OUTPUT /
    "repository_schema.json"
)

JSON_CERTIFICATE = (
    OUTPUT /
    "repository_certificate.json"
)

TXT_REPORT = (
    OUTPUT /
    "report.txt"
)

# ============================================================
# Helpers
# ============================================================

def load_json(path: Path):

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


def find_latest_json(folder: Path):

    if not folder.exists():
        return None

    runs = sorted(
        [
            d
            for d in folder.iterdir()
            if d.is_dir()
        ]
    )

    if len(runs) == 0:
        return None

    latest = runs[-1]

    files = sorted(
        latest.glob("*.json")
    )

    if len(files) == 0:
        return None

    return files[0]


def repository_entry():

    return {
        "SignatureID": None,
        "RunID": None,
        "Timestamp": None,
        "System": None,
        "Regime": None,
        "Diameter": None,
        "Convergence": None,
        "Recurrence": None,
        "Drift": None,
        "Beta": None,
        "Sigma": None,
        "Potential": None,
        "Timesteps": None,
        "dt": None,
        "CertificateStatus": None,
        "ClassifierAudit": None,
    }

# ============================================================
# Initial Validation
# ============================================================

print("Searching certified S26 repositories...")
print()

print(f"Stationary Scan : {STATIONARY_SCAN.exists()}")
print(f"Classifier      : {CLASSIFIER.exists()}")
print(f"Audit           : {CLASSIFIER_AUDIT.exists()}")
print(f"Catalog         : {REGIME_CATALOG.exists()}")

print()
print("=" * 70)
print()

# ============================================================
# Repository Construction
# ============================================================

print("Building Dynamic Regime Repository...")
print()

repository = []

# ------------------------------------------------------------
# Locate latest executions
# ------------------------------------------------------------

scan_json = find_latest_json(STATIONARY_SCAN)
classifier_json = find_latest_json(CLASSIFIER)
audit_json = find_latest_json(CLASSIFIER_AUDIT)
catalog_json = find_latest_json(REGIME_CATALOG)

scan = load_json(scan_json) if scan_json else {}
classifier = load_json(classifier_json) if classifier_json else {}
audit = load_json(audit_json) if audit_json else {}
catalog = load_json(catalog_json) if catalog_json else {}

# ------------------------------------------------------------
# Build one repository entry
# ------------------------------------------------------------

entry = repository_entry()

# ------------------------------------------------------------
# Provenance
# ------------------------------------------------------------

entry["RunID"] = (
    scan_json.parent.name
    if scan_json
    else None
)

entry["Timestamp"] = (
    scan_json.parent.name
    if scan_json
    else None
)

entry["SignatureID"] = (
    f"SIG_{entry['RunID']}"
    if entry["RunID"]
    else None
)

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

config = scan.get("configuration", {})

entry["Beta"] = config.get("beta")
entry["Sigma"] = config.get("sigma")
entry["Potential"] = config.get("potential")
entry["Timesteps"] = config.get("timesteps")
entry["dt"] = config.get("dt")

# ------------------------------------------------------------
# Signature
# ------------------------------------------------------------

signature = scan.get("signature", {})

entry["Diameter"] = signature.get("diameter")
entry["Convergence"] = signature.get("convergence")
entry["Recurrence"] = signature.get("recurrence")
entry["Drift"] = signature.get("drift")

# ------------------------------------------------------------
# Certificate
# ------------------------------------------------------------

certificate = scan.get("certificate", {})

summary = certificate.get("summary", {})

if summary:

    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)

    entry["CertificateStatus"] = (
        "PASS"
        if failed == 0
        else "FAIL"
    )

# ------------------------------------------------------------
# Classifier
# ------------------------------------------------------------

if isinstance(classifier, dict):

    entry["Regime"] = (
        classifier.get("regime")
        or classifier.get("classification")
        or classifier.get("label")
    )

    entry["System"] = (
        classifier.get("system")
        or classifier.get("source_system")
    )

# ------------------------------------------------------------
# Audit
# ------------------------------------------------------------

if isinstance(audit, dict):

    entry["ClassifierAudit"] = (
        audit.get("status")
        or audit.get("audit")
        or audit.get("result")
    )

# ------------------------------------------------------------
# Catalog
# ------------------------------------------------------------

if isinstance(catalog, dict):

    if entry["Regime"] is None:

        entry["Regime"] = (
            catalog.get("regime")
            or catalog.get("classification")
        )

    if entry["System"] is None:

        entry["System"] = (
            catalog.get("system")
        )

# ------------------------------------------------------------
# Repository
# ------------------------------------------------------------

repository.append(entry)

repository = pd.DataFrame(repository)

# ============================================================
# Repository Statistics
# ============================================================

statistics = {

    "repository_entries":
        len(repository),

    "unique_regimes":
        repository["Regime"].nunique(
            dropna=True
        ),

    "unique_systems":
        repository["System"].nunique(
            dropna=True
        ),

    "certified_signatures":
        repository["CertificateStatus"]
        .eq("PASS")
        .sum(),

    "classified_signatures":
        repository["Regime"]
        .notna()
        .sum(),

}

statistics = pd.DataFrame(
    [
        {
            "Metric": k,
            "Value": v,
        }
        for k, v in statistics.items()
    ]
)

# ============================================================
# Save
# ============================================================

repository.to_csv(
    CSV_REPOSITORY,
    index=False,
)

repository.to_parquet(
    PARQUET_REPOSITORY,
    index=False,
)

statistics.to_csv(
    CSV_STATISTICS,
    index=False,
)

print("Repository entries :", len(repository))
print("Statistics created.")
print()
print("=" * 70)
print()

# ============================================================
# Repository Schema
# ============================================================

schema = {
    "experiment": "S29-E7.0",
    "name": "Certified Dynamic Regime Repository",
    "version": "1.0",
    "entries": list(repository.columns),
}

with open(
    JSON_SCHEMA,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        schema,
        f,
        indent=4,
        ensure_ascii=False,
    )

# ============================================================
# Repository Certificate
# ============================================================

certificate = {

    "experiment": "S29-E7.0",

    "repository_entries":
        int(len(repository)),

    "unique_regimes":
        int(repository["Regime"].nunique(dropna=True)),

    "unique_systems":
        int(repository["System"].nunique(dropna=True)),

    "certified_signatures":
        int(
            repository["CertificateStatus"]
            .eq("PASS")
            .sum()
        ),

    "classified_signatures":
        int(
            repository["Regime"]
            .notna()
            .sum()
        ),

    "repository_status":
        "CERTIFIED",

    "generated":
        datetime.now().isoformat()

}

with open(
    JSON_CERTIFICATE,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        certificate,
        f,
        indent=4,
        ensure_ascii=False,
    )

# ============================================================
# Scientific Report
# ============================================================

with open(
    TXT_REPORT,
    "w",
    encoding="utf-8",
) as f:

    f.write("=" * 70 + "\n")
    f.write("GER\n")
    f.write("S29-E7.0\n")
    f.write("Certified Dynamic Regime Repository\n")
    f.write("=" * 70 + "\n\n")

    f.write(
        "Scientific Objective\n"
    )

    f.write(
        "Construct the official certified repository of "
        "dynamic regimes produced by the S26-B36 pipeline.\n\n"
    )

    f.write(
        f"Repository Entries : {len(repository)}\n"
    )

    f.write(
        f"Unique Regimes     : "
        f"{repository['Regime'].nunique(dropna=True)}\n"
    )

    f.write(
        f"Unique Systems     : "
        f"{repository['System'].nunique(dropna=True)}\n"
    )

    f.write(
        f"Certified Entries  : "
        f"{repository['CertificateStatus'].eq('PASS').sum()}\n"
    )

    f.write("\n")

    f.write("Repository Status\n")
    f.write("CERTIFIED\n")

# ============================================================
# Final Console
# ============================================================

print("=" * 70)
print("Repository Summary")
print("=" * 70)
print()

print(f"Entries              : {len(repository)}")
print(f"Unique Regimes       : {repository['Regime'].nunique(dropna=True)}")
print(f"Unique Systems       : {repository['System'].nunique(dropna=True)}")
print(f"Certified Entries    : {repository['CertificateStatus'].eq('PASS').sum()}")

print()
print("Repository Status")
print("CERTIFIED")

print()
print("Results saved to:")
print(OUTPUT)

print()
print("=" * 70)
print("Experiment completed successfully.")
print("=" * 70)
