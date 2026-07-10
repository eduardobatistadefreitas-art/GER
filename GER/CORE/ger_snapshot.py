%%writefile GER_CORE/ger_snapshot.py

"""
=========================================================
GER CORE
Arquivo : ger_snapshot.py
=========================================================

Registro padronizado dos estados temporais da GER.

Cada snapshot representa uma fotografia completa
do sistema em um instante da evolução.

Responsabilidades:

• Métricas globais
• Observatório espectral
• Organização dos dados
"""

from __future__ import annotations


from GER_CORE.ger_metrics import (
    compute_hamiltonian,
    compute_l2_norm,
    compute_max_amplitude
)

from GER_CORE.ger_modal import (
    analyze_modal_state
)


# =========================================================
# Construção do Snapshot
# =========================================================

def build_snapshot(
    step,
    time,
    gamma,
    velocity,
    laplacian,
    beta,
    potential,
    eigenvectors,
    theta=None
):
    """
    Cria um registro completo do estado.

    Parameters
    ----------

    step :
        passo temporal

    time :
        tempo físico/numerico

    gamma :
        campo atual

    velocity :
        velocidade atual

    laplacian :
        operador discreto

    beta :
        intensidade não linear

    potential :
        tipo de potencial

    eigenvectors :
        base espectral
    """


    # -----------------------------
    # Métricas globais
    # -----------------------------

    energy = compute_hamiltonian(
        gamma,
        velocity,
        laplacian,
        beta,
        potential
    )

    l2 = compute_l2_norm(
        gamma
    )

    amplitude = compute_max_amplitude(
        gamma
    )


    # -----------------------------
    # Análise espectral
    # -----------------------------

    modal = analyze_modal_state(
        gamma,
        eigenvectors
    )


    # -----------------------------
    # Registro final
    # -----------------------------

    snapshot = {

        "step":
            step,

        "time":
            time,

        "energy":
            energy,

        "l2":
            l2,

        "amplitude":
            amplitude,

        "dominant_mode":
            modal["dominant_mode"],

        "modal_center":
            modal["modal_center"],

        "modal_width":
            modal["modal_width"],

        "spectral_entropy":
            modal["spectral_entropy"],

        "participation_ratio":
            modal["participation_ratio"],

        "probability":
            modal["probability"],

        "modal_energy":
            modal["modal_energy"],

        "spectral_bands":
            modal["spectral_bands"],

        "gamma":
            gamma.copy()
    }


    return snapshot
