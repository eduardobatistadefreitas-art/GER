# ============================================================
# GER
#
# S27-RA4
#
# Modal Embedding Candidates
#
# Theoretical audit of candidate modal
# representations compatible with the
# GER observational framework.
# ============================================================


def main():

    print("=" * 60)
    print("GER")
    print("S27-RA4")
    print("Modal Embedding Candidates")
    print("=" * 60)
    print()

    print("MINIMUM REQUIREMENTS")
    print("-" * 60)

    requirements = [

        "Complete state representation.",

        "Modal coefficients can be normalized.",

        "Modes possess an intrinsic ordering.",

        "Probability distribution can be constructed.",

        "Participation Ratio is well defined.",

        "Modal Center is well defined.",

        "Spectral Entropy is well defined.",

    ]

    for i, r in enumerate(requirements, start=1):

        print(f"{i}. {r}")

    print()

    print("CANDIDATE EMBEDDINGS")
    print("-" * 60)

    table = [

        ("Relational Laplacian",      "YES",      "Native GER representation"),

        ("Graph Laplacian",           "LIKELY",   "Equivalent spectral structure"),

        ("Fourier Basis",             "LIKELY",   "Ordered orthogonal modes"),

        ("Normal Modes",              "LIKELY",   "Physical modal decomposition"),

        ("Hamiltonian Eigenstates",   "LIKELY",   "Spectral representation"),

        ("Wavelets",                  "POSSIBLE", "Requires ordering criterion"),

        ("PCA",                       "POSSIBLE", "Ordering by explained variance"),

        ("SVD",                       "POSSIBLE", "Ordering by singular values"),

        ("Autoencoder Latent Space",  "UNKNOWN",  "Ordering not intrinsic"),

        ("Raw Time Series",           "NO",       "No modal representation"),

    ]

    print(f"{'Representation':<28}{'Status':<12}Comment")
    print("-" * 60)

    for name, status, comment in table:

        print(f"{name:<28}{status:<12}{comment}")

    print()

    print("WORKING HYPOTHESIS")
    print("-" * 60)

    print(
        "The GER observational framework may be applicable "
        "to any dynamical system admitting a modal "
        "representation satisfying the minimum "
        "requirements above."
    )

    print()

    print("=" * 60)
    print("STATUS : HYPOTHESIS UNDER INVESTIGATION")
    print("=" * 60)


if __name__ == "__main__":

    main()
