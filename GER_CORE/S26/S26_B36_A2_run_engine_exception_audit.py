# ============================================================
# GER
#
# S26-B36-A2
#
# Run Engine Exception Audit
#
# Verifica se run_engine lança exceções para
# alguma configuração padrão utilizada pelo
# Geometry Scan.
# ============================================================

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26_B36_geometry_scan import (
    DEFAULT_BETAS,
    DEFAULT_SIGMAS,
    DEFAULT_POTENTIALS,
)


# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S26-B36-A2")
    print("Run Engine Exception Audit")
    print("=" * 60)
    print()

    planned = (
        len(DEFAULT_BETAS)
        * len(DEFAULT_SIGMAS)
        * len(DEFAULT_POTENTIALS)
    )

    ok = 0
    failed = []

    for beta in DEFAULT_BETAS:

        for sigma in DEFAULT_SIGMAS:

            for potential in DEFAULT_POTENTIALS:

                try:

                    run_engine(

                        beta=beta,
                        sigma=sigma,
                        potential=potential,

                        timesteps=2000,
                        dt=2.5e-4,

                    )

                    ok += 1

                except Exception as exc:

                    failed.append(

                        (

                            beta,
                            sigma,
                            potential,
                            type(exc).__name__,
                            str(exc),

                        )

                    )

    print(f"Planned simulations : {planned}")
    print(f"run_engine OK       : {ok}")
    print(f"Exceptions          : {len(failed)}")
    print()

    if failed:

        print("Failed configurations")
        print("-" * 60)

        for beta, sigma, potential, etype, msg in failed:

            print(
                f"beta={beta}"
                f" sigma={sigma}"
                f" potential={potential}"
            )

            print(
                f"{etype}: {msg}"
            )

            print()

    print("=" * 60)

    print(
        "STATUS :",
        "PASS" if not failed else "FAIL",
    )

    print("=" * 60)


# ============================================================

if __name__ == "__main__":
    main()
