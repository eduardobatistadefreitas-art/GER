"""
=============================================================
GER
S29_E8

Signature Trajectory Experiment

Version : 1.0
=============================================================
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path

from GER.CORE.bootstrap import initialize
from GER.CORE.ger_engine import run_engine
from GER.CORE.experiment_pipeline import run_signature_pipeline

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)


# ==========================================================
# Experiment configuration
# ==========================================================

EXPERIMENT = "S29_E8"

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS"
)

TIMESTAMP = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

OUTPUT_DIR = (
    RESULTS_ROOT
    / "S29"
    / EXPERIMENT
    / TIMESTAMP
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# Scan parameters
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
# Containers
# ==========================================================

trajectory = []
trajectory_vectors = []


# ==========================================================
# Utility functions
# ==========================================================

def euclidean_distance(a, b):

    return math.sqrt(

        sum(

            (x - y) ** 2

            for x, y in zip(a, b)

        )

    )


def save_json(filename, obj):

    path = OUTPUT_DIR / filename

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


def normalize_signature(signature):

    """
    Converts any Signature representation into:

        signature_dict
        signature_vector
    """

    try:

        from GER.CORE.ger_geometric_signature import (
            extract_signature,
        )

        extracted = extract_signature(
            signature
        )

    except Exception:

        extracted = signature


    if isinstance(extracted, dict):

        signature_dict = extracted

    elif hasattr(extracted, "to_dict"):

        signature_dict = extracted.to_dict()

    elif hasattr(extracted, "__dict__"):

        signature_dict = dict(
            extracted.__dict__
        )

    else:

        signature_dict = {
            "value": extracted
        }


    signature_vector = []

    for key in sorted(signature_dict):

        value = signature_dict[key]

        if isinstance(

            value,

            (int, float),

        ):

            signature_vector.append(
                float(value)
            )


    return (

        signature_dict,

        signature_vector,

    )


# ==========================================================
# Initialization
# ==========================================================

initialize()

print("=" * 60)
print("GER")
print("S29 E8")
print("Signature Trajectory Experiment")
print("=" * 60)
print()
print("Output directory")
print(OUTPUT_DIR)
print()


# ==========================================================
# Main scan
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

# ======================================================
# Signature pipeline
# ======================================================

pipeline = run_signature_pipeline(

    observables,

    configuration["dt"],

)

if not isinstance(

    pipeline,

    dict,

):

    raise TypeError(

        "run_signature_pipeline() must return a dict."

    )


available_keys = list(

    pipeline.keys()

)


print()

print(

    "Pipeline keys:",

    available_keys,

)


if "signature" not in pipeline:

    raise KeyError(

        "Pipeline does not contain 'signature'. "

        f"Available keys: {available_keys}"

    )


signature = pipeline["signature"]


certificate = pipeline.get(

    "certificate",

    None,

)
        # ======================================================
    # Geometric trajectory
    # ======================================================

    if len(trajectory_vectors) == 0:

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
    # Dynamic geometry
    # ======================================================

    velocity = delta_sigma

    acceleration = 0.0

    turning_angle = 0.0

    curvature = 0.0


    if len(trajectory) > 0:

        acceleration = (

            velocity

            -

            trajectory[-1]["velocity"]

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


        if norm1 > 0.0 and norm2 > 0.0:

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

                norm2

            )


    # ======================================================
    # Local classification
    # ======================================================

    if velocity < 1e-10:

        stability = "stationary"

    elif curvature < 1e-4:

        stability = "stable"

    elif curvature < 1e-2:

        stability = "transition"

    else:

        stability = "bifurcation"


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

        "certificate":

            certificate,

        "vector":

            signature_vector,

        "delta_sigma":

            delta_sigma,

        "path_length":

            path_length,

        "velocity":

            velocity,

        "acceleration":

            acceleration,

        "turning_angle":

            turning_angle,

        "curvature":

            curvature,

        "stability":

            stability,

    }


    trajectory.append(

        record

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


    print(

        f"Dimension      : {len(signature_vector)}"

    )

    print(

        f"ΔSigma         : {delta_sigma:.8f}"

    )

    print(

        f"Path Length    : {path_length:.8f}"

    )

    print(

        f"Curvature      : {curvature:.8f}"

    )

    print(

        f"State          : {stability}"

    )


    experiment_index += 1

    sigma += SIGMA_STEP
    # ==========================================================
# End of experiment
# ==========================================================

print()

print("=" * 60)
print("Scan completed")
print("=" * 60)
print()

total_points = len(trajectory)

if total_points > 0:

    total_length = trajectory[-1]["path_length"]

    dimension = len(trajectory_vectors[0])

else:

    total_length = 0.0

    dimension = 0


stable_points = sum(

    1

    for r in trajectory

    if r["stability"] == "stable"

)

transition_points = sum(

    1

    for r in trajectory

    if r["stability"] == "transition"

)

bifurcation_points = sum(

    1

    for r in trajectory

    if r["stability"] == "bifurcation"

)

stationary_points = sum(

    1

    for r in trajectory

    if r["stability"] == "stationary"

)


summary = {

    "experiment": EXPERIMENT,

    "timestamp": TIMESTAMP,

    "points": total_points,

    "dimension": dimension,

    "sigma_start": SIGMA_START,

    "sigma_stop": SIGMA_STOP,

    "sigma_step": SIGMA_STEP,

    "trajectory_length": total_length,

    "stable_points": stable_points,

    "transition_points": transition_points,

    "bifurcation_points": bifurcation_points,

    "stationary_points": stationary_points,

}

save_json(

    "summary.json",

    summary,

)


# ==========================================================
# CSV
# ==========================================================

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

            "velocity",

            "acceleration",

            "turning_angle",

            "curvature",

            "stability",

        ]

    )

    for record in trajectory:

        writer.writerow(

            [

                record["index"],

                record["sigma"],

                record["delta_sigma"],

                record["path_length"],

                record["velocity"],

                record["acceleration"],

                record["turning_angle"],

                record["curvature"],

                record["stability"],

            ]

        )


# ==========================================================
# TXT Report
# ==========================================================

report_file = OUTPUT_DIR / "report.txt"

with open(

    report_file,

    "w",

    encoding="utf-8",

) as f:

    f.write("=" * 60 + "\n")

    f.write("GER\n")

    f.write("S29 E8\n")

    f.write("Signature Trajectory Experiment\n")

    f.write("=" * 60 + "\n\n")

    f.write(

        f"Timestamp              : {TIMESTAMP}\n"

    )

    f.write(

        f"Trajectory Points      : {total_points}\n"

    )

    f.write(

        f"Trajectory Dimension   : {dimension}\n"

    )

    f.write(

        f"Trajectory Length      : {total_length:.10f}\n"

    )

    f.write("\n")

    f.write(

        f"Stable Regions         : {stable_points}\n"

    )

    f.write(

        f"Transition Regions     : {transition_points}\n"

    )

    f.write(

        f"Bifurcation Regions    : {bifurcation_points}\n"

    )

    f.write(

        f"Stationary Regions     : {stationary_points}\n"

    )

    f.write("\n")

    f.write("Output Directory\n")

    f.write(

        str(OUTPUT_DIR)

    )

    f.write("\n")


print()

print("=" * 60)

print("Experiment finished")

print("=" * 60)

print()

print(

    f"Trajectory points : {total_points}"

)

print(

    f"Dimension         : {dimension}"

)

print(

    f"Path length       : {total_length:.8f}"

)

print(

    f"Stable            : {stable_points}"

)

print(

    f"Transitions       : {transition_points}"

)

print(

    f"Bifurcations      : {bifurcation_points}"

)

print(

    f"Output            : {OUTPUT_DIR}"

)

print()
