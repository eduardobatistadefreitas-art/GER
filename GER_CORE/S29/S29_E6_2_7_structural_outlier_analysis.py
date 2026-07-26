"""
============================================================
GER
S29-E6.2.7
STRUCTURAL OUTLIER ANALYSIS OF THE OBSERVABLE SPACE
============================================================

Objective
---------
Identify observables presenting exceptional geometric
behavior within the certified Observable Space.

Rather than applying arbitrary thresholds, this experiment
quantifies structural deviations using standardized geometric
descriptors derived from the certified stability profile.

The resulting anomaly scores provide an observational ranking
of structural singularities while preserving the neutrality
principle adopted throughout the GER framework.

Execution
---------
python -m GER_CORE.S29.S29_E6_2_7_structural_outlier_analysis

Author
------
Eduardo Batista de Freitas
GER Project
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd


# ============================================================
# INPUT
# ============================================================

PROFILE_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_6_StabilityAnalysis"
    / "stability_profile.csv"
)

SUMMARY_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_6_StabilityAnalysis"
    / "stability_summary.csv"
)

CERTIFICATE_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_6_StabilityAnalysis"
    / "stability_certificate.json"
)


# ============================================================
# OUTPUT
# ============================================================

OUT = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_7_StructuralOutlierAnalysis"
)

OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# Banner
# ============================================================

print("=" * 70)
print("GER")
print("S29-E6.2.7")
print("Structural Outlier Analysis of the Observable Space")
print("=" * 70)


# ============================================================
# Load
# ============================================================

profile = pd.read_csv(PROFILE_FILE)

summary = pd.read_csv(SUMMARY_FILE)

with open(
    CERTIFICATE_FILE,
    "r",
    encoding="utf-8"
) as f:

    certificate = json.load(f)

nucleus = certificate["geometric_nucleus"]

print("[OK] stability_profile.csv")
print("[OK] stability_summary.csv")
print("[OK] stability_certificate.json")

print()

print(f"Observables : {len(profile)}")
print(f"Geometric Nucleus : {nucleus}")

print()

# ============================================================
# Standardized Structural Deviations
# ============================================================

outliers = profile.copy()

distance = outliers["DistanceToNucleus"].to_numpy()

mean_distance = np.mean(distance)
std_distance = np.std(distance)

if std_distance > 0:

    outliers["DistanceZ"] = (
        outliers["DistanceToNucleus"] - mean_distance
    ) / std_distance

else:

    outliers["DistanceZ"] = 0.0


# ============================================================
# Relative Isolation
# ============================================================

max_distance = outliers["DistanceToNucleus"].max()

if max_distance > 0:

    outliers["RelativeIsolation"] = (
        outliers["DistanceToNucleus"] /
        max_distance
    )

else:

    outliers["RelativeIsolation"] = 0.0


# ============================================================
# Structural Deviation
# ============================================================

outliers["StructuralDeviation"] = np.abs(
    outliers["DistanceZ"]
)


# ============================================================
# Outlier Score
# ============================================================

outliers["OutlierScore"] = (

    outliers["StructuralDeviation"] +

    outliers["RelativeIsolation"]

) / 2.0


# ============================================================
# Ranking
# ============================================================

outliers = outliers.sort_values(

    "OutlierScore",

    ascending=False

).reset_index(drop=True)

outliers["OutlierRank"] = np.arange(
    1,
    len(outliers) + 1
)


# ============================================================
# Global Statistics
# ============================================================

mean_score = float(
    outliers["OutlierScore"].mean()
)

std_score = float(
    outliers["OutlierScore"].std(ddof=0)
)

max_score = float(
    outliers["OutlierScore"].max()
)

min_score = float(
    outliers["OutlierScore"].min()
)


# ============================================================
# Save Ranking
# ============================================================

outliers.to_csv(

    OUT / "outlier_profile.csv",

    index=False

)


# ============================================================
# Summary
# ============================================================

summary = pd.DataFrame({

    "Metric":[

        "MeanOutlierScore",
        "StdOutlierScore",
        "MaximumOutlierScore",
        "MinimumOutlierScore"

    ],

    "Value":[

        mean_score,
        std_score,
        max_score,
        min_score

    ]

})

summary.to_csv(

    OUT / "outlier_summary.csv",

    index=False

)


print("=" * 70)
print("Structural Outlier Summary")
print("=" * 70)

print(f"Geometric Nucleus      : {nucleus}")
print(f"Highest Score          : {max_score:.6f}")
print(f"Mean Score             : {mean_score:.6f}")
print(f"Lowest Score           : {min_score:.6f}")
print()

print("Top Structural Singularities")

for _, row in outliers.head(5).iterrows():

    print(
        f"{int(row['OutlierRank']):2d}  "
        f"{row['Observable']:<20}"
        f"{row['OutlierScore']:.6f}"
    )

print()

# ============================================================
# Scientific Certificate
# ============================================================

certificate = {

    "experiment": "S29-E6.2.7",

    "title": "Structural Outlier Analysis of the Observable Space",

    "geometric_nucleus": nucleus,

    "observables": int(len(outliers)),

    "highest_outlier_score": max_score,

    "lowest_outlier_score": min_score,

    "mean_outlier_score": mean_score,

    "std_outlier_score": std_score,

    "top_structural_outlier": outliers.iloc[0]["Observable"]

}

with open(

    OUT / "outlier_certificate.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        certificate,

        f,

        indent=4

    )


# ============================================================
# Scientific Report
# ============================================================

with open(

    OUT / "outlier_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("GER\n")
    f.write("S29-E6.2.7\n")
    f.write("Structural Outlier Analysis of the Observable Space\n")
    f.write("=" * 60 + "\n\n")

    f.write("Global Statistics\n")
    f.write("-----------------\n\n")

    f.write(f"Geometric Nucleus      : {nucleus}\n")
    f.write(f"Observables            : {len(outliers)}\n")
    f.write(f"Highest Score          : {max_score:.6f}\n")
    f.write(f"Mean Score             : {mean_score:.6f}\n")
    f.write(f"Std Score              : {std_score:.6f}\n")
    f.write(f"Lowest Score           : {min_score:.6f}\n")

    f.write("\n")

    f.write("Structural Outlier Ranking\n")
    f.write("--------------------------\n\n")

    for _, row in outliers.iterrows():

        f.write(
            f"{int(row['OutlierRank']):2d}  "
            f"{row['Observable']:<20}"
            f"Score={row['OutlierScore']:.6f}   "
            f"Z={row['DistanceZ']:.6f}   "
            f"Isolation={row['RelativeIsolation']:.6f}\n"
        )

    f.write("\n")

    f.write("Conclusion\n")
    f.write("----------\n")

    f.write(
        "This experiment establishes an observational ranking "
        "of structural singularities within the certified "
        "Observable Space. The resulting scores quantify the "
        "degree of geometric exceptionality of each observable "
        "without introducing arbitrary thresholds or binary "
        "classification rules. The ranking complements the "
        "global geometric characterization developed in the "
        "previous experiments and concludes the structural "
        "analysis stage of the E6.2 series.\n"
    )


# ============================================================
# Final Console Summary
# ============================================================

print("=" * 70)
print("Experiment completed.")
print()
print("Results saved to:")
print(OUT)
print("=" * 70)


# ============================================================
# Main
# ============================================================

def main():
    """Main entry point."""
    pass


if __name__ == "__main__":
    main()
