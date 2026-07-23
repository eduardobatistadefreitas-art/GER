# ============================================================
# GER
#
# S27-R5.6
#
# Structural Certificate
#
# First external Structural Certificate
# generated for the Lorenz Attractor.
# ============================================================

from GER.CORE.signature_api import Signature

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

from GER_CORE.S26_B36_stationary_scan import (
    stationary_scan,
)


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

    drift, _ = compute_drift(
        trajectory
    )

    return Signature(

        diameter=diameter,

        convergence=convergence,

        recurrence=recurrence,

        drift=drift,

    )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-R5.6")
    print("Structural Certificate")
    print("=" * 60)
    print()

    signature = generate_signature()

    certificate = stationary_scan(
        signature
    )

    print("Signature")
    print("-" * 60)

    print(signature)

    print()

    print("Certificate summary")
    print("-" * 60)

    print(
        certificate["summary"]
    )

    print()

    print("Deductions")
    print("-" * 60)

    for deduction in certificate["deductions"]:

        print(deduction)

    print()

    print("=" * 60)
    print("STATUS : FIRST LORENZ STRUCTURAL CERTIFICATE")
    print("=" * 60)


if __name__ == "__main__":

    main()
