"""
======================================================================
GER
S29-E6.2.1.1
Feature Audit
======================================================================

Objective
---------
Classify every feature contained in structural_atlas.csv and determine
whether it should participate in the geometric representation of the
Observable Space.

Outputs
-------
- geometric_feature_mask.csv
- feature_audit_report.txt
- scientific_certificate.json
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd


# ======================================================================
# PATHS
# ======================================================================

INPUT_ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")
INPUT_FILE = (
    INPUT_ROOT
    / "E6_1_16_StructuralAtlas"
    / "structural_atlas.csv"
)

ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")

OUT = ROOT / "E6_2_1_1_FeatureAudit"
OUT.mkdir(parents=True, exist_ok=True)


# ======================================================================
# BANNER
# ======================================================================

print("=" * 70)
print("GER")
print("S29-E6.2.1.1")
print("Feature Audit")
print("=" * 70)


# ======================================================================
# LOAD
# ======================================================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(INPUT_FILE)

atlas = pd.read_csv(INPUT_FILE)

print("[OK] structural_atlas.csv")
print()

print(f"Observables : {len(atlas)}")
print(f"Attributes  : {len(atlas.columns)}")
print()


# ======================================================================
# HELPERS
# ======================================================================

def semantic_type(series: pd.Series):
    """
    Automatic semantic classification.
    """

    values = series.dropna()

    unique = values.nunique()

    variance = None

    numeric = pd.api.types.is_numeric_dtype(values)

    if numeric:
        variance = float(values.var())

    # --------------------------------------------------------------

    if unique <= 1:
        return "Constant"

    # --------------------------------------------------------------

    if numeric:

        uniques = sorted(values.unique())

        if len(uniques) == 2:

            if set(uniques).issubset({0, 1, True, False}):
                return "Binary"

        if pd.api.types.is_float_dtype(values):
            return "Continuous"

        return "Discrete"

    return "Categorical"


def recommended(semantic):
    """
    Geometry recommendation.
    """

    if semantic == "Continuous":
        return True, "Continuous metric"

    if semantic == "Discrete":
        return True, "Quantitative attribute"

    if semantic == "Binary":
        return False, "Binary metadata"

    if semantic == "Categorical":
        return False, "Categorical label"

    if semantic == "Constant":
        return False, "Zero variance"

    return False, "Unknown"


# ======================================================================
# FEATURE AUDIT
# ======================================================================

records = []

for column in atlas.columns:

    s = atlas[column]

    sem = semantic_type(s)

    use, reason = recommended(sem)

    variance = (
        float(s.var())
        if pd.api.types.is_numeric_dtype(s)
        else np.nan
    )

    record = {

        "Feature": column,

        "DType": str(s.dtype),

        "SemanticType": sem,

        "UniqueValues": int(s.nunique()),

        "Variance": variance,

        "Constant": bool(s.nunique() <= 1),

        "RecommendedForGeometry": use,

        "Reason": reason,
    }

    records.append(record)

mask = pd.DataFrame(records)

# ======================================================================
# SUMMARY STATISTICS
# ======================================================================

total_features = len(mask)

continuous_features = int(
    (mask["SemanticType"] == "Continuous").sum()
)

discrete_features = int(
    (mask["SemanticType"] == "Discrete").sum()
)

binary_features = int(
    (mask["SemanticType"] == "Binary").sum()
)

categorical_features = int(
    (mask["SemanticType"] == "Categorical").sum()
)

constant_features = int(
    (mask["SemanticType"] == "Constant").sum()
)

accepted_features = int(
    mask["RecommendedForGeometry"].sum()
)

rejected_features = total_features - accepted_features


# ======================================================================
# SAVE FEATURE MASK
# ======================================================================

mask_file = OUT / "geometric_feature_mask.csv"

mask.sort_values(
    ["RecommendedForGeometry", "SemanticType", "Feature"],
    ascending=[False, True, True]
).to_csv(mask_file, index=False)


# ======================================================================
# REPORT
# ======================================================================

report_file = OUT / "feature_audit_report.txt"

with open(report_file, "w", encoding="utf-8") as f:

    f.write("=" * 70 + "\n")
    f.write("GER\n")
    f.write("S29-E6.2.1.1\n")
    f.write("Feature Audit Report\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Observables : {len(atlas)}\n")
    f.write(f"Attributes  : {total_features}\n\n")

    f.write("Semantic Classification\n")
    f.write("-----------------------\n")

    f.write(f"Continuous : {continuous_features}\n")
    f.write(f"Discrete   : {discrete_features}\n")
    f.write(f"Binary     : {binary_features}\n")
    f.write(f"Categorical: {categorical_features}\n")
    f.write(f"Constant   : {constant_features}\n\n")

    f.write("Geometry\n")
    f.write("--------\n")

    f.write(f"Accepted : {accepted_features}\n")
    f.write(f"Rejected : {rejected_features}\n\n")

    f.write("Detailed Classification\n")
    f.write("-----------------------\n\n")

    for _, row in mask.iterrows():

        status = (
            "YES"
            if row["RecommendedForGeometry"]
            else "NO"
        )

        f.write(f"{row['Feature']}\n")
        f.write(f"    DType      : {row['DType']}\n")
        f.write(f"    Semantic   : {row['SemanticType']}\n")
        f.write(f"    Variance   : {row['Variance']}\n")
        f.write(f"    Geometry   : {status}\n")
        f.write(f"    Reason     : {row['Reason']}\n\n")


# ======================================================================
# SCIENTIFIC CERTIFICATE
# ======================================================================

certificate = {

    "experiment": "S29-E6.2.1.1",

    "title": "Feature Audit",

    "observables": int(len(atlas)),

    "attributes": int(total_features),

    "continuous_features": continuous_features,

    "discrete_features": discrete_features,

    "binary_features": binary_features,

    "categorical_features": categorical_features,

    "constant_features": constant_features,

    "accepted_features": accepted_features,

    "rejected_features": rejected_features,

    "geometry_mask": "geometric_feature_mask.csv"

}

with open(
    OUT / "scientific_certificate.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        certificate,
        f,
        indent=4,
        ensure_ascii=False
    )


# ======================================================================
# FINAL REPORT
# ======================================================================

print("=" * 70)
print("Feature Audit Summary")
print("=" * 70)

print(f"Attributes            : {total_features}")
print(f"Continuous            : {continuous_features}")
print(f"Discrete              : {discrete_features}")
print(f"Binary                : {binary_features}")
print(f"Categorical           : {categorical_features}")
print(f"Constant              : {constant_features}")
print()

print(f"Accepted for Geometry : {accepted_features}")
print(f"Rejected              : {rejected_features}")
print()

print("=" * 70)
print("Experiment completed.")
print("Results saved to:")
print(OUT)
print("=" * 70)


# ======================================================================
# MAIN
# ======================================================================

def main():
    pass


if __name__ == "__main__":
    main()
