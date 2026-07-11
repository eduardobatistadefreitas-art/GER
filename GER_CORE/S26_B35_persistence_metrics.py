%%writefile GER_CORE/S26_B35_persistence_metrics.py

import numpy as np


# ============================================================
# S26-B35
# Persistence Observatory
#
# Observáveis:
# Rloc
# Dspec
# Hshape
# Cauto
# Rmacro
# Entropia auxiliar
# ============================================================


def safe_normalize(x):

    norm = np.linalg.norm(x)

    if norm < 1e-15:
        return x * 0.0

    return x / norm


# ------------------------------------------------------------
# 1) Resíduo local temporal
# ------------------------------------------------------------

def compute_Rloc(
    gamma_prev,
    gamma_now,
    dt
):

    numerator = np.linalg.norm(
        gamma_now - gamma_prev
    )

    denominator = (
        dt *
        np.linalg.norm(gamma_now)
        + 1e-15
    )

    return numerator / denominator


# ------------------------------------------------------------
# 2) Divergência espectral Jensen-Shannon
# ------------------------------------------------------------

def compute_Dspec(
    p_prev,
    p_now
):

    p_prev = np.asarray(p_prev)
    p_now = np.asarray(p_now)

    m = 0.5 * (
        p_prev + p_now
    )

    def kl(p, q):

        mask = p > 0

        return np.sum(
            p[mask] *
            np.log(
                p[mask] /
                (q[mask] + 1e-15)
            )
        )

    return 0.5 * (
        kl(p_prev, m)
        +
        kl(p_now, m)
    )


# ------------------------------------------------------------
# 3) Variação do Participation Ratio
# ------------------------------------------------------------

def compute_Hshape(
    PR_prev,
    PR_now,
    dt
):

    return (
        PR_now - PR_prev
    ) / dt


# ------------------------------------------------------------
# 4) Coerência com estado inicial
# ------------------------------------------------------------

def compute_Cauto(
    gamma_initial,
    gamma_now
):

    a = np.linalg.norm(
        gamma_initial
    )

    b = np.linalg.norm(
        gamma_now
    )

    if a < 1e-15 or b < 1e-15:
        return 0.0

    return np.dot(
        gamma_initial,
        gamma_now
    ) / (a * b)


# ------------------------------------------------------------
# 5) Deslocamento do centro modal
# ------------------------------------------------------------

def compute_Rmacro(
    center_prev,
    center_now,
    dt,
    n
):

    return abs(
        center_now - center_prev
    ) / (
        dt * n
    )


# ------------------------------------------------------------
# 6) Entropia espectral auxiliar
# ------------------------------------------------------------

def compute_entropy(
    probability
):

    p = np.asarray(
        probability
    )

    mask = p > 0

    n = len(p)

    if n <= 1:
        return 0.0

    S = -np.sum(
        p[mask] *
        np.log(
            p[mask]
        )
    )

    return S / np.log(n)


# ------------------------------------------------------------
# Observatório completo
# ------------------------------------------------------------

def run_persistence_observatory(
    snapshots,
    dt
):

    results = {

        "Rloc": [],
        "Dspec": [],
        "Hshape": [],
        "Cauto": [],
        "Rmacro": [],
        "entropy": []

    }

    gamma_initial = np.asarray(
        snapshots[0]["gamma"]
    )

    for i in range(
        1,
        len(snapshots)
    ):

        prev = snapshots[i - 1]
        now = snapshots[i]

        gamma_prev = np.asarray(
            prev["gamma"]
        )

        gamma_now = np.asarray(
            now["gamma"]
        )

        results["Rloc"].append(

            compute_Rloc(
                gamma_prev,
                gamma_now,
                dt
            )

        )

        results["Dspec"].append(

            compute_Dspec(
                prev["probability"],
                now["probability"]
            )

        )

        results["Hshape"].append(

            compute_Hshape(
                prev["participation_ratio"],
                now["participation_ratio"],
                dt
            )

        )

        results["Cauto"].append(

            compute_Cauto(
                gamma_initial,
                gamma_now
            )

        )

        results["Rmacro"].append(

            compute_Rmacro(
                prev["modal_center"],
                now["modal_center"],
                dt,
                len(gamma_now)
            )

        )

        results["entropy"].append(

            compute_entropy(
                now["probability"]
            )

        )

    return results
