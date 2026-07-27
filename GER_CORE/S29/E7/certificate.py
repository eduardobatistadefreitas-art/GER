"""
============================================================
GER

S29 — E7

Structural Certificate

============================================================

Representação textual oficial de um DynamicRegime.

Este módulo não grava arquivos.
A persistência é responsabilidade do executável.

============================================================
"""

from __future__ import annotations

from datetime import datetime

from .model import DynamicRegime
from .serializer import dynamic_regime_to_dict


# ============================================================
# Certificate
# ============================================================

def generate_certificate(
    regime: DynamicRegime,
) -> str:
    """
    Gera o certificado estrutural em formato texto.
    """

    data = dynamic_regime_to_dict(regime)

    configuration = data["configuration"]
    signature = data["signature"]
    classification = data["classification"]
    audit = data["audit"]

    lines = []

    lines.append("=" * 60)
    lines.append("GER")
    lines.append("STRUCTURAL CERTIFICATE")
    lines.append("=" * 60)
    lines.append("")

    lines.append(
        f"Generated : {datetime.now().isoformat(timespec='seconds')}"
    )

    lines.append("")

    # --------------------------------------------------------

    lines.append("Configuration")
    lines.append("-" * 60)

    for key, value in configuration.items():
        lines.append(f"{key:20} : {value}")

    lines.append("")

    # --------------------------------------------------------

    lines.append("Geometric Signature")
    lines.append("-" * 60)

    for key, value in signature.items():
        lines.append(f"{key:20} : {value}")

    lines.append("")

    # --------------------------------------------------------

    lines.append("Classification")
    lines.append("-" * 60)

    for key, value in classification.items():
        lines.append(f"{key:20} : {value}")

    lines.append("")

    # --------------------------------------------------------

    lines.append("Audit")
    lines.append("-" * 60)

    for key, value in audit.items():
        lines.append(f"{key:20} : {value}")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
