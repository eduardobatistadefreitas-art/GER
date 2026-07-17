"""
=========================================================
GER
S29-E1.0

Identity Architecture Validation

Validates the complete external pipeline using the
Identity Embedding.

Expected flow:

External System
    ↓
Identity Embedding
    ↓
Gamma Sequence
=========================================================
"""

from GER_CORE.S29.harmonic_system import (
    HarmonicSystem,
)

from GER_CORE.S29.identity_embedding import (
    IdentityEmbedding,
)

from GER_CORE.S29.external_pipeline import (
    ExternalPipeline,
)


def main():

    print("=" * 60)
    print("GER")
    print("S29-E1.0")
    print("Identity Architecture Validation")
    print("=" * 60)
    print()

    system = HarmonicSystem(
        samples=10
    )

    embedding = IdentityEmbedding()

    pipeline = ExternalPipeline(
        system,
        embedding,
    )

    gamma_sequence = pipeline.run()

    print("Generated relational states")
    print("-" * 60)

    print(f"Total states : {len(gamma_sequence)}")

    print()

    print("First five states")

    for gamma in gamma_sequence[:5]:
        print(gamma)

    print()

    print("=" * 60)
    print("STATUS : PASS")
    print("=" * 60)


if __name__ == "__main__":
    main()
