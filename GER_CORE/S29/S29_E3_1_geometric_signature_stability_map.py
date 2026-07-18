"""
============================================================
GER
S29-E3.1

Geometric Signature Stability Map

Official RSG Experiment

This experiment performs a dense parameter scan of the Duffing
forcing parameter in order to investigate the intrinsic geometry
of the Relational Signature Space.

Author:
Eduardo Batista de Freitas

============================================================
"""

import os
import csv
import json
import time
import math
from datetime import datetime

import numpy as np

# ============================================================
# OFFICIAL GER IMPORTS
# ============================================================

from GER_CORE.S29.S29_E1_2_external_signature_generation import (
    initialize_signature_provider,
    run_external_signature_generation,
)

from GER_CORE.S29.external_systems.duffing import (
    simulate_duffing,
)

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIRECTORY = "/content/drive/MyDrive/GER_RESULTS"

CSV_FILE = os.path.join(
    OUTPUT_DIRECTORY,
    "S29_E3_1_signature_map.csv"
)

CHECKPOINT_FILE = os.path.join(
    OUTPUT_DIRECTORY,
    "S29_E3_1_checkpoint.json"
)

SUMMARY_FILE = os.path.join(
    OUTPUT_DIRECTORY,
    "S29_E3_1_summary.txt"
)

# ------------------------------------------------------------

GAMMA_INITIAL = 0.250
GAMMA_FINAL   = 0.500
GAMMA_STEP    = 0.005

DT = 0.01
DURATION = 100.0

# ------------------------------------------------------------

TOTAL_RUNS = int(
    round(
        (GAMMA_FINAL - GAMMA_INITIAL)
        / GAMMA_STEP
    )
) + 1

# ============================================================
# CSV HEADER
# ============================================================

CSV_HEADER = [

    "gamma",

    "diameter",

    "convergence",

    "recurrence",

    "drift"

]

# ============================================================
# SMALL UTILITIES
# ============================================================

def banner():

    print()
    print("=" * 60)
    print("GER")
    print("S29-E3.1")
    print("GEOMETRIC SIGNATURE STABILITY MAP")
    print("=" * 60)
    print()


def ensure_directory():

    os.makedirs(
        OUTPUT_DIRECTORY,
        exist_ok=True
    )


# ============================================================
# CHECKPOINT
# ============================================================

def checkpoint_exists():

    return os.path.exists(CHECKPOINT_FILE)


def load_checkpoint():

    if not checkpoint_exists():

        return 0

    with open(
        CHECKPOINT_FILE,
        "r"
    ) as f:

        data = json.load(f)

    return int(data["next_index"])


def save_checkpoint(index):

    data = {

        "next_index": int(index),

        "timestamp": str(datetime.now())

    }

    with open(
        CHECKPOINT_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# ============================================================
# CSV
# ============================================================

def create_csv_if_needed():

    if os.path.exists(CSV_FILE):

        return

    with open(
        CSV_FILE,
        "w",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow(CSV_HEADER)


def append_row(row):

    with open(
        CSV_FILE,
        "a",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow(row)

        f.flush()

        os.fsync(f.fileno())


# ============================================================
# GAMMA GRID
# ============================================================

def build_gamma_list():

    values = []

    g = GAMMA_INITIAL

    while g <= GAMMA_FINAL + 1e-12:

        values.append(
            round(g, 6)
        )

        g += GAMMA_STEP

    return values


# ============================================================
# TIME ESTIMATION
# ============================================================

def estimate_eta(

        start_time,

        completed

):

    if completed == 0:

        return "--"

    elapsed = time.time() - start_time

    average = elapsed / completed

    remaining = TOTAL_RUNS - completed

    eta = average * remaining

    hours = int(eta // 3600)

    minutes = int(
        (eta % 3600) // 60
    )

    seconds = int(
        eta % 60
    )

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def elapsed_string(start):

    elapsed = int(time.time() - start)

    h = elapsed // 3600

    m = (elapsed % 3600) // 60

    s = elapsed % 60

    return f"{h:02d}:{m:02d}:{s:02d}"

# ============================================================
# OFFICIAL PIPELINE EXECUTION
# ============================================================

def run_single_simulation(gamma):

    """
    Executes the complete official RSG pipeline
    for one Duffing parameter.
    """

    print()
    print("-" * 60)
    print(f"Gamma = {gamma:.3f}")
    print("-" * 60)

    # --------------------------------------------------------
    # External system
    # --------------------------------------------------------

    time, signal = simulate_duffing(
        dt=DT,
        duration=DURATION,
        gamma=float(gamma),
    )

    # --------------------------------------------------------
    # Complete official pipeline
    # --------------------------------------------------------

    result = run_external_signature_generation(
        system_name=f"Duffing (gamma={gamma:.3f})",
        time=time,
        signal=signal,
        dt=DT,
    )

    # --------------------------------------------------------
    # Signature extraction
    # --------------------------------------------------------

    s = result.signature

    return {

        "gamma": gamma,

        "diameter": float(s.diameter),

        "convergence": float(s.convergence),

        "recurrence": float(s.recurrence),

        "drift": float(s.drift),

    }


# ============================================================
# STORAGE
# ============================================================

def store_signature(data):

    append_row([

        data["gamma"],

        data["diameter"],

        data["convergence"],

        data["recurrence"],

        data["drift"]

    ])


# ============================================================
# LOADING RESULTS
# ============================================================

def load_results():

    if not os.path.exists(CSV_FILE):

        return []

    rows = []

    with open(CSV_FILE, "r") as f:

        reader = csv.DictReader(f)

        for row in reader:

            rows.append({

                "gamma": float(row["gamma"]),

                "diameter": float(row["diameter"]),

                "convergence": float(row["convergence"]),

                "recurrence": float(row["recurrence"]),

                "drift": float(row["drift"])

            })

    return rows


# ============================================================
# SIGNATURE MATRIX
# ============================================================

def signature_matrix(results):

    matrix = []

    for r in results:

        matrix.append([

            r["diameter"],

            r["convergence"],

            r["recurrence"],

            r["drift"]

        ])

    return np.asarray(matrix)


# ============================================================
# DISTANCE BETWEEN CONSECUTIVE SIGNATURES
# ============================================================

def consecutive_distances(matrix):

    distances = []

    for i in range(len(matrix)-1):

        d = np.linalg.norm(

            matrix[i+1] - matrix[i]

        )

        distances.append(float(d))

    return np.asarray(distances)


# ============================================================
# LOCAL VARIATIONS
# ============================================================

def local_variations(values):

    values = np.asarray(values)

    delta = np.diff(values)

    return np.abs(delta)

# ============================================================
# BASIC STATISTICS
# ============================================================

def compute_statistics(matrix):

    stats = {}

    names = [

        "Diameter",
        "Convergence",
        "Recurrence",
        "Drift"

    ]

    for i, name in enumerate(names):

        column = matrix[:, i]

        stats[name] = {

            "min": float(np.min(column)),
            "max": float(np.max(column)),
            "mean": float(np.mean(column)),
            "std": float(np.std(column)),
            "median": float(np.median(column))

        }

    return stats


# ============================================================
# CORRELATION MATRIX
# ============================================================

def correlation_matrix(matrix):

    return np.corrcoef(matrix.T)


# ============================================================
# LARGEST LOCAL VARIATIONS
# ============================================================

def largest_variations(results):

    report = {}

    fields = [

        "diameter",
        "convergence",
        "recurrence",
        "drift"

    ]

    for field in fields:

        values = np.asarray([r[field] for r in results])

        delta = np.abs(np.diff(values))

        idx = int(np.argmax(delta))

        report[field] = {

            "variation": float(delta[idx]),

            "gamma_1": results[idx]["gamma"],

            "gamma_2": results[idx + 1]["gamma"]

        }

    return report


# ============================================================
# SIGNATURE DISPLACEMENT
# ============================================================

def displacement_analysis(results):

    matrix = signature_matrix(results)

    distances = consecutive_distances(matrix)

    return {

        "all": distances,

        "mean": float(np.mean(distances)),

        "std": float(np.std(distances)),

        "max": float(np.max(distances)),

        "min": float(np.min(distances)),

        "index_max": int(np.argmax(distances)),

        "index_min": int(np.argmin(distances))

    }


# ============================================================
# LOCAL EXTREMA
# ============================================================

def detect_local_extrema(values):

    maxima = []

    minima = []

    for i in range(1, len(values) - 1):

        if values[i] > values[i-1] and values[i] > values[i+1]:

            maxima.append(i)

        if values[i] < values[i-1] and values[i] < values[i+1]:

            minima.append(i)

    return maxima, minima


# ============================================================
# GLOBAL EXTREMA REPORT
# ============================================================

def extrema_report(results):

    report = {}

    fields = [

        "diameter",
        "convergence",
        "recurrence",
        "drift"

    ]

    for field in fields:

        values = [r[field] for r in results]

        maxima, minima = detect_local_extrema(values)

        report[field] = {

            "maxima": maxima,

            "minima": minima

        }

    return report

# ============================================================
# SUMMARY REPORT
# ============================================================

def write_summary(results):

    matrix = signature_matrix(results)

    stats = compute_statistics(matrix)

    corr = correlation_matrix(matrix)

    jumps = largest_variations(results)

    displacement = displacement_analysis(results)

    extrema = extrema_report(results)

    with open(SUMMARY_FILE, "w") as f:

        f.write("=" * 60 + "\n")
        f.write("GER\n")
        f.write("S29-E3.1\n")
        f.write("GEOMETRIC SIGNATURE STABILITY MAP\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Generated : {datetime.now()}\n")
        f.write(f"Simulations : {len(results)}\n\n")

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        f.write("BASIC STATISTICS\n")
        f.write("-" * 60 + "\n")

        for observable in stats:

            s = stats[observable]

            f.write(f"\n{observable}\n")

            f.write(f"    Minimum : {s['min']:.12f}\n")
            f.write(f"    Maximum : {s['max']:.12f}\n")
            f.write(f"    Mean    : {s['mean']:.12f}\n")
            f.write(f"    Median  : {s['median']:.12f}\n")
            f.write(f"    Std Dev : {s['std']:.12f}\n")

        # ----------------------------------------------------
        # Correlation
        # ----------------------------------------------------

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("CORRELATION MATRIX\n")
        f.write("=" * 60 + "\n\n")

        names = [

            "Diameter",
            "Convergence",
            "Recurrence",
            "Drift"

        ]

        f.write("             ")

        for n in names:

            f.write(f"{n:>15}")

        f.write("\n")

        for i, name in enumerate(names):

            f.write(f"{name:12}")

            for j in range(4):

                f.write(f"{corr[i,j]:15.6f}")

            f.write("\n")

        # ----------------------------------------------------
        # Largest variations
        # ----------------------------------------------------

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("LARGEST LOCAL VARIATIONS\n")
        f.write("=" * 60 + "\n")

        for key in jumps:

            r = jumps[key]

            f.write("\n")

            f.write(f"{key.upper()}\n")

            f.write(
                f"    Gamma interval : "
                f"{r['gamma_1']:.3f}"
                f" -> "
                f"{r['gamma_2']:.3f}\n"
            )

            f.write(
                f"    Variation      : "
                f"{r['variation']:.12f}\n"
            )

        # ----------------------------------------------------
        # Displacement
        # ----------------------------------------------------

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("SIGNATURE DISPLACEMENT\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Mean displacement : {displacement['mean']:.12f}\n")
        f.write(f"Std displacement  : {displacement['std']:.12f}\n")
        f.write(f"Maximum           : {displacement['max']:.12f}\n")
        f.write(f"Minimum           : {displacement['min']:.12f}\n")

        imax = displacement["index_max"]
        imin = displacement["index_min"]

        f.write("\n")

        f.write(
            "Largest displacement between\n"
        )

        f.write(
            f"gamma = {results[imax]['gamma']:.3f}"
            " and "
            f"{results[imax+1]['gamma']:.3f}\n"
        )

        f.write("\n")

        f.write(
            "Smallest displacement between\n"
        )

        f.write(
            f"gamma = {results[imin]['gamma']:.3f}"
            " and "
            f"{results[imin+1]['gamma']:.3f}\n"
        )

        # ----------------------------------------------------
        # Extrema
        # ----------------------------------------------------

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("LOCAL EXTREMA\n")
        f.write("=" * 60 + "\n")

        for observable in extrema:

            f.write("\n")

            f.write(f"{observable.upper()}\n")

            f.write("Local maxima:\n")

            for idx in extrema[observable]["maxima"]:

                f.write(
                    f"    gamma = "
                    f"{results[idx]['gamma']:.3f}\n"
                )

            f.write("Local minima:\n")

            for idx in extrema[observable]["minima"]:

                f.write(
                    f"    gamma = "
                    f"{results[idx]['gamma']:.3f}\n"
                )

    print()
    print("=" * 60)
    print("Summary written successfully.")
    print("=" * 60)

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():

    banner()

    ensure_directory()

    create_csv_if_needed()

    gamma_values = build_gamma_list()

    if checkpoint_exists():

        start_index = load_checkpoint()

        print()
        print("Checkpoint detected.")
        print(f"Resuming from simulation {start_index+1}/{TOTAL_RUNS}")

    else:

        start_index = 0

        print()
        print("Starting new experiment.")

    start_time = time.time()

    # --------------------------------------------------------
    # Simulation Loop
    # --------------------------------------------------------

    initialize_signature_provider()

    for i in range(start_index, TOTAL_RUNS):

        gamma = gamma_values[i]

        print()
        print("=" * 60)
        print(f"Simulation {i+1} / {TOTAL_RUNS}")
        print("=" * 60)

        try:

            result = run_single_simulation(gamma)

            store_signature(result)

            save_checkpoint(i + 1)

            elapsed = elapsed_string(start_time)

            eta = estimate_eta(

                start_time,

                i - start_index + 1

            )

            print()

            print(
                f"Diameter    : {result['diameter']:.6f}"
            )

            print(
                f"Convergence : {result['convergence']:.6f}"
            )

            print(
                f"Recurrence  : {result['recurrence']:.6f}"
            )

            print(
                f"Drift       : {result['drift']:.6e}"
            )

            print()

            print(f"Elapsed : {elapsed}")

            print(f"ETA     : {eta}")

        except Exception as e:

            print()
            print("=" * 60)
            print("ERROR")
            print("=" * 60)

            print(e)

            print()

            print(
                "Checkpoint preserved."
            )

            print(
                "Restart the script to continue."
            )

            return

    # --------------------------------------------------------
    # Analysis
    # --------------------------------------------------------

    print()

    print("=" * 60)
    print("Loading complete dataset...")
    print("=" * 60)

    results = load_results()

    print()

    print(
        f"Loaded {len(results)} signatures."
    )

    print()

    print("=" * 60)
    print("Running geometric analysis...")
    print("=" * 60)

    write_summary(results)

    print()

    print("=" * 60)
    print("Experiment finished successfully.")
    print("=" * 60)

    print()

    print("CSV:")
    print(CSV_FILE)

    print()

    print("Summary:")
    print(SUMMARY_FILE)

# ============================================================
# CLEANUP
# ============================================================

def cleanup():

    """
    Removes the checkpoint after a successful execution.
    """

    if os.path.exists(CHECKPOINT_FILE):

        os.remove(CHECKPOINT_FILE)

        print()
        print("=" * 60)
        print("Checkpoint removed.")
        print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

        cleanup()

        print()
        print("=" * 60)
        print("S29-E3.1 COMPLETED")
        print("=" * 60)
        print()
        print("Output directory:")
        print(OUTPUT_DIRECTORY)
        print()
        print("Generated files:")
        print("  • S29_E3_1_signature_map.csv")
        print("  • S29_E3_1_summary.txt")
        print()

    except KeyboardInterrupt:

        print()
        print("=" * 60)
        print("Execution interrupted by user.")
        print("Checkpoint preserved.")
        print("=" * 60)

    except Exception as exc:

        print()
        print("=" * 60)
        print("UNEXPECTED ERROR")
        print("=" * 60)
        print(exc)
        print()
        print("Checkpoint preserved for recovery.")

  
