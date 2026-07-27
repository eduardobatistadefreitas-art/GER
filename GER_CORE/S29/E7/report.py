"""
============================================================
GER

S29 — E7.2

Structural Consistency Report

============================================================

Text report generator.

============================================================
"""

from __future__ import annotations

from .consistency import (
    ConsistencyResult,
)


# ============================================================
# Report
# ============================================================

def generate_consistency_report(
    result: ConsistencyResult,
) -> str:

    lines = []

    lines.append("=" * 60)
    lines.append("GER")
    lines.append("STRUCTURAL CONSISTENCY REPORT")
    lines.append("=" * 60)
    lines.append("")

    lines.append(
        f"Checked fields : {result.checked_fields}"
    )

    lines.append(
        f"Conflicts      : {len(result.conflicts)}"
    )

    lines.append(
        f"Warnings       : {len(result.warnings)}"
    )

    lines.append("")

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    lines.append("Overall Status")
    lines.append("-" * 60)

    if result.passed:

        lines.append("PASS")

    else:

        lines.append("FAIL")

    lines.append("")

    # --------------------------------------------------------
    # Conflicts
    # --------------------------------------------------------

    lines.append("Conflicts")
    lines.append("-" * 60)

    if not result.conflicts:

        lines.append("None")

    else:

        for i, conflict in enumerate(
            result.conflicts,
            start=1,
        ):

            lines.append(f"[{i}]")

            lines.append(
                f"Field       : {conflict.field}"
            )

            lines.append(
                f"Primary     : {conflict.primary_value}"
            )

            lines.append(
                f"Secondary   : {conflict.secondary_value}"
            )

            lines.append(
                f"Description : {conflict.description}"
            )

            lines.append("")

    # --------------------------------------------------------
    # Warnings
    # --------------------------------------------------------

    lines.append("Warnings")
    lines.append("-" * 60)

    if not result.warnings:

        lines.append("None")

    else:

        for i, warning in enumerate(
            result.warnings,
            start=1,
        ):

            lines.append(f"[{i}]")

            lines.append(
                f"Field       : {warning.field}"
            )

            lines.append(
                f"Description : {warning.description}"
            )

            lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)
