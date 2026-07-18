"""
============================================================
GER
S29-E3.2
GEOMETRIC STABILITY REGIONS
============================================================

Uses:
    S29_E3_1_signature_map.csv

Produces:
    S29_E3_2_stability_regions.csv
    S29_E3_2_summary.txt
    S29_E3_2_stability_map.png

Description
-----------
Analyzes the geometric organization of the signature space
generated in S29-E3.1.

No new simulations are executed.

Author:
GER Project
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# FILES
# ============================================================

INPUT_CSV = Path("/content/drive/MyDrive/GER_RESULTS/S29_E3_1_signature_map.csv")

OUTPUT_CSV = Path("S29_E3_2_stability_regions.csv")

SUMMARY_FILE = Path("S29_E3_2_summary.txt")

FIGURE_FILE = Path("S29_E3_2_stability_map.png")


# ============================================================
# SIGNATURE VARIABLES
# ============================================================

SIGNATURE_COLUMNS = [
    "diameter",
    "convergence",
    "recurrence",
    "drift",
]


# ============================================================
# UTILITIES
# ============================================================

def print_header():

    print()
    print("=" * 60)
    print("GER")
    print("S29-E3.2")
    print("GEOMETRIC STABILITY REGIONS")
    print("=" * 60)
    print()


def check_input_file():

    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{INPUT_CSV}"
        )


# ============================================================
# DATA LOADING
# ============================================================

def load_signature_map():

    check_input_file()

    df = pd.read_csv(INPUT_CSV)

    required = [
        "gamma",
        "diameter",
        "convergence",
        "recurrence",
        "drift",
    ]

    missing = [
        c
        for c in required
        if c not in df.columns
    ]

    if missing:
        raise RuntimeError(
            "Missing columns:\n"
            + "\n".join(missing)
        )

    df = df.sort_values("gamma").reset_index(drop=True)

    print(f"Loaded signatures : {len(df)}")

    return df


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_signature_space(df):

    norm = df.copy()

    print()
    print("Normalizing signature space...")
    print()

    for column in SIGNATURE_COLUMNS:

        mean = df[column].mean()

        std = df[column].std()

        if std == 0:

            norm[column] = 0.0

        else:

            norm[column] = (
                df[column] - mean
            ) / std

        print(
            f"{column:<15}"
            f"mean={mean:12.6f}   "
            f"std={std:12.6f}"
        )

    return norm

# ============================================================
# GEOMETRIC DISPLACEMENTS
# ============================================================

def compute_neighbor_displacements(df):

    rows = []

    for i in range(len(df) - 1):

        p0 = df.loc[i, SIGNATURE_COLUMNS].to_numpy(dtype=float)
        p1 = df.loc[i + 1, SIGNATURE_COLUMNS].to_numpy(dtype=float)

        distance = np.linalg.norm(p1 - p0)

        rows.append(
            {
                "gamma_start": float(df.loc[i, "gamma"]),
                "gamma_end": float(df.loc[i + 1, "gamma"]),
                "distance": float(distance),
            }
        )

    disp = pd.DataFrame(rows)

    print()
    print(f"Neighbor displacements : {len(disp)}")

    return disp


# ============================================================
# DISPLACEMENT STATISTICS
# ============================================================

def compute_statistics(displacements):

    d = displacements["distance"].to_numpy()

    stats = {

        "mean": float(np.mean(d)),
        "median": float(np.median(d)),
        "std": float(np.std(d)),

        "min": float(np.min(d)),
        "max": float(np.max(d)),

        "p10": float(np.percentile(d, 10)),
        "p25": float(np.percentile(d, 25)),
        "p50": float(np.percentile(d, 50)),
        "p75": float(np.percentile(d, 75)),
        "p90": float(np.percentile(d, 90)),
    }

    print()
    print("=" * 60)
    print("Displacement Statistics")
    print("=" * 60)

    for key in [
        "min",
        "p10",
        "p25",
        "p50",
        "median",
        "mean",
        "p75",
        "p90",
        "max",
        "std",
    ]:

        print(f"{key:<10} : {stats[key]:.6f}")

    return stats


# ============================================================
# REGION CONSTRUCTION
# ============================================================

def build_regions(df, displacements, stats):

    threshold = stats["p90"]

    regions = []

    region_start = float(df.iloc[0]["gamma"])
    region_distances = []

    region_id = 1

    for _, row in displacements.iterrows():

        distance = float(row["distance"])

        region_distances.append(distance)

        if distance >= threshold:

            gamma_end = float(row["gamma_end"])

            mean_distance = float(np.mean(region_distances))
            max_distance = float(np.max(region_distances))

            classification = f"Region {region_id:02d}"

            regions.append({
                "region_id": f"R{region_id:03d}",
                "gamma_start": region_start,
                "gamma_end": gamma_end,
                "length": gamma_end - region_start,
                "mean_distance": mean_distance,
                "max_distance": max_distance,
                "classification": classification,
            })

            region_id += 1
            region_start = gamma_end
            region_distances = []

    if len(region_distances) > 0:

        gamma_end = float(df.iloc[-1]["gamma"])

        mean_distance = float(np.mean(region_distances))
        max_distance = float(np.max(region_distances))

        classification = f"Region {region_id:02d}"

        regions.append({
            "region_id": f"R{region_id:03d}",
            "gamma_start": region_start,
            "gamma_end": gamma_end,
            "length": gamma_end - region_start,
            "mean_distance": mean_distance,
            "max_distance": max_distance,
            "classification": classification,
        })

    regions = pd.DataFrame(regions)

    print()
    print("=" * 60)
    print("Regions")
    print("=" * 60)
    print(regions)

    return regions
  # ============================================================
# CSV EXPORT
# ============================================================

def save_regions_csv(regions):

    regions.to_csv(
        OUTPUT_CSV,
        index=False,
    )

    print()
    print(f"CSV saved : {OUTPUT_CSV}")


# ============================================================
# SUMMARY
# ============================================================

def save_summary(stats, regions):

    stable = int((regions.classification == "Stable").sum())
    intermediate = int((regions.classification == "Intermediate").sum())
    transition = int((regions.classification == "Transition").sum())

    largest = regions.iloc[
        regions["length"].idxmax()
    ]

    strongest = regions.iloc[
        regions["max_distance"].idxmax()
    ]

    with open(SUMMARY_FILE, "w") as f:

        f.write("=" * 60 + "\n")
        f.write("GER\n")
        f.write("S29-E3.2\n")
        f.write("GEOMETRIC STABILITY REGIONS\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Total regions : {len(regions)}\n\n")

        f.write("Classification\n")
        f.write("------------------------------\n")
        f.write(f"Stable        : {stable}\n")
        f.write(f"Intermediate  : {intermediate}\n")
        f.write(f"Transition    : {transition}\n\n")

        f.write("Distance Statistics\n")
        f.write("------------------------------\n")

        for key in [
            "min",
            "p10",
            "p25",
            "p50",
            "median",
            "mean",
            "p75",
            "p90",
            "max",
            "std",
        ]:

            f.write(
                f"{key:<10}: {stats[key]:.6f}\n"
            )

        f.write("\n")

        f.write("Largest Region\n")
        f.write("------------------------------\n")

        f.write(
            f"ID            : {largest.region_id}\n"
        )

        f.write(
            f"Gamma         : "
            f"{largest.gamma_start:.6f} -> "
            f"{largest.gamma_end:.6f}\n"
        )

        f.write(
            f"Length        : {largest.length:.6f}\n"
        )

        f.write(
            f"Class         : {largest.classification}\n\n"
        )

        f.write("Largest Boundary\n")
        f.write("------------------------------\n")

        f.write(
            f"Region        : {strongest.region_id}\n"
        )

        f.write(
            f"Maximum ΔΣ    : "
            f"{strongest.max_distance:.6f}\n\n"
        )

        f.write("Interpretation\n")
        f.write("------------------------------\n")

        f.write(
            "The signature space was partitioned "
            "into contiguous geometric regions "
            "using percentile-based displacement "
            "thresholds.\n"
        )

    print(f"Summary saved : {SUMMARY_FILE}")


# ============================================================
# STABILITY MAP
# ============================================================

def plot_stability_map(regions):

    region_color = "steelblue"

    fig, ax = plt.subplots(
        figsize=(12, 1.8)
    )

    for _, row in regions.iterrows():

        ax.axvspan(
            row.gamma_start,
            row.gamma_end,
            color=region_color,
            alpha=0.90,
        )

    for _, row in regions.iterrows():

        ax.axvline(
            row.gamma_start,
            color="black",
            linewidth=0.5,
        )

    ax.set_xlim(
        regions.gamma_start.min(),
        regions.gamma_end.max(),
    )

    ax.set_ylim(0, 1)

    ax.set_yticks([])

    ax.set_xlabel("Gamma")

    ax.set_title(
        "Geometric Stability Regions"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURE_FILE,
        dpi=300,
    )

    plt.close()

    print(f"Figure saved : {FIGURE_FILE}")
  # ============================================================
# MAIN
# ============================================================

def main():

    print_header()

    try:

        # ----------------------------------------------------
        # Load
        # ----------------------------------------------------

        df = load_signature_map()

        # ----------------------------------------------------
        # Normalize
        # ----------------------------------------------------

        df_norm = normalize_signature_space(df)

        # ----------------------------------------------------
        # Geometric displacements
        # ----------------------------------------------------

        displacements = compute_neighbor_displacements(df_norm)

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        stats = compute_statistics(displacements)

        # ----------------------------------------------------
        # Stability regions
        # ----------------------------------------------------

        regions = build_regions(
            df,
            displacements,
            stats,
        )

        # ----------------------------------------------------
        # Export
        # ----------------------------------------------------

        save_regions_csv(regions)

        save_summary(
            stats,
            regions,
        )

        plot_stability_map(regions)

        # ----------------------------------------------------
        # Final report
        # ----------------------------------------------------

        print()
        print("=" * 60)
        print("EXPERIMENT COMPLETED")
        print("=" * 60)

        print()

                print(f"Input CSV  : {INPUT_CSV}")
        print(f"Regions    : {OUTPUT_CSV}")
        print(f"Summary    : {SUMMARY_FILE}")
        print(f"Figure     : {FIGURE_FILE}")

        print()

        print(f"Total regions : {len(regions)}")

        print(
            f"Gamma range   : "
            f"{regions.gamma_start.min():.3f} -> {regions.gamma_end.max():.3f}"
        )

        print(
            f"Mean length   : "
            f"{regions.length.mean():.3f}"
        )

        print()

        print("Done.")

    except Exception as exc:

        print()

        print("=" * 60)
        print("ERROR")
        print("=" * 60)

        print(type(exc).__name__)
        print(exc)

        raise


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
