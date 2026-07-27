"""
GER - Geometria Espectral Relacional
S29 - E7.4

Identity Report

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

from GER_CORE.S29.E7.identity import (
    IdentityComparison,
)


LINE = "=" * 60


def _status(value: bool) -> str:

    return "MATCH" if value else "DIFFERENT"


def generate_identity_report(
    comparison: IdentityComparison,
) -> str:

    lines = []

    lines.append(LINE)
    lines.append("GER")
    lines.append("RELATIONAL IDENTITY REPORT")
    lines.append(LINE)
    lines.append("")

    lines.append(
        f"Left Object  : {comparison.left}"
    )

    lines.append(
        f"Right Object : {comparison.right}"
    )

    lines.append("")

    # --------------------------------------------------------

    lines.append("Configuration")
    lines.append("-" * 60)
    lines.append(
        _status(
            comparison.configuration_match
        )
    )
    lines.append("")

    # --------------------------------------------------------

    lines.append("Signature")
    lines.append("-" * 60)
    lines.append(
        _status(
            comparison.signature_match
        )
    )
    lines.append("")

    # --------------------------------------------------------

    lines.append("Classification")
    lines.append("-" * 60)
    lines.append(
        _status(
            comparison.classification_match
        )
    )
    lines.append("")

    # --------------------------------------------------------

    lines.append("Audit")
    lines.append("-" * 60)
    lines.append(
        _status(
            comparison.audit_match
        )
    )
    lines.append("")

    # --------------------------------------------------------

    lines.append(LINE)

    lines.append("Canonical Identity")

    lines.append("-" * 60)

    if comparison.canonical_identity:

        lines.append("SAME CANONICAL OBJECT")

    else:

        lines.append("DIFFERENT CANONICAL OBJECTS")

    lines.append("")

    lines.append(LINE)

    return "\n".join(lines)
