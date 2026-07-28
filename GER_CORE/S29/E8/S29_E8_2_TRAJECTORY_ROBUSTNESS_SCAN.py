"""
===============================================================================
S29_E8_2_TRAJECTORY_ROBUSTNESS_SCAN.py
===============================================================================

Experiment:
    S29 E8.2 - Trajectory Robustness Scan (Sliding Window)

Objective
---------
Verify whether the geometric properties observed in S29_E8_1 remain invariant
when the observation window is translated along the control parameter σ.

The experiment performs a sliding-window scan over the trajectory and computes
the same geometric descriptors used in E8.1 for each window.

Input
-----
/content/drive/MyDrive/GER_RESULTS/S29/S29_E8

Expected files
--------------
trajectory.csv
trajectory_vectors.json
summary.json

Outputs
-------
GER_RESULTS/
    S29/
        S29_E8_2_TRAJECTORY_ROBUSTNESS_SCAN/

            robustness_scan.csv
            robustness_scan.json
            robustness_summary.txt

Author
------
GER Project
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import pandas as pd


# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/S29_E8"
)

OUTPUT_DIR = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29/"
    "S29_E8_2_TRAJECTORY_ROBUSTNESS_SCAN"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


TRAJECTORY_FILE = INPUT_DIR / "trajectory.csv"
VECTORS_FILE = INPUT_DIR / "trajectory_vectors.json"
SUMMARY_FILE = INPUT_DIR / "summary.json"


# -----------------------------------------------------------------------------
# Sliding window parameters
# -----------------------------------------------------------------------------

WINDOW_SIZE = 101
WINDOW_STEP = 10

EPS = 1e-12


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class WindowResult:

    window_id: int

    start_index: int
    end_index: int

    sigma_start: float
    sigma_end: float

    samples: int

    path_length: float

    mean_velocity: float
    max_velocity: float

    mean_acceleration: float
    max_acceleration: float

    mean_curvature: float
    max_curvature: float

    mean_turning_angle: float
    max_turning_angle: float

    alignment_mean: float
    alignment_min: float

    effective_dimension: int

    stable_points: int

    transition_points: int

    bifurcation_points: int

    stationary_points: int


# =============================================================================
# IO
# =============================================================================

def load_summary():

    with open(SUMMARY_FILE, "r") as f:
        return json.load(f)


def load_trajectory():

    return pd.read_csv(TRAJECTORY_FILE)


def load_vectors():

    with open(VECTORS_FILE, "r") as f:
        vectors = json.load(f)

    return np.asarray(vectors, dtype=float)


# =============================================================================
# BASIC UTILITIES
# =============================================================================

def vector_norm(v):

    return np.linalg.norm(v)


def normalize(v):

    n = vector_norm(v)

    if n < EPS:
        return np.zeros_like(v)

    return v / n


def cosine_similarity(a, b):

    na = vector_norm(a)
    nb = vector_norm(b)

    if na < EPS or nb < EPS:
        return 1.0

    return float(np.dot(a, b) / (na * nb))


def safe_mean(values):

    if len(values) == 0:
        return 0.0

    return float(np.mean(values))


def safe_max(values):

    if len(values) == 0:
        return 0.0

    return float(np.max(values))


# =============================================================================
# TRAJECTORY UTILITIES
# =============================================================================

def trajectory_displacements(points):

    return np.diff(points, axis=0)


def trajectory_length(points):

    disp = trajectory_displacements(points)

    if len(disp) == 0:
        return 0.0

    return float(np.sum(np.linalg.norm(disp, axis=1)))


def dominant_direction(points):

    disp = trajectory_displacements(points)

    if len(disp) == 0:
        return np.zeros(points.shape[1])

    direction = np.mean(disp, axis=0)

    return normalize(direction)


def effective_dimension(points):

    centered = points - points.mean(axis=0)

    covariance = np.cov(centered.T)

    eigvals = np.linalg.eigvalsh(covariance)

    eigvals = np.maximum(eigvals, 0.0)

    total = eigvals.sum()

    if total < EPS:
        return 0

    ratios = eigvals / total

    return int(np.sum(ratios > 1e-3))


# =============================================================================
# WINDOW GENERATOR
# =============================================================================

def generate_windows(n_points):

    start = 0
    idx = 0

    while start + WINDOW_SIZE <= n_points:

        yield idx, start, start + WINDOW_SIZE

        idx += 1
        start += WINDOW_STEP
      # =============================================================================
# GEOMETRIC ANALYSIS
# =============================================================================

def alignment_statistics(points):
    """
    Computes directional alignment between all displacement vectors
    and the dominant trajectory direction.
    """

    disp = trajectory_displacements(points)

    if len(disp) == 0:

        return {
            "mean": 1.0,
            "min": 1.0
        }

    direction = dominant_direction(points)

    similarities = []

    for d in disp:

        similarities.append(
            cosine_similarity(
                normalize(d),
                direction
            )
        )

    similarities = np.asarray(similarities)

    return {

        "mean": float(similarities.mean()),
        "min": float(similarities.min())

    }


def curvature_statistics(df_window):

    curvature = (
        df_window["curvature"]
        .to_numpy(dtype=float)
    )

    turning = (
        df_window["turning_angle"]
        .to_numpy(dtype=float)
    )

    return {

        "mean_curvature": safe_mean(curvature),
        "max_curvature": safe_max(curvature),

        "mean_turning": safe_mean(turning),
        "max_turning": safe_max(turning)

    }


def velocity_statistics(df_window):

    velocity = (
        df_window["velocity"]
        .to_numpy(dtype=float)
    )

    acceleration = (
        df_window["acceleration"]
        .to_numpy(dtype=float)
    )

    return {

        "mean_velocity": safe_mean(velocity),
        "max_velocity": safe_max(velocity),

        "mean_acceleration": safe_mean(acceleration),
        "max_acceleration": safe_max(acceleration)

    }


def stability_statistics(df_window):
    """
    Counts structural labels inside the window.
    """

    stable = 0
    transition = 0
    bifurcation = 0
    stationary = 0

    if "stability" not in df_window.columns:

        return {

            "stable": 0,
            "transition": 0,
            "bifurcation": 0,
            "stationary": 0

        }

    labels = (
        df_window["stability"]
        .astype(str)
        .str.lower()
    )

    for label in labels:

        if "stable" in label:
            stable += 1

        elif "transition" in label:
            transition += 1

        elif "bifurcation" in label:
            bifurcation += 1

        elif "stationary" in label:
            stationary += 1

    return {

        "stable": stable,
        "transition": transition,
        "bifurcation": bifurcation,
        "stationary": stationary

    }


# =============================================================================
# WINDOW ANALYSIS
# =============================================================================

def analyze_window(
    window_id,
    start,
    end,
    trajectory_df,
    trajectory_points
):

    df_window = trajectory_df.iloc[start:end].reset_index(drop=True)

    points = trajectory_points[start:end]

    velocity = velocity_statistics(df_window)

    curvature = curvature_statistics(df_window)

    alignment = alignment_statistics(points)

    stability = stability_statistics(df_window)

    result = WindowResult(

        window_id=window_id,

        start_index=start,
        end_index=end - 1,

        sigma_start=float(df_window.iloc[0]["sigma"]),
        sigma_end=float(df_window.iloc[-1]["sigma"]),

        samples=len(df_window),

        path_length=trajectory_length(points),

        mean_velocity=velocity["mean_velocity"],
        max_velocity=velocity["max_velocity"],

        mean_acceleration=velocity["mean_acceleration"],
        max_acceleration=velocity["max_acceleration"],

        mean_curvature=curvature["mean_curvature"],
        max_curvature=curvature["max_curvature"],

        mean_turning_angle=curvature["mean_turning"],
        max_turning_angle=curvature["max_turning"],

        alignment_mean=alignment["mean"],
        alignment_min=alignment["min"],

        effective_dimension=effective_dimension(points),

        stable_points=stability["stable"],
        transition_points=stability["transition"],
        bifurcation_points=stability["bifurcation"],
        stationary_points=stability["stationary"]

    )

    return result


# =============================================================================
# COMPLETE SCAN
# =============================================================================

def robustness_scan(
    trajectory_df,
    trajectory_points
):

    results = []

    total_points = len(trajectory_df)

    for window_id, start, end in generate_windows(total_points):

        result = analyze_window(

            window_id=window_id,

            start=start,
            end=end,

            trajectory_df=trajectory_df,
            trajectory_points=trajectory_points

        )

        results.append(result)

    return results
  # =============================================================================
# EXPORTS
# =============================================================================

def results_dataframe(results):

    rows = []

    for r in results:
        rows.append(asdict(r))

    return pd.DataFrame(rows)


def export_csv(df):

    output = OUTPUT_DIR / "robustness_scan.csv"

    df.to_csv(
        output,
        index=False
    )

    return output


def export_json(df):

    output = OUTPUT_DIR / "robustness_scan.json"

    records = df.to_dict(orient="records")

    with open(output, "w") as f:

        json.dump(
            records,
            f,
            indent=4
        )

    return output


# =============================================================================
# GLOBAL SUMMARY
# =============================================================================

def build_summary(df):

    summary = {

        "experiment":
            "S29_E8_2_TRAJECTORY_ROBUSTNESS_SCAN",

        "windows":
            int(len(df)),

        "window_size":
            WINDOW_SIZE,

        "window_step":
            WINDOW_STEP,

        "sigma_min":
            float(df["sigma_start"].min()),

        "sigma_max":
            float(df["sigma_end"].max()),

        "mean_path_length":
            float(df["path_length"].mean()),

        "std_path_length":
            float(df["path_length"].std()),

        "mean_velocity":
            float(df["mean_velocity"].mean()),

        "std_velocity":
            float(df["mean_velocity"].std()),

        "mean_curvature":
            float(df["mean_curvature"].mean()),

        "max_curvature":
            float(df["max_curvature"].max()),

        "mean_alignment":
            float(df["alignment_mean"].mean()),

        "minimum_alignment":
            float(df["alignment_min"].min()),

        "mean_effective_dimension":
            float(df["effective_dimension"].mean()),

        "maximum_effective_dimension":
            int(df["effective_dimension"].max()),

        "stable_windows":
            int(
                (df["transition_points"] == 0).sum()
            ),

        "transition_windows":
            int(
                (df["transition_points"] > 0).sum()
            ),

        "bifurcation_windows":
            int(
                (df["bifurcation_points"] > 0).sum()
            )

    }

    return summary


# =============================================================================
# TEXT REPORT
# =============================================================================

def export_report(summary):

    output = OUTPUT_DIR / "robustness_summary.txt"

    lines = []

    lines.append("=" * 80)
    lines.append("S29 E8.2")
    lines.append("TRAJECTORY ROBUSTNESS SCAN")
    lines.append("=" * 80)
    lines.append("")

    for key, value in summary.items():

        lines.append(
            f"{key:30s}: {value}"
        )

    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF REPORT")
    lines.append("=" * 80)

    with open(output, "w") as f:

        f.write("\n".join(lines))

    return output


# =============================================================================
# CONSOLE REPORT
# =============================================================================

def print_summary(summary):

    print()
    print("=" * 80)
    print("S29 E8.2")
    print("Trajectory Robustness Scan")
    print("=" * 80)

    for k, v in summary.items():

        print(f"{k:30s}: {v}")

    print("=" * 80)
    print()


# =============================================================================
# MAIN
# =============================================================================

def main():

    print()
    print("=" * 80)
    print("Loading experiment...")
    print("=" * 80)

    _ = load_summary()

    trajectory = load_trajectory()

    vectors = load_vectors()

    print(f"Trajectory points : {len(trajectory)}")
    print(f"Vector dimension  : {vectors.shape[1]}")
    print()

    print("Running sliding-window robustness scan...")

    results = robustness_scan(

        trajectory_df=trajectory,
        trajectory_points=vectors

    )

    print(f"Windows analyzed : {len(results)}")

    df = results_dataframe(results)

    export_csv(df)

    export_json(df)

    summary = build_summary(df)

    export_report(summary)

    print_summary(summary)

    print("Results saved to:")
    print(OUTPUT_DIR)

    print()
    print("Experiment completed successfully.")
    print()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
