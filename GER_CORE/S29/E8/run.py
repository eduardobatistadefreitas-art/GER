"""
=============================================================
GER
S29_E8

Signature Trajectory Experiment
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
# Configuration
# ==========================================================

EXPERIMENT = "S29_E8"

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS"
)


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


def save_json(path, obj):

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

    try:

        from GER.CORE.ger_geometric_signature import (
            extract_signature,
        )

        extracted = extract_signature(signature)

    except Exception:

        extracted = signature


    if isinstance(extracted, dict):

        signature_dict = extracted

    elif hasattr(extracted, "to_dict"):

        signature_dict = extracted.to_dict()

    elif hasattr(extracted, "__dict__"):

        signature_dict = dict(extracted.__dict__)

    else:

        signature_dict = {

            "value": extracted

        }


    vector = []

    for key in sorted(signature_dict):

        value = signature_dict[key]

        if isinstance(value, (int, float)):

            vector.append(float(value))

    return signature_dict, vector


# ==========================================================
# Main Experiment
# ==========================================================

def run_experiment(

    sigma_start=0.1000,

    sigma_stop=0.2000,

    sigma_step=0.0001,

    n=384,

    timesteps=2000,

    dt=0.00025,

    beta=1.0,

    potential="A",

    snapshot_stride=50,

):

    initialize()

    timestamp = datetime.now().strftime(

        "%Y%m%d_%H%M%S"

    )

    output_dir = (

        RESULTS_ROOT

        / "S29"

        / EXPERIMENT

        / timestamp

    )

    output_dir.mkdir(

        parents=True,

        exist_ok=True,

    )

    print("=" * 60)
    print("GER")
    print("S29 E8")
    print("Signature Trajectory Experiment")
    print("=" * 60)
    print()

    trajectory = []

    trajectory_vectors = []

    sigma = sigma_start

    experiment_index = 0

    while sigma <= sigma_stop + 1e-12:

        print("-" * 60)

        print(

            f"Experiment {experiment_index}"

        )

        print(

            f"Sigma = {sigma:.6f}"

        )

        simulation = run_engine(

            n=n,

            timesteps=timesteps,

            dt=dt,

            beta=beta,

            potential=potential,

            snapshot_stride=snapshot_stride,

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

        if not isinstance(pipeline, dict):

            raise TypeError(

                "run_signature_pipeline() must return dict."

            )

        signature = pipeline["signature"]

        certificate = pipeline.get(

            "certificate",

            None,

        )

        signature_dict, signature_vector = normalize_signature(

            signature

        )

        # ==================================================
        # Trajectory metrics
        # ==================================================

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

        second_difference = 0.0
        
        second_difference_rate = 0.0

        if len(trajectory_vectors) >= 3:

            p1 = trajectory_vectors[-3]
            p2 = trajectory_vectors[-2]
            p3 = trajectory_vectors[-1]

            second_difference = math.sqrt(

                sum(

                    (c - 2 * b + a) ** 2

                    for a, b, c in zip(

                        p1,
                        p2,
                        p3,

                    )

                )

            )
            
        if len(trajectory) < 2:

            second_difference_rate = 0.0

        else:

            second_difference_rate = (

                second_difference

                -

                trajectory[-1]["second_difference"]

            )

        # ==================================================
        # Local geometric dynamics
        # ==================================================

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

                    max(

                        norm2,

                        1e-12,

                    )

                )

        # ==================================================
        # Local regime
        # ==================================================

        if velocity < 1e-10:

            stability = "stationary"

        elif curvature < 1e-4:

            stability = "stable"

        elif curvature < 1e-2:

            stability = "transition"

        else:

            stability = "bifurcation"

        # ==================================================
        # Store point
        # ==================================================

        record = {

            "index": experiment_index,

            "sigma": sigma,

            "signature": signature_dict,

            "certificate": certificate,

            "vector": signature_vector,

            "delta_sigma": delta_sigma,

            "path_length": path_length,

            "velocity": velocity,

            "acceleration": acceleration,

            "second_difference": second_difference,
            
            "second_difference_rate": second_difference_rate,

            "turning_angle": turning_angle,

            "curvature": curvature,

            "stability": stability,

        }

        trajectory.append(

            record

        )

        # ==================================================
        # Incremental checkpoint
        # ==================================================

        save_json(

            output_dir / "trajectory.json",

            trajectory,

        )

        save_json(

            output_dir / "trajectory_vectors.json",

            trajectory_vectors,

        )

        save_json(

            output_dir / "latest_record.json",

            record,

        )

        print(

            f"Dimension      : {len(signature_vector)}"

        )

        print(

            f"Delta Sigma    : {delta_sigma:.8f}"

        )

        print(

            f"Path Length    : {path_length:.8f}"

        )

        print(

            f"Curvature      : {curvature:.8f}"

        )

        print(
            
            f"Second Diff    : {second_difference:.8e}"
            
        )
        
        print(
            
            f"Second DiffRate: {second_difference_rate:.8e}"
            
        )

        print(

            f"State          : {stability}"

        )

        print()

        experiment_index += 1

        sigma += sigma_step

    # ==========================================================
    # End of scan
    # ==========================================================

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

        "timestamp": timestamp,

        "points": total_points,

        "dimension": dimension,

        "sigma_start": sigma_start,

        "sigma_stop": sigma_stop,

        "sigma_step": sigma_step,

        "trajectory_length": total_length,

        "stable_points": stable_points,

        "transition_points": transition_points,

        "bifurcation_points": bifurcation_points,

        "stationary_points": stationary_points,

    }


    save_json(

        output_dir / "summary.json",

        summary,

    )


    # ==========================================================
    # CSV Export
    # ==========================================================

    csv_file = output_dir / "trajectory.csv"

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
                
                "second_difference",
                
                "second_difference_rate",
                
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
            
                    record["second_difference"],
                    
                    record["second_difference_rate"],
                    
                    record["turning_angle"],
                    
                    record["curvature"],
                    
                    record["stability"],
                ]

            )


    # ==========================================================
    # Final report
    # ==========================================================

    report_file = output_dir / "report.txt"

    with open(

        report_file,

        "w",

        encoding="utf-8",

    ) as f:

        f.write("=" * 60 + "\n")

        f.write("GER\n")

        f.write("S29_E8\n")

        f.write("Signature Trajectory Experiment\n")

        f.write("=" * 60 + "\n\n")

        f.write(f"Timestamp              : {timestamp}\n")

        f.write(f"Trajectory points      : {total_points}\n")

        f.write(f"Trajectory dimension   : {dimension}\n")

        f.write(f"Trajectory length      : {total_length:.10f}\n")

        f.write(f"Sigma start            : {sigma_start}\n")

        f.write(f"Sigma stop             : {sigma_stop}\n")

        f.write(f"Sigma step             : {sigma_step}\n")

        f.write("\n")

        f.write(f"Stable                 : {stable_points}\n")

        f.write(f"Transition             : {transition_points}\n")

        f.write(f"Bifurcation            : {bifurcation_points}\n")

        f.write(f"Stationary             : {stationary_points}\n")

        f.write("\n")

        f.write("Output directory\n")

        f.write(str(output_dir))

        f.write("\n")


    print()

    print("=" * 60)

    print("Experiment finished")

    print("=" * 60)

    print()

    print(f"Trajectory points : {total_points}")

    print(f"Dimension         : {dimension}")

    print(f"Trajectory length : {total_length:.8f}")

    print(f"Output            : {output_dir}")

    print()


    return {

        "summary": summary,

        "trajectory": trajectory,

        "output_directory": output_dir,

    }


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    run_experiment()
