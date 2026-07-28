"""
=============================================================
GER
S29_E8

Signature Trajectory Experiment

Version : 1.0
=============================================================
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

from GER.CORE.bootstrap import initialize
from GER.CORE.experiment_pipeline import run_signature_pipeline
from GER.CORE.ger_engine import run_engine

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)


# ==========================================================
# Experiment
# ==========================================================

EXPERIMENT = "S29_E8"

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29"
)

OUTPUT_DIR = (
    RESULTS_ROOT
    / EXPERIMENT
    / datetime.now().strftime("%Y%m%d_%H%M%S")
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

print("=" * 60)
print("GER")
print("S29 E8")
print("Signature Trajectory Experiment")
print("=" * 60)
print()
print("Output")
print(OUTPUT_DIR)
print()


# ==========================================================
# Scan configuration
# ==========================================================

SIGMA_START = 0.1000
SIGMA_STOP = 0.2000
SIGMA_STEP = 0.0001

N = 384

TIMESTEPS = 2000

DT = 0.00025

BETA = 1.0

POTENTIAL = "A"

SNAPSHOT_STRIDE = 50


# ==========================================================
# Trajectory
# ==========================================================

trajectory = []

trajectory_vectors = []


# ==========================================================
# Utilities
# ==========================================================

def euclidean_distance(a, b):

    return math.sqrt(

        sum(

            (x - y) ** 2

            for x, y in zip(a, b)

        )

    )


def save_json(name, obj):

    path = OUTPUT_DIR / name

    with open(

        path,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            obj,

            f,

            indent=4,

            ensure_ascii=False,

            default=str,

        )


# ==========================================================
# Initialization
# ==========================================================

initialize()


# ==========================================================
# Main Loop
# ==========================================================

sigma = SIGMA_START

experiment_index = 0

while sigma <= SIGMA_STOP + 1e-12:

    print()

    print("-" * 60)

    print(

        f"Experiment {experiment_index}"

    )

    print(

        f"Sigma = {sigma:.6f}"

    )


    simulation = run_engine(

        n=N,

        timesteps=TIMESTEPS,

        dt=DT,

        beta=BETA,

        potential=POTENTIAL,

        snapshot_stride=SNAPSHOT_STRIDE,

        sigma=sigma,

    )


    snapshots = simulation["snapshots"]

    configuration = simulation["configuration"]


    observables = run_persistence_observatory(

        snapshots,

        configuration["dt"],

    )


    pipeline = run_signature_pipeline(

        observables,

        configuration["dt"],

    )


    signature = pipeline["signature"]

    certificate = pipeline["certificate"]

    # ======================================================
    # Signature extraction
    # ======================================================

    signature_metadata = {}

    try:

        from GER.CORE.ger_geometric_signature import (
            extract_signature,
            extract_signature_metadata,
        )

        extracted = extract_signature(signature)

        try:

            signature_metadata = extract_signature_metadata(
                signature
            )

        except Exception:

            signature_metadata = {}

    except Exception:

        extracted = signature


    # ------------------------------------------------------
    # Normalize to dictionary
    # ------------------------------------------------------

    if isinstance(extracted, dict):

        signature_dict = extracted

    elif hasattr(extracted, "to_dict"):

        signature_dict = extracted.to_dict()

    elif hasattr(extracted, "__dict__"):

        signature_dict = dict(extracted.__dict__)

    else:

        signature_dict = {
            "value": extracted,
        }


    # ------------------------------------------------------
    # Numeric vector
    # ------------------------------------------------------

    signature_vector = []

    for key in sorted(signature_dict.keys()):

        value = signature_dict[key]

        if isinstance(value, (int, float)):

            signature_vector.append(
                float(value)
            )

    # ======================================================
    # Trajectory vector
    # ======================================================

    #
    # Mantemos sempre a mesma ordem.
    #

    signature_vector = [

        float(v)

        for _, v in sorted(

            signature_dict.items()

        )

        if isinstance(

            v,

            (

                int,

                float,

            ),

        )

    ]


    # ======================================================
    # Geometric trajectory
    # ======================================================

    if len(

        trajectory_vectors

    ) == 0:

        delta_sigma = 0.0

        path_length = 0.0

    else:

        delta_sigma = euclidean_distance(

            trajectory_vectors[-1],

            signature_vector,

        )

        path_length = (

            trajectory[-1]["path_length"]

            +

            delta_sigma

        )


    trajectory_vectors.append(

        signature_vector

    )


    # ======================================================
    # Record
    # ======================================================

    record = {

        "index":

            experiment_index,

        "sigma":

            sigma,

        "signature":

            signature_dict,

        "metadata":

            signature_metadata,

        "certificate":

            certificate,

        "delta_sigma":

            delta_sigma,

        "path_length":

            path_length,

        "vector":

            signature_vector,

    }

    trajectory.append(

        record

    )


    # ======================================================
    # Progress
    # ======================================================

    print(

        "Signature dimension :",

        len(

            signature_vector

        )

    )

    print(

        "Delta Sigma         :",

        f"{delta_sigma:.8f}",

    )

    print(

        "Path Length         :",

        f"{path_length:.8f}",

    )


    # ======================================================
    # Incremental save
    # ======================================================

    save_json(

        "trajectory.json",

        trajectory,

    )

    save_json(

        "trajectory_vectors.json",

        trajectory_vectors,

    )

    save_json(

        "last_signature.json",

        signature_dict,

    )

    save_json(

        "last_certificate.json",

        certificate,

    )


    # ======================================================
    # Next experiment
    # ======================================================

    experiment_index += 1

    sigma += SIGMA_STEP

    # ======================================================
    # Console
    # ======================================================

    print()

    print(
        "Certificate :",
        certificate,
    )

    print(
        "Trajectory Points :",
        len(trajectory),
    )

    print(
        "Current Length :",
        f"{path_length:.8f}",
    )

    print()

    # ======================================================
    # Next sigma
    # ======================================================

    experiment_index += 1

    sigma += SIGMA_STEP


# ==========================================================
# End of scan
# ==========================================================

print()

print("=" * 60)
print("Trajectory completed.")
print("=" * 60)
print()

total_points = len(trajectory)

total_length = 0.0

if total_points > 0:

    total_length = trajectory[-1]["path_length"]


summary = {

    "experiment": EXPERIMENT,

    "points": total_points,

    "sigma_start": SIGMA_START,

    "sigma_stop": SIGMA_STOP,

    "sigma_step": SIGMA_STEP,

    "path_length": total_length,

    "dimension": (

        len(trajectory_vectors[0])

        if trajectory_vectors

        else 0

    ),

    "output_directory": str(
        OUTPUT_DIR
    ),

}

save_json(

    "summary.json",

    summary,

)


# ==========================================================
# CSV export
# ==========================================================

import csv

csv_file = OUTPUT_DIR / "trajectory.csv"

with open(

    csv_file,

    "w",

    newline="",

    encoding="utf-8",

) as f:

    writer = csv.writer(f)

    writer.writerow(

        [

            "index",

            "sigma",

            "delta_sigma",

            "path_length",

        ]

    )

    for record in trajectory:

        writer.writerow(

            [

                record["index"],

                record["sigma"],

                record["delta_sigma"],

                record["path_length"],

            ]

        )


# ==========================================================
# TXT report
# ==========================================================

report = OUTPUT_DIR / "report.txt"

with open(

    report,

    "w",

    encoding="utf-8",

) as f:

    f.write("=" * 60 + "\n")

    f.write("GER\n")

    f.write("S29 E8\n")

    f.write("Signature Trajectory Experiment\n")

    f.write("=" * 60 + "\n\n")

    f.write(

        f"Trajectory points : {total_points}\n"

    )

    f.write(

        f"Sigma start      : {SIGMA_START}\n"

    )

    f.write(

        f"Sigma stop       : {SIGMA_STOP}\n"

    )

    f.write(

        f"Sigma step       : {SIGMA_STEP}\n"

    )

    f.write(

        f"Dimension        : {summary['dimension']}\n"

    )

    f.write(

        f"Path length      : {total_length:.10f}\n"

    )

    f.write("\n")

    f.write("Output directory\n")

    f.write(

        str(OUTPUT_DIR)

    )

    f.write("\n")


# ==========================================================
# Final console
# ==========================================================

print()

print("=" * 60)

print("Experiment finished.")

print("=" * 60)

print()

print(

    "Trajectory points :",

    total_points,

)

print(

    "Trajectory length :",

    f"{total_length:.8f}",

)

print(

    "Results saved to:",

    OUTPUT_DIR,

)

print()

    # ======================================================
    # Geometric trajectory analysis
    # ======================================================

    velocity = delta_sigma

    acceleration = 0.0

    curvature = 0.0

    turning_angle = 0.0

    if len(trajectory) >= 1:

        previous_velocity = trajectory[-1].get(
            "velocity",
            0.0,
        )

        acceleration = (

            velocity

            -

            previous_velocity

        )


    if len(trajectory_vectors) >= 3:

        p1 = trajectory_vectors[-3]

        p2 = trajectory_vectors[-2]

        p3 = trajectory_vectors[-1]


        v1 = [

            b - a

            for a, b in zip(
                p1,
                p2,
            )

        ]


        v2 = [

            c - b

            for b, c in zip(
                p2,
                p3,
            )

        ]


        norm1 = math.sqrt(

            sum(

                x * x

                for x in v1

            )

        )


        norm2 = math.sqrt(

            sum(

                x * x

                for x in v2

            )

        )


        if (

            norm1 > 0.0

            and

            norm2 > 0.0

        ):

            dot = sum(

                a * b

                for a, b in zip(
                    v1,
                    v2,
                )

            )


            cosine = dot / (

                norm1 * norm2

            )


            cosine = max(

                -1.0,

                min(

                    1.0,

                    cosine,

                ),

            )


            turning_angle = math.acos(
                cosine
            )


            curvature = (

                turning_angle

                /

                max(

                    norm2,

                    1e-12,

                )

            )


    if len(trajectory) == 0:

        stability = "origin"

    elif velocity < 1e-8:

        stability = "stationary"

    elif curvature < 1e-3:

        stability = "smooth"

    elif curvature < 1e-1:

        stability = "transition"

    else:

        stability = "bifurcation"

if __name__ == "__main__":
    run_experiment()
