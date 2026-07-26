"""
============================================================
GER
S29-E6.2.7.1
STRUCTURAL PERIPHERALITY ANALYSIS
============================================================

Objective
---------
Characterize the structural peripherality of the certified
Observable Space.

Unlike the Structural Outlier Analysis (E6.2.7), which
measures geometric exceptionality, this experiment quantifies
only the radial distance from the certified geometric nucleus.

The resulting Peripherality Score provides a direct,
parameter-free measure of how peripheral each observable is
within the intrinsic geometry of the Observable Space.

Execution
---------
python -m GER_CORE.S29.S29_E6_2_7_1_structural_peripherality_analysis

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
    / "E6_2_7_StructuralOutlierAnalysis"
    / "outlier_profile.csv"
)

CERTIFICATE_FILE = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_7_StructuralOutlierAnalysis"
    / "outlier_certificate.json"
)


# ============================================================
# OUTPUT
# ============================================================

OUT = (
    Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.2")
    / "E6_2_7_1_StructuralPeripherality"
)

OUT.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Banner
# ============================================================

print("=" * 70)
print("GER")
print("S29-E6.2.7.1")
print("Structural Peripherality Analysis")
print("=" * 70)


# ============================================================
# Load
# ============================================================

profile = pd.read_csv(PROFILE_FILE)

with open(
    CERTIFICATE_FILE,
    "r",
    encoding="utf-8"
) as f:

    certificate = json.load(f)

nucleus = certificate["geometric_nucleus"]

print("[OK] outlier_profile.csv")
print("[OK] outlier_certificate.json")

print()

print(f"Observables : {len(profile)}")
print(f"Geometric Nucleus : {nucleus}")

print()

# ============================================================
# Peripherality Profile
# ============================================================

periphery = profile.copy()

max_distance = float(
    periphery["DistanceToNucleus"].max()
)

if max_distance > 0:

    periphery["PeripheralityScore"] = (

        periphery["DistanceToNucleus"] /
        max_distance

    )

else:

    periphery["PeripheralityScore"] = 0.0


# ============================================================
# Ranking
# ============================================================

periphery = periphery.sort_values(

    "PeripheralityScore",

    ascending=False

).reset_index(drop=True)

periphery["PeripheralRank"] = np.arange(

    1,
    len(periphery) + 1

)


# ============================================================
# Summary Statistics
# ============================================================

mean_score = float(

    periphery["PeripheralityScore"].mean()

)

std_score = float(

    periphery["PeripheralityScore"].std(ddof=0)

)

max_score = float(

    periphery["PeripheralityScore"].max()

)

min_score = float(

    periphery["PeripheralityScore"].min()

)


# ============================================================
# Peripheral Classes (continuous partition)
# ============================================================

bins = np.linspace(0.0, 1.0, 6)

labels = [

    "Central",
    "Inner",
    "Intermediate",
    "Outer",
    "Peripheral"

]

periphery["PeripheralClass"] = pd.cut(

    periphery["PeripheralityScore"],

    bins=bins,

    labels=labels,

    include_lowest=True

)


# ============================================================
# Save Profile
# ============================================================

periphery.to_csv(

    OUT / "peripherality_profile.csv",

    index=False

)


# ============================================================
# Summary
# ============================================================

summary = pd.DataFrame({

    "Metric":[

        "MeanPeripherality",
        "StdPeripherality",
        "MaximumPeripherality",
        "MinimumPeripherality"

    ],

    "Value":[

        mean_score,
        std_score,
        max_score,
        min_score

    ]

})

summary.to_csv(

    OUT / "peripherality_summary.csv",

    index=False

)


# ============================================================
# Console
# ============================================================

print("=" * 70)
print("Structural Peripherality Summary")
print("=" * 70)

print(f"Geometric Nucleus      : {nucleus}")
print(f"Maximum Score          : {max_score:.6f}")
print(f"Mean Score             : {mean_score:.6f}")
print(f"Minimum Score          : {min_score:.6f}")

print()

print("Most Peripheral Observables")

for _, row in periphery.head(5).iterrows():

    print(

        f"{int(row['PeripheralRank']):2d}  "
        f"{row['Observable']:<20}"
        f"{row['PeripheralityScore']:.6f}"

    )

print()

# ============================================================
# Scientific Certificate
# ============================================================

certificate = {

    "experiment": "S29-E6.2.7.1",

    "title": "Structural Peripherality Analysis",

    "geometric_nucleus": nucleus,

    "observables": int(len(periphery)),

    "maximum_peripherality": max_score,

    "minimum_peripherality": min_score,

    "mean_peripherality": mean_score,

    "std_peripherality": std_score,

    "most_peripheral_observable":
        periphery.iloc[0]["Observable"],

    "least_peripheral_observable":
        periphery.iloc[-1]["Observable"]

}

with open(

    OUT / "peripherality_certificate.json",

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

    OUT / "peripherality_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("GER\n")
    f.write("S29-E6.2.7.1\n")
    f.write("Structural Peripherality Analysis\n")
    f.write("=" * 60 + "\n\n")

    f.write("Global Statistics\n")
    f.write("-----------------\n\n")

    f.write(f"Geometric Nucleus           : {nucleus}\n")
    f.write(f"Observables                 : {len(periphery)}\n")
    f.write(f"Maximum Peripherality       : {max_score:.6f}\n")
    f.write(f"Mean Peripherality          : {mean_score:.6f}\n")
    f.write(f"Std Peripherality           : {std_score:.6f}\n")
    f.write(f"Minimum Peripherality       : {min_score:.6f}\n")
    f.write(f"Most Peripheral Observable  : {periphery.iloc[0]['Observable']}\n")
    f.write(f"Least Peripheral Observable : {periphery.iloc[-1]['Observable']}\n")

    f.write("\n")

    f.write("Peripherality Ranking\n")
    f.write("---------------------\n\n")

    for _, row in periphery.iterrows():

        f.write(
            f"{int(row['PeripheralRank']):2d}  "
            f"{row['Observable']:<20}"
            f"Score={row['PeripheralityScore']:.6f}   "
            f"Distance={row['DistanceToNucleus']:.6f}   "
            f"Class={row['PeripheralClass']}\n"
        )

    f.write("\n")

    f.write("Scientific Conclusion\n")
    f.write("---------------------\n\n")

    f.write(
        "This experiment provides a dedicated characterization "
        "of structural peripherality within the certified "
        "Observable Space. Unlike the Structural Outlier "
        "Analysis, which measures geometric exceptionality, "
        "the present analysis quantifies only radial "
        "peripherality with respect to the certified "
        "geometric nucleus. The resulting ranking is a direct, "
        "parameter-free representation of the intrinsic "
        "radial organization of the Observable Space and "
        "complements the structural characterization of the "
        "E6.2 series.\n"
    )


# ============================================================
# Final Console Summary
# ============================================================

print("=" * 70)
print("Experiment completed.")
print()

print("Most Peripheral Observable :",
      periphery.iloc[0]["Observable"])

print("Least Peripheral Observable:",
      periphery.iloc[-1]["Observable"])

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
