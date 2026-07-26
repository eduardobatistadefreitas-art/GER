# ============================================================
# GER
#
# GER_CORE/S26/run_B36_stationary_scan.py
#
# Official Runner
#
# S26-B36
# Stationary Scan
#
# Pipeline:
#
# Engine
#     ↓
# Persistence Observatory
#     ↓
# Geometry Scan
#     ↓
# Geometric Signature
#     ↓
# Stationary Scan
#     ↓
# Structural Certificate
#
# ============================================================

import json
import os
from datetime import datetime

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_geometry_scan import (
    build_trajectory,
    compute_confinement,
    compute_convergence,
    compute_recurrence,
    compute_drift,
)

from GER_CORE.S26_B36_stationary_scan import (
    stationary_scan,
)

from GER.CORE.signature_api import Signature

from GER_CORE.S26.OPERATORS.result_manager import (
    save_json,
)


# ============================================================
# Runner
# ============================================================

def run_B36_stationary_scan(
    beta=1.0,
    sigma=0.20,
    potential="A",
    timesteps=2000,
    dt=2.5e-4,
):

    print("=" * 70)
    print("GER")
    print("S26-B36")
    print("STATIONARY SCAN")
    print("=" * 70)
    print()

    # --------------------------------------------------------
    # Engine
    # --------------------------------------------------------

    result = run_engine(
        beta=beta,
        sigma=sigma,
        potential=potential,
        timesteps=timesteps,
        dt=dt,
    )

    # --------------------------------------------------------
    # Persistence Observatory
    # --------------------------------------------------------

    observables = run_persistence_observatory(
        result["snapshots"],
        result["configuration"]["dt"],
    )

    # --------------------------------------------------------
    # Trajectory
    # --------------------------------------------------------

    trajectory = build_trajectory(
        observables
    )

    # --------------------------------------------------------
    # Geometry Operators
    # --------------------------------------------------------

    diameter = compute_confinement(
        trajectory
    )

    convergence = compute_convergence(
        trajectory,
        result["configuration"]["dt"],
    )

    recurrence = compute_recurrence(
        trajectory
    )

    drift, trajectory_length = compute_drift(
        trajectory
    )

    # --------------------------------------------------------
    # Geometric Signature
    # --------------------------------------------------------

    signature = Signature(
        diameter=diameter,
        convergence=convergence,
        recurrence=recurrence,
        drift=drift,
    )

    # --------------------------------------------------------
    # Structural Certificate
    # --------------------------------------------------------

    certificate = stationary_scan(
        signature.to_dict()
    )

    # --------------------------------------------------------
    # Final Result
    # --------------------------------------------------------

    output = {

        "timestamp": datetime.now().isoformat(),

        "configuration": {

            "beta": beta,
            "sigma": sigma,
            "potential": potential,
            "timesteps": timesteps,
            "dt": dt,

        },

        "signature": signature.to_dict(),

        "trajectory_length": trajectory_length,

        "certificate": certificate,

    }

    save_json(

        "S26_B36_stationary_scan",

        "stationary_scan",

        output,

    )

    print("Geometry Signature")
    print("------------------------------")
    print(signature)
    print()

    print("Structural Certificate")
    print("------------------------------")
    print(
        certificate["summary"]
    )
    print()

    print("=" * 70)
    print("Experiment completed.")
    print("=" * 70)

    return output


# ============================================================
# Main
# ============================================================

def main():

    run_B36_stationary_scan()


# ============================================================

if __name__ == "__main__":

    main()
