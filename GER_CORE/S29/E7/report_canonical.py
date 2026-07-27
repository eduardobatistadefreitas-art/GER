"""
GER - Geometria Espectral Relacional
S29 - E7.3

Canonical Object Report

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

from GER_CORE.S29.E7.canonical import (
    CanonicalAnalysis,
)


LINE = "=" * 60


def generate_canonical_report(
    analysis: CanonicalAnalysis,
) -> str:

    lines = []

    lines.append(LINE)
    lines.append("GER")
    lines.append("CANONICAL OBJECT ANALYSIS")
    lines.append(LINE)
    lines.append("")

    # ---------------------------------------------------------

    lines.append("CORE")
    lines.append("-" * 60)

    for component in analysis.components:

        if component.category == "CORE":

            lines.append(component.name)
            lines.append(f"Required : {component.required}")
            lines.append(f"Reason   : {component.reason}")
            lines.append("")

    # ---------------------------------------------------------

    lines.append("DERIVED")
    lines.append("-" * 60)

    for component in analysis.components:

        if component.category == "DERIVED":

            lines.append(component.name)
            lines.append(f"Required : {component.required}")
            lines.append(f"Reason   : {component.reason}")
            lines.append("")

    # ---------------------------------------------------------

    lines.append("METADATA")
    lines.append("-" * 60)

    for component in analysis.components:

        if component.category == "METADATA":

            lines.append(component.name)
            lines.append(f"Required : {component.required}")
            lines.append(f"Reason   : {component.reason}")
            lines.append("")

    # ---------------------------------------------------------

    if analysis.unknown_components:

        lines.append("UNKNOWN")
        lines.append("-" * 60)

        for component in analysis.components:

            if component.category == "UNKNOWN":

                lines.append(component.name)
                lines.append(f"Reason : {component.reason}")
                lines.append("")

    # ---------------------------------------------------------

    lines.append(LINE)

    lines.append(
        f"Canonical Core Size : {analysis.core_components}"
    )

    lines.append(
        f"Derived Components  : {analysis.derived_components}"
    )

    lines.append(
        f"Metadata Components : {analysis.metadata_components}"
    )

    lines.append(
        f"Unknown Components  : {analysis.unknown_components}"
    )

    lines.append(LINE)

    return "\n".join(lines)
