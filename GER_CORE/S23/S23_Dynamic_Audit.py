"""
=============================================================
GER
Relational Spectral Geometry

S23
Dynamic Audit

Consolidação dos experimentos:

    S23-D.1
    S23-D.2
    S23-D.3
    S23-E.1

Autor:
Eduardo Batista de Freitas

=============================================================
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import scipy.linalg as la
import scipy.stats as stats

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
)

from sklearn.metrics import (
    mean_squared_error,
    r2_score,
)

# ============================================================
# DIRETÓRIO DE RESULTADOS
# ============================================================

from pathlib import Path

try:

    from google.colab import drive

    drive.mount("/content/drive", force_remount=False)

    BASE_RESULTS = (
        Path("/content/drive/MyDrive")
        / "GER_RESULTS"
    )

except Exception:

    BASE_RESULTS = Path("GER_RESULTS")


RESULT_DIR = (
    BASE_RESULTS
    / "S23"
    / "S23_dynamic_audit"
)

RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ============================================================
# UTILITÁRIOS
# ============================================================

def save_json(filename, data):

    with open(
        RESULT_DIR / filename,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )


def save_csv(filename, header, rows):

    with open(
        RESULT_DIR / filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(header)

        writer.writerows(rows)


def save_txt(filename, text):

    with open(
        RESULT_DIR / filename,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(text)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def vetorizar_operador_quarta_ordem(
    tensor,
    n,
):

    matriz = np.zeros(
        (
            n * n,
            n * n,
        )
    )

    for i in range(n):
        for j in range(n):

            coluna = i + j * n

            for k in range(n):
                for l in range(n):

                    linha = k + l * n

                    matriz[
                        linha,
                        coluna,
                    ] = tensor[
                        k,
                        l,
                        i,
                        j,
                    ]

    return matriz


# ============================================================
# RECONSTRUÇÃO DO AMBIENTE RELACIONAL
# ============================================================

n = 6

np.random.seed(42)

# ------------------------------------------------------------
# Grafo relacional
# ------------------------------------------------------------

A_R = np.zeros(
    (
        n,
        n,
    )
)

for i in range(n):

    j = (i + 1) % n

    A_R[i, j] = 1.0
    A_R[j, i] = 1.0

# ------------------------------------------------------------
# Campo efetivo
# ------------------------------------------------------------

kappa_eff = (
    A_R
    * np.random.uniform(
        0.8,
        1.2,
        size=(
            n,
            n,
        ),
    )
)

# ------------------------------------------------------------
# Forma bilinear
# ------------------------------------------------------------

Gamma = (
    kappa_eff
    +
    (
        kappa_eff
        @
        kappa_eff
    ) / n
)

# ------------------------------------------------------------
# Curvatura espectral
# ------------------------------------------------------------

D = np.diag(
    np.sum(
        Gamma,
        axis=1,
    )
)

L = D - Gamma

Gamma_2 = L @ L

# ============================================================
# OPERADOR H_rel
# ============================================================

H_rel_tensor = np.zeros(
    (
        n,
        n,
        n,
        n,
    )
)

for i in range(n):
    for j in range(n):
        for k in range(n):
            for l in range(n):

                H_rel_tensor[
                    i,
                    j,
                    k,
                    l,
                ] = 1.0 / (
                    1
                    +
                    (i - k) ** 2
                    +
                    (j - l) ** 2
                )

H_rel_mat = vetorizar_operador_quarta_ordem(
    H_rel_tensor,
    n,
)

# ============================================================
# RESTRIÇÃO C_phi
# ============================================================

C_phi_tensor = np.zeros(
    (
        n,
        n,
        n,
        n,
    )
)

for i in range(n):

    C_phi_tensor[
        i,
        :,
        i,
        :
    ] = 1.0

C_phi_mat = vetorizar_operador_quarta_ordem(
    C_phi_tensor,
    n,
)

# ============================================================
# HESSIANO ELÁSTICO
# ============================================================

H_U_tensor = np.zeros(
    (
        n,
        n,
        n,
        n,
    )
)

for i in range(n):
    for j in range(n):

        H_U_tensor[
            i,
            j,
            i,
            j,
        ] = Gamma[
            i,
            j,
        ] ** 2

H_U_mat = vetorizar_operador_quarta_ordem(
    H_U_tensor,
    n,
)

# ============================================================
# PROJETOR RELACIONAL
# ============================================================

U, S, Vt = la.svd(
    H_U_mat
)

tol = 1e-5

modos_degenerados = Vt[
    S < tol
]

if modos_degenerados.shape[0] > 0:

    M = np.vstack(
        [
            C_phi_mat,
            modos_degenerados,
        ]
    )

else:

    M = C_phi_mat

P_R_star = (
    np.eye(n * n)
    -
    la.pinv(M)
    @
    M
)

# ============================================================
# GRADIENTE DISCRETO
# ============================================================

grad_tensor = np.zeros(
    (
        n,
        n,
        n,
        n,
    )
)

for i in range(n):
    for j in range(n):
        for k in range(n):
            for l in range(n):

                if (
                    i == k
                    or
                    j == l
                ):

                    grad_tensor[
                        i,
                        j,
                        k,
                        l,
                    ] = (
                        Gamma_2[
                            i,
                            j,
                        ]
                        -
                        Gamma_2[
                            k,
                            l,
                        ]
                    )

grad_Gamma2_mat = vetorizar_operador_quarta_ordem(
    grad_tensor,
    n,
)

# ============================================================
# OPERADOR RELACIONAL FINAL
# ============================================================

operador_central = (
    grad_Gamma2_mat
    @
    H_rel_mat
)

K_rel_star = (
    P_R_star
    @
    operador_central
    @
    P_R_star
)

# ============================================================
# DIAGNÓSTICO ESTRUTURAL
# ============================================================

audit = {

    "dimension": int(
        K_rel_star.shape[0]
    ),

    "projector_error": float(
        la.norm(
            P_R_star @ P_R_star
            -
            P_R_star
        )
    ),

    "symmetry_error": float(
        la.norm(
            P_R_star
            -
            P_R_star.T
        )
    ),

    "operator_asymmetry": float(
        la.norm(
            K_rel_star
            -
            K_rel_star.T
        )
    ),

}

save_json(
    "structural_audit.json",
    audit,
)
# ============================================================
# DINÂMICA TEMPORAL
# ============================================================

passos = 3000

dt = 0.001

amortecimento = 0.15

dim = K_rel_star.shape[0]

np.random.seed(123)

eta = np.random.normal(
    0.0,
    0.05,
    size=dim,
)

v = np.zeros(dim)

eta_hist = []
v_hist = []
a_hist = []

for _ in range(passos):

    forca = K_rel_star @ eta

    a = (
        -forca
        -
        amortecimento * v
    )

    # Euler semi-implícito

    v += dt * a

    eta += dt * v

    eta_hist.append(
        eta.copy()
    )

    v_hist.append(
        v.copy()
    )

    a_hist.append(
        a.copy()
    )

eta_hist = np.asarray(eta_hist)
v_hist = np.asarray(v_hist)
a_hist = np.asarray(a_hist)

# ============================================================
# AUDITORIA DA TRAJETÓRIA
# ============================================================

norma_eta = np.linalg.norm(
    eta_hist,
    axis=1,
)

norma_v = np.linalg.norm(
    v_hist,
    axis=1,
)

trajectory_audit = {

    "steps": int(passos),

    "dt": float(dt),

    "damping": float(amortecimento),

    "eta_initial": float(
        norma_eta[0]
    ),

    "eta_final": float(
        norma_eta[-1]
    ),

    "eta_max": float(
        np.max(norma_eta)
    ),

    "velocity_max": float(
        np.max(norma_v)
    ),

    "nan_detected": bool(
        np.any(
            np.isnan(eta_hist)
        )
    ),

    "overflow_detected": bool(
        np.max(norma_eta) > 1e8
    ),

}

save_json(
    "trajectory_audit.json",
    trajectory_audit,
)

# ============================================================
# ENERGIAS
# ============================================================

num_passos = len(
    eta_hist
)

Ecin = np.zeros(
    num_passos
)

Equad = np.zeros(
    num_passos
)

Epot = np.zeros(
    num_passos
)

Lyapunov = np.zeros(
    num_passos
)

for k in range(num_passos):

    x = eta_hist[k]

    vel = v_hist[k]

    Ecin[k] = (
        0.5
        *
        np.dot(
            vel,
            vel,
        )
    )

    Equad[k] = (
        0.5
        *
        x
        @
        K_rel_star
        @
        x
    )

    Epot[k] = (
        0.5
        *
        np.dot(
            x,
            x,
        )
    )

    Lyapunov[k] = (

        Ecin[k]

        +

        Equad[k]

        +

        Epot[k]

    )

delta_L = np.diff(
    Lyapunov
)

violacoes = int(
    np.sum(
        delta_L > 0
    )
)

lyapunov_audit = {

    "initial_value": float(
        Lyapunov[0]
    ),

    "final_value": float(
        Lyapunov[-1]
    ),

    "global_variation": float(
        Lyapunov[-1]
        -
        Lyapunov[0]
    ),

    "maximum_increment": float(
        np.max(delta_L)
    ),

    "minimum_increment": float(
        np.min(delta_L)
    ),

    "violations": violacoes,

}

save_json(
    "lyapunov_audit.json",
    lyapunov_audit,
)

save_csv(

    "energy_history.csv",

    [

        "step",

        "kinetic",

        "quadratic",

        "potential",

        "lyapunov",

    ],

    [

        [

            i,

            Ecin[i],

            Equad[i],

            Epot[i],

            Lyapunov[i],

        ]

        for i in range(num_passos)

    ],

)
# ============================================================
# AUDITORIA DA TRANSFERÊNCIA ENERGÉTICA
# ============================================================

nomes_candidatos = [

    "C1_eta_dot_v",

    "C2_v_dot_Keta",

    "C3_eta_dot_Kv",

    "C4_eta_norm2",

    "C5_v_norm2",

    "C6_eta_dot_Keta",

    "C7_a_dot_v",

    "C8_Keta_norm2",

]

C = np.zeros(
    (
        num_passos,
        8,
    )
)

for k in range(num_passos):

    eta = eta_hist[k]

    vel = v_hist[k]

    acc = a_hist[k]

    F = K_rel_star @ eta

    C[k, 0] = np.dot(
        eta,
        vel,
    )

    C[k, 1] = np.dot(
        vel,
        F,
    )

    C[k, 2] = np.dot(
        eta,
        K_rel_star @ vel,
    )

    C[k, 3] = np.dot(
        eta,
        eta,
    )

    C[k, 4] = np.dot(
        vel,
        vel,
    )

    C[k, 5] = np.dot(
        eta,
        F,
    )

    C[k, 6] = np.dot(
        acc,
        vel,
    )

    C[k, 7] = np.dot(
        F,
        F,
    )

C = C[:-1]

# ============================================================
# AUDITORIA ESTATÍSTICA
# ============================================================

ranking = []

for indice in range(8):

    x = C[:, indice]

    pearson = stats.pearsonr(
        x,
        delta_L,
    )[0]

    spearman = stats.spearmanr(
        x,
        delta_L,
    )[0]

    modelo = LinearRegression()

    modelo.fit(
        x.reshape(-1, 1),
        delta_L,
    )

    pred = modelo.predict(
        x.reshape(-1, 1)
    )

    R2 = r2_score(
        delta_L,
        pred,
    )

    mse = mean_squared_error(
        delta_L,
        pred,
    )

    ranking.append(

        {

            "candidate": nomes_candidatos[indice],

            "pearson": float(
                pearson
            ),

            "spearman": float(
                spearman
            ),

            "R2": float(
                R2
            ),

            "mse": float(
                mse
            ),

        }

    )

ranking = sorted(

    ranking,

    key=lambda r: abs(
        r["R2"]
    ),

    reverse=True,

)

# ============================================================
# EXPORTAÇÃO
# ============================================================

save_csv(

    "energy_candidates.csv",

    [

        "candidate",

        "pearson",

        "spearman",

        "R2",

        "mse",

    ],

    [

        [

            r["candidate"],

            r["pearson"],

            r["spearman"],

            r["R2"],

            r["mse"],

        ]

        for r in ranking

    ],

)

save_json(

    "energy_transfer_audit.json",

    {

        "best_candidate": ranking[0]["candidate"],

        "best_R2": ranking[0]["R2"],

        "best_pearson": ranking[0]["pearson"],

        "ranking": ranking,

    },

)

# ============================================================
# DADOS PARA A RECONSTRUÇÃO DE W
# ============================================================

X = C

y = delta_L

candidate_matrix = X

target_energy = y
# ============================================================
# RECONSTRUÇÃO DO TERMO W
# ============================================================

X = candidate_matrix

y = target_energy

modelos = {

    "Linear": LinearRegression(),

    "Ridge": Ridge(
        alpha=1.0
    ),

    "Lasso": Lasso(
        alpha=1e-6,
        max_iter=100000,
    ),

}

reconstruction_results = []

predictions = {}

best_model = None

best_r2 = -np.inf

best_prediction = None

best_coefficients = None

# ============================================================
# AJUSTE DOS MODELOS
# ============================================================

for nome, modelo in modelos.items():

    modelo.fit(
        X,
        y,
    )

    pred = modelo.predict(
        X
    )

    r2 = r2_score(
        y,
        pred,
    )

    mse = mean_squared_error(
        y,
        pred,
    )

    rmse = np.sqrt(
        mse
    )

    if hasattr(
        modelo,
        "coef_",
    ):

        coef = np.asarray(
            modelo.coef_
        )

    else:

        coef = np.zeros(
            X.shape[1]
        )

    reconstruction_results.append(

        {

            "model": nome,

            "R2": float(r2),

            "RMSE": float(rmse),

            "MSE": float(mse),

        }

    )

    predictions[nome] = pred

    if r2 > best_r2:

        best_r2 = r2

        best_model = nome

        best_prediction = pred.copy()

        best_coefficients = coef.copy()

# ============================================================
# IMPORTÂNCIA DOS MECANISMOS
# ============================================================

importance = []

for nome, coef in zip(
    nomes_candidatos,
    best_coefficients,
):

    importance.append(

        {

            "candidate": nome,

            "coefficient": float(coef),

            "absolute": float(
                abs(coef)
            ),

        }

    )

importance = sorted(

    importance,

    key=lambda x: x["absolute"],

    reverse=True,

)

# ============================================================
# EXPORTAÇÃO
# ============================================================

save_csv(

    "W_reconstruction_models.csv",

    [

        "model",

        "R2",

        "RMSE",

        "MSE",

    ],

    [

        [

            r["model"],

            r["R2"],

            r["RMSE"],

            r["MSE"],

        ]

        for r in reconstruction_results

    ],

)

save_csv(

    "W_coefficients.csv",

    [

        "candidate",

        "coefficient",

        "absolute",

    ],

    [

        [

            r["candidate"],

            r["coefficient"],

            r["absolute"],

        ]

        for r in importance

    ],

)

save_csv(

    "W_prediction.csv",

    [

        "delta_L",

        "prediction",

        "residual",

    ],

    [

        [

            y[i],

            best_prediction[i],

            y[i] - best_prediction[i],

        ]

        for i in range(len(y))

    ],

)

save_json(

    "W_reconstruction.json",

    {

        "best_model": best_model,

        "best_R2": float(best_r2),

        "importance": importance,

    },

)

# ============================================================
# VARIÁVEIS CONSOLIDADAS
# ============================================================

W_model = best_model

W_prediction = best_prediction

W_coefficients = best_coefficients

W_importance = importance
# ============================================================
# ANÁLISE ESPECTRAL DO OPERADOR
# ============================================================

K_sym = (
    K_rel_star
    +
    K_rel_star.T
) / 2.0

eigvals = la.eigvalsh(
    K_sym
)

positive_modes = eigvals[
    eigvals > 0
]

negative_modes = eigvals[
    eigvals < 0
]

spectral_summary = {

    "dimension": int(
        len(eigvals)
    ),

    "positive_modes": int(
        len(positive_modes)
    ),

    "negative_modes": int(
        len(negative_modes)
    ),

    "largest_positive": float(
        np.max(positive_modes)
        if len(positive_modes)
        else 0.0
    ),

    "most_negative": float(
        np.min(negative_modes)
        if len(negative_modes)
        else 0.0
    ),

    "spectral_center": float(
        np.mean(eigvals)
    ),

}

save_json(
    "spectral_summary.json",
    spectral_summary,
)

# ============================================================
# RENORMALIZAÇÃO ESPECTRAL
# ============================================================

alphas = np.array(

    [
        0,
        1,
        5,
        10,
        20,
        50,
        100,
        150,
    ]

)

renormalization_table = []

best_alpha = None

best_lambda = np.inf

for alpha in alphas:

    K_eff = (

        K_sym

        -

        alpha
        *
        np.eye(
            K_sym.shape[0]
        )

    )

    eig = la.eigvalsh(
        K_eff
    )

    lambda_max = np.max(eig)

    lambda_min = np.min(eig)

    positive_mass = np.sum(
        eig[eig > 0]
    )

    negative_mass = np.sum(
        np.abs(
            eig[eig < 0]
        )
    )

    renormalization_table.append(

        [

            alpha,

            lambda_max,

            lambda_min,

            positive_mass,

            negative_mass,

        ]

    )

    if lambda_max < best_lambda:

        best_lambda = lambda_max

        best_alpha = alpha

save_csv(

    "spectral_renormalization.csv",

    [

        "alpha",

        "lambda_max",

        "lambda_min",

        "positive_mass",

        "negative_mass",

    ],

    renormalization_table,

)

# ============================================================
# VALIDAÇÃO DINÂMICA
# ============================================================

K_eff = (

    K_rel_star

    -

    best_alpha
    *
    np.eye(
        dim
    )

)

K_eff = (

    K_eff

    +

    K_eff.T

) / 2.0

np.random.seed(2027)

n_tests = 20

validation = []

dt_validation = dt

steps_validation = passos

for _ in range(n_tests):

    eta = np.random.randn(
        dim
    ) * 0.1

    vel = np.zeros(
        dim
    )

    max_norm = 0.0

    for _ in range(
        steps_validation
    ):

        acc = (

            -K_eff @ eta

            -

            0.01 * vel

        )

        vel += dt_validation * acc

        eta += dt_validation * vel

        current = np.linalg.norm(
            eta
        )

        if current > max_norm:

            max_norm = current

    validation.append(

        [

            np.linalg.norm(
                eta
            ),

            max_norm,

        ]

    )

validation = np.asarray(
    validation
)

# ============================================================
# EXPOENTE DE SENSIBILIDADE
# ============================================================

eta1 = np.random.randn(
    dim
) * 0.1

eta2 = (

    eta1

    +

    1e-6
    *
    np.random.randn(dim)

)

v1 = np.zeros(dim)

v2 = np.zeros(dim)

d0 = np.linalg.norm(
    eta2 - eta1
)

for _ in range(
    steps_validation
):

    a1 = (

        -K_eff @ eta1

        -

        0.01 * v1

    )

    a2 = (

        -K_eff @ eta2

        -

        0.01 * v2

    )

    v1 += dt_validation * a1

    eta1 += dt_validation * v1

    v2 += dt_validation * a2

    eta2 += dt_validation * v2

df = np.linalg.norm(
    eta2 - eta1
)

lambda_dynamic = np.log(
    df / d0
) / (
    steps_validation
    *
    dt_validation
)

# ============================================================
# CERTIFICADO FINAL
# ============================================================

final_certificate = {

    "best_energy_model": W_model,

    "best_energy_R2": float(
        best_r2
    ),

    "best_candidate": ranking[0][
        "candidate"
    ],

    "best_candidate_R2": ranking[0][
        "R2"
    ],

    "spectral_shift": float(
        best_alpha
    ),

    "largest_eigenvalue_after_shift": float(
        best_lambda
    ),

    "dynamic_lambda": float(
        lambda_dynamic
    ),

    "mean_final_norm": float(
        np.mean(
            validation[:, 0]
        )
    ),

    "maximum_norm": float(
        np.max(
            validation[:, 1]
        )
    ),

}

save_json(
    "final_certificate.json",
    final_certificate,
)

save_csv(

    "dynamic_validation.csv",

    [

        "final_norm",

        "maximum_norm",

    ],

    validation,

)
# ============================================================
# RELATÓRIO FINAL
# ============================================================

summary = f"""
============================================================
GER
Relational Spectral Geometry

S23
Dynamic Audit
============================================================

RESULTADOS PRINCIPAIS

Melhor modelo para W
--------------------

Modelo : {W_model}
R²     : {best_r2:.6f}


Melhor candidato individual
---------------------------

{ranking[0]["candidate"]}

R²       : {ranking[0]["R2"]:.6f}
Pearson  : {ranking[0]["pearson"]:.6f}
Spearman : {ranking[0]["spearman"]:.6f}


Operador Relacional
-------------------

Dimensão                 : {audit["dimension"]}
Erro do projetor         : {audit["projector_error"]:.6e}
Erro de simetria         : {audit["symmetry_error"]:.6e}
Assimetria do operador   : {audit["operator_asymmetry"]:.6e}


Trajetória
----------

Passos              : {trajectory_audit["steps"]}
dt                  : {trajectory_audit["dt"]}
Amortecimento       : {trajectory_audit["damping"]}
Norma inicial       : {trajectory_audit["eta_initial"]:.6e}
Norma final         : {trajectory_audit["eta_final"]:.6e}
Norma máxima        : {trajectory_audit["eta_max"]:.6e}
Velocidade máxima   : {trajectory_audit["velocity_max"]:.6e}


Lyapunov
---------

Valor inicial       : {lyapunov_audit["initial_value"]:.6e}
Valor final         : {lyapunov_audit["final_value"]:.6e}
ΔL global           : {lyapunov_audit["global_variation"]:.6e}
Violações           : {lyapunov_audit["violations"]}


Espectro
---------

Centro espectral            : {spectral_summary["spectral_center"]:.6e}
Modos positivos             : {spectral_summary["positive_modes"]}
Modos negativos             : {spectral_summary["negative_modes"]}
Maior autovalor positivo    : {spectral_summary["largest_positive"]:.6e}
Menor autovalor             : {spectral_summary["most_negative"]:.6e}


Renormalização
--------------

Melhor α                   : {best_alpha}
Maior λ(Keff)              : {best_lambda:.6e}


Validação dinâmica
------------------

Lambda dinâmico            : {lambda_dynamic:.6e}

Norma média final          : {np.mean(validation[:,0]):.6e}

Maior norma observada      : {np.max(validation[:,1]):.6e}

============================================================
"""

save_txt(
    "summary.txt",
    summary,
)

# ============================================================
# INVENTÁRIO
# ============================================================

inventory = []

for file in sorted(
    RESULT_DIR.iterdir()
):

    inventory.append(

        {

            "name": file.name,

            "suffix": file.suffix,

            "size_bytes": file.stat().st_size,

        }

    )

save_json(
    "inventory.json",
    inventory,
)

# ============================================================
# CERTIFICADO GERAL
# ============================================================

experiment_certificate = {

    "series": "S23",

    "experiment": "Dynamic Audit",

    "status": "completed",

    "outputs": len(inventory),

    "result_directory": str(
        RESULT_DIR
    ),

    "files": [

        item["name"]

        for item in inventory

    ],

}

save_json(
    "experiment_certificate.json",
    experiment_certificate,
)

# ============================================================
# MAIN
# ============================================================

def main():

    print()

    print("=" * 60)

    print("GER — S23 Dynamic Audit")

    print("=" * 60)

    print()

    print("Experimento concluído.")

    print()

    print("Resultados salvos em:")

    print(RESULT_DIR)

    print()

    print(f"Arquivos gerados: {len(inventory)}")

    print()

    print(summary)


if __name__ == "__main__":

    main()
