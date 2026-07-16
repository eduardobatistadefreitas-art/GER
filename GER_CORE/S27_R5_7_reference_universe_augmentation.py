# ============================================================
# GER
#
# S27-R5.7
#
# Reference Universe Augmentation
#
# Inserts the external Lorenz signature into
# the official GER reference universe.
# ============================================================

from copy import deepcopy

from GER_CORE.S26_B36_geometry_scan import (
    run_geometry_scan,
)

from GER_CORE.S27_R5_5_geometric_signature import (
    generate_snapshots,
)

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

from GER.CORE.signature_api import Signature


# ============================================================
# Signature
# ============================================================

def generate_signature():

    snapshots = generate_snapshots()

    observables = run_persistence_observatory(
        snapshots,
        dt=1.0,
    )

    trajectory = build_trajectory(
        observables
    )

    diameter = compute_confinement(
        trajectory
    )

    convergence = compute_convergence(
        trajectory,
        1.0,
    )

    recurrence = compute_recurrence(
        trajectory
    )

    drift, trajectory_length = compute_drift(
        trajectory
    )

    signature = Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )

    return signature, trajectory_length


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R5.7")
    print("Reference Universe Augmentation")
    print("=" * 60)
    print()

    universe = deepcopy(
        run_geometry_scan()
    )

    print("Reference Universe")
    print("-" * 60)

    print(
        f"Internal signatures : {len(universe)}"
    )

    signature, length = generate_signature()

    universe.append({

        "simulation_id": "EXTERNAL",

        "system": "Lorenz Attractor",

        "beta": None,

        "sigma": None,

        "potential": None,

        "dt": 1.0,

        "window_size": 49,

        "diameter": signature.diameter,

        "convergence": signature.convergence,

        "recurrence": signature.recurrence,

        "drift": signature.drift,

        "trajectory_length": length,

        "signature": signature,

    })

    print()

    print("Augmented Universe")
    print("-" * 60)

    print(
        f"Total signatures : {len(universe)}"
    )

    print()

    print("Last entry")
    print("-" * 60)

    for key, value in universe[-1].items():

        print(f"{key:<20}{value}")

    print()

    print("=" * 60)
    print("STATUS : EXTERNAL SIGNATURE INSERTED")
    print("=" * 60)


if __name__ == "__main__":

    main()
