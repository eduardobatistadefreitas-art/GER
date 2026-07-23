# ============================================================
# GER
#
# S27-RA3
#
# External Modal Embedding
#
# Architectural specification.
#
# No implementation is performed in this stage.
#
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-RA3")
    print("External Modal Embedding")
    print("=" * 60)
    print()

    print("QUESTION")
    print("-" * 60)
    print(
        "Which mathematical structure must an external "
        "dynamic system provide in order to be observed "
        "by the GER framework?"
    )

    print()

    print("CURRENT GER PIPELINE")
    print("-" * 60)

    print("""
gamma
    ↓
Relational Laplacian
    ↓
Eigenvectors
    ↓
Modal State
    ↓
Snapshot
    ↓
Persistence Observatory
""")

    print()

    print("GENERALIZED PIPELINE")
    print("-" * 60)

    print("""
External Dynamic System
    ↓
State Representation
    ↓
Generator Operator
    ↓
Modal Basis
    ↓
Modal Coefficients
    ↓
GER Snapshot
    ↓
Persistence Observatory
""")

    print()

    print("OPEN QUESTIONS")
    print("-" * 60)

    questions = [

        "What is the minimal definition of a Modal Basis?",

        "Must the Generator Operator be symmetric?",

        "Must the basis be orthogonal?",

        "Can modal coefficients come from Fourier, Laplacian, PCA or other decompositions?",

        "Which mathematical properties are actually required by the GER observatory?",

    ]

    for i, q in enumerate(questions, start=1):

        print(f"{i}. {q}")

    print()

    print("=" * 60)
    print("STATUS : ARCHITECTURAL RFC")
    print("=" * 60)


if __name__ == "__main__":
    main()
