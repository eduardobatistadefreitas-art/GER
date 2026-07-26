"""
GER
S26-B36

Stationary Scan Runner

Pipeline oficial

Engine
    ↓
Persistence Observatory
    ↓
Geometry Signature
    ↓
Stationary Scan
    ↓
Structural Certificate

Este módulo apenas orquestra o pipeline.
Toda a lógica científica permanece encapsulada
nos respectivos módulos.
"""

from pprint import pprint

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26.S26_B36_geometry_scan import (
    generate_signature,
)

from GER_CORE.S26.S26_B36_stationary_scan import (
    stationary_scan,
)

from GER_CORE.S26.OPERATORS.result_manager import (
    save_json,
)

def run_B36_stationary_scan(
    beta=1.0,
    sigma=0.20,
    potential="A",
    timesteps=2000,
    dt=2.5e-4,
):

    print()
    print("=" * 70)
    print("GER")
    print("S26-B36")
    print("Stationary Scan")
    print("=" * 70)

    # --------------------------------------------------------
    # Engine
    # --------------------------------------------------------

    print()
    print("1) Running Engine...")

    engine = run_engine(
        beta=beta,
        sigma=sigma,
        potential=potential,
        timesteps=timesteps,
        dt=dt,
    )

    print("OK")

    # --------------------------------------------------------
    # Persistence Observatory
    # --------------------------------------------------------

    print()
    print("2) Running Persistence Observatory...")

    observables = run_persistence_observatory(
        engine["snapshots"],
        engine["configuration"]["dt"],
    )

    print("OK")

    # --------------------------------------------------------
    # Geometry Signature
    # --------------------------------------------------------

    print()
    print("3) Building Geometry Signature...")

    signature, trajectory_length = generate_signature(
        engine["snapshots"],
        engine["configuration"]["dt"],
    )

    print("OK")

    # --------------------------------------------------------
    # Stationary Scan
    # --------------------------------------------------------

    print()
    print("4) Running Stationary Scan...")

    certificate = stationary_scan(
        signature.to_dict()
    )

    print("OK")

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    result = {

        "configuration": {

            "beta": beta,
            "sigma": sigma,
            "potential": potential,
            "timesteps": timesteps,
            "dt": dt,

        },

        "trajectory_length": trajectory_length,

        "signature": signature.to_dict(),

        "certificate": certificate,

    }

    # --------------------------------------------------------
    # Relatório
    # --------------------------------------------------------

    print()

    print("=" * 70)
    print("Geometry Signature")
    print("=" * 70)

    pprint(
        signature.to_dict(),
        sort_dicts=False,
    )

    print()

    print("=" * 70)
    print("Structural Certificate")
    print("=" * 70)

    pprint(
        certificate,
        sort_dicts=False,
    )

    # --------------------------------------------------------
    # Salvamento
    # --------------------------------------------------------

    print()

    print("5) Saving results...")

    save_json(
        "S26_B36_stationary_scan",
        "stationary_scan",
        result,
    )

    print("OK")

    print()

    print("=" * 70)
    print("Stationary Scan Finished")
    print("=" * 70)

    return result

# ============================================================
# Execução direta
# ============================================================

def main():

    run_B36_stationary_scan()


# ============================================================

if __name__ == "__main__":

    main()
