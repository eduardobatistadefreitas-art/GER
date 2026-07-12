import numpy as np

# ============================================================
# S26-B36
# Stationary Scan
#
# Classificação algorítmica de regimes
# baseada no observatório B35 - Corrigida para Robustez
# ============================================================

def linear_slope(values):
    values = np.asarray(values)
    if len(values) < 2:
        return 0.0
    x = np.arange(len(values))
    coef = np.polyfit(x, values, 1)
    return coef[0]

def mean_abs(x):
    return np.mean(np.abs(np.asarray(x)))

def compute_persistence_score(Rloc, Dspec, Hshape, Cauto, dt):
    return np.abs(Cauto) * np.exp(-(dt * Rloc + Dspec + dt * np.abs(Hshape)))

def stationary_scan(observables, dt, K=None, epsilon=1e-8):
    if K is None:
        K = len(observables["Rloc"])

    data = {}
    for key in observables:
        data[key] = np.asarray(observables[key])[-K:]

    # -------------------------
    # Estatísticas
    # -------------------------
    statistics = {
        "mean_Rloc": np.mean(data["Rloc"]),
        "mean_Dspec": np.mean(data["Dspec"]),
        "mean_Hshape": mean_abs(data["Hshape"]),
        "var_Rloc": np.var(data["Rloc"]),
        "var_Dspec": np.var(data["Dspec"]),
        "slope_Rmacro": linear_slope(data["Rmacro"]),
        "slope_Cauto": linear_slope(data["Cauto"]),
        "slope_entropy": linear_slope(data["entropy"])
    }

    # -------------------------
    # Persistence score
    # -------------------------
    P = []
    for i in range(len(data["Rloc"])):
        P.append(
            compute_persistence_score(
                data["Rloc"][i],
                data["Dspec"][i],
                data["Hshape"][i],
                data["Cauto"][i],
                dt
            )
        )
    P = np.asarray(P)

    statistics["mean_P"] = np.mean(P)
    statistics["var_P"] = np.var(P)

    # -------------------------
    # Classificação Corrigida
    # -------------------------
    # 1. Instável: Se a variância local explodir
    if statistics["var_Rloc"] > 1 / epsilon:
        regime = "INSTAVEL"
        
    # 2. Persistente: Score de persistência quase perfeito e variância residual
    elif statistics["mean_P"] > (1.0 - epsilon) and statistics["var_P"] < epsilon:
        regime = "PERSISTENTE"
        
    # 3. Oscilatório: A persistência é alta/estável, mas a variância espectral indica ciclos ativos
    elif statistics["var_P"] > 0.0 and statistics["var_Dspec"] > 1e-15:
        regime = "OSCILATORIO"
        
    # 4. Transitório: Caso padrão de evolução suave
    else:
        regime = "TRANSITORIO"

    return {
        "regime": regime,
        "persistence_score": statistics["mean_P"],
        "persistence_variance": statistics["var_P"],
        "statistics": statistics,
        "persistence_history": P
    }
    
# ============================================================
# API pública oficial do GER
# ============================================================

def run_stationary_scan(*args, **kwargs):
    """
    Interface pública oficial do Stationary Scan.
    """
    return stationary_scan(*args, **kwargs)
