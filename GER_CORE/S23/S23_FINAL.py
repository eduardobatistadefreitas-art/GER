"""
=============================================================
S23_FINAL.py
=============================================================

GER — Geometria Espectral Relacional

S23
Validação Dinâmica da Renormalização Espectral

Versão:
    Produção

Autor:
    Eduardo Batista de Freitas

Descrição
----------
Reconstrução oficial do experimento S23 a partir da versão
consolidada do programa de pesquisa.

Esta implementação substitui o notebook histórico por um
experimento único reproduzível.

Resultados são gravados automaticamente em:

    GER_RESULTS/S23_FINAL/

=============================================================
"""

from __future__ import annotations

import csv
import json
import time
import warnings

from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.linalg as la
from scipy.integrate import solve_ivp

warnings.filterwarnings("ignore")

# ============================================================
# METADADOS
# ============================================================

EXPERIMENT = "S23_FINAL"

TITLE = "Dynamic Validation of Spectral Renormalization"

AUTHOR = "Eduardo Batista de Freitas"

VERSION = "1.0"

START_TIME = time.time()

# ============================================================
# NUMPY
# ============================================================

np.set_printoptions(
    precision=10,
    suppress=True,
    linewidth=200
)

RNG = np.random.default_rng(42)

# ============================================================
# GOOGLE COLAB
# ============================================================

IN_COLAB = False

try:

    import google.colab

    from google.colab import drive

    drive.mount("/content/drive")

    IN_COLAB = True

except Exception:

    pass

# ============================================================
# DIRETÓRIOS
# ============================================================

if IN_COLAB:

    ROOT = Path(
        "/content/drive/MyDrive/GER_RESULTS"
    )

else:

    ROOT = Path("GER_RESULTS")

RESULTS = ROOT / EXPERIMENT

DATA = RESULTS / "data"

FIGURES = RESULTS / "figures"

REPORTS = RESULTS / "reports"

for folder in [

    ROOT,
    RESULTS,
    DATA,
    FIGURES,
    REPORTS

]:

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

# ============================================================
# LOGGER
# ============================================================

LOGFILE = REPORTS / "execution.log"

def log(text=""):

    stamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    line = f"[{stamp}] {text}"

    print(line)

    with open(

        LOGFILE,

        "a",

        encoding="utf8"

    ) as f:

        f.write(line + "\n")

# ============================================================
# SUMMARY
# ============================================================

SUMMARY = []

def write(text=""):

    print(text)

    SUMMARY.append(str(text))

def save_summary():

    with open(

        REPORTS / "summary.txt",

        "w",

        encoding="utf8"

    ) as f:

        f.write("\n".join(SUMMARY))

# ============================================================
# JSON
# ============================================================

def save_json(name, obj):

    with open(

        REPORTS / name,

        "w",

        encoding="utf8"

    ) as f:

        json.dump(

            obj,

            f,

            indent=4,

            ensure_ascii=False

        )

# ============================================================
# CSV
# ============================================================

def save_dataframe(name, df):

    df.to_csv(

        DATA / name,

        index=False

    )

# ============================================================
# NUMPY
# ============================================================

def save_array(name, array):

    np.save(

        DATA / name,

        array

    )

# ============================================================
# FIGURAS
# ============================================================

def save_figure(name):

    plt.tight_layout()

    plt.savefig(

        FIGURES / name,

        dpi=300,

        bbox_inches="tight"

    )

    plt.close()

# ============================================================
# REGISTRO DE RESULTADOS
# ============================================================

class S23Results:

    def __init__(self):

        self.results = {}

    def record(self, key, value):

        if isinstance(value, np.ndarray):

            value = value.tolist()

        elif isinstance(value, np.generic):

            value = value.item()

        self.results[key] = value

    def save(self):

        report = {

            "experiment": EXPERIMENT,

            "title": TITLE,

            "author": AUTHOR,

            "version": VERSION,

            "date": datetime.now().isoformat(),

            "execution_time_seconds":

                round(

                    time.time() - START_TIME,

                    3

                ),

            "results":

                self.results

        }

        save_json(

            "report.json",

            report

        )

results = S23Results()

# ============================================================
# CONSTANTES DO EXPERIMENTO
# ============================================================

ALPHA = 150.0

DT = 0.01

NSTEPS = 3000

TMAX = DT * NSTEPS

SEED = 42

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================

K_rel_star = None

K_eff = None

P_R_star = None

eta_hist = None

v_hist = None

a_hist = None

# ============================================================
# CABEÇALHO
# ============================================================

log("=" * 60)
log("GER")
log(EXPERIMENT)
log("=" * 60)

log(f"Título : {TITLE}")
log(f"Versão : {VERSION}")
log(f"Autor  : {AUTHOR}")

log(f"Colab  : {IN_COLAB}")

log(f"Saída  : {RESULTS}")

log("=" * 60)

write("=" * 60)
write("GER")
write(EXPERIMENT)
write("=" * 60)
write("")
write(TITLE)
write("")

results.record("version", VERSION)
results.record("alpha", ALPHA)
results.record("dt", DT)
results.record("steps", NSTEPS)

log("Infraestrutura inicializada.")

# ============================================================
# PARTE 2
# RECONSTRUÇÃO DO AMBIENTE RELACIONAL
# (Adaptado do S23-C.2-A)
# ============================================================

log("")
log("=" * 60)
log("PARTE 2")
log("Reconstrução do ambiente relacional")
log("=" * 60)

# ------------------------------------------------------------
# Ambiente discreto
# ------------------------------------------------------------

def inicializar_ambiente(
    n=6,
    seed=SEED
):

    np.random.seed(seed)

    # --------------------------------------------------------
    # Grafo relacional (anel)
    # --------------------------------------------------------

    A_R = np.zeros((n, n))

    for i in range(n):

        j = (i + 1) % n

        A_R[i, j] = 1.0
        A_R[j, i] = 1.0

    # --------------------------------------------------------
    # Campo efetivo
    # --------------------------------------------------------

    kappa_eff = np.random.uniform(
        0.8,
        1.2,
        size=(n, n)
    )

    kappa_eff = (
        kappa_eff +
        kappa_eff.T
    ) / 2

    np.fill_diagonal(
        kappa_eff,
        0.0
    )

    # --------------------------------------------------------
    # Laplaciano
    # --------------------------------------------------------

    D = np.diag(
        np.sum(A_R, axis=1)
    )

    Gamma = D - A_R

    Gamma_2 = Gamma @ Gamma

    # --------------------------------------------------------
    # Tensores
    # --------------------------------------------------------

    H_rel = np.zeros(
        (n, n, n, n)
    )

    C_phi = np.zeros_like(
        H_rel
    )

    H_U = np.zeros_like(
        H_rel
    )

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):

                    if (
                        i == k
                        and
                        j == l
                    ):

                        H_rel[
                            i,
                            j,
                            k,
                            l
                        ] = (
                            kappa_eff[
                                i,
                                j
                            ]
                        )

                        H_U[
                            i,
                            j,
                            k,
                            l
                        ] = 1.0

                    if (
                        i == j
                        and
                        k == l
                    ):

                        C_phi[
                            i,
                            j,
                            k,
                            l
                        ] = 1.0

    return (

        n,

        A_R,

        kappa_eff,

        Gamma,

        Gamma_2,

        H_rel,

        C_phi,

        H_U

    )

# ------------------------------------------------------------
# Tensor -> matriz
# ------------------------------------------------------------

def tensor_para_matriz(
    T,
    n
):

    M = np.zeros(
        (n * n, n * n)
    )

    for i in range(n):
        for j in range(n):

            coluna = i + j * n

            for k in range(n):
                for l in range(n):

                    linha = k + l * n

                    M[
                        linha,
                        coluna
                    ] = T[
                        k,
                        l,
                        i,
                        j
                    ]

    return M

# ------------------------------------------------------------
# Projetor relacional
# ------------------------------------------------------------

def construir_projetor(
    C_phi,
    H_U,
    n
):

    C = tensor_para_matriz(
        C_phi,
        n
    )

    H = tensor_para_matriz(
        H_U,
        n
    )

    U, S, Vt = la.svd(H)

    tol = 1e-10

    modos_zero = Vt[
        S < tol
    ]

    if len(modos_zero) > 0:

        M = np.vstack(
            [
                C,
                modos_zero
            ]
        )

    else:

        M = C

    M_pinv = la.pinv(M)

    I = np.eye(
        n * n
    )

    P = I - M_pinv @ M

    return P

# ------------------------------------------------------------
# Gradiente discreto
# ------------------------------------------------------------

def gradiente_discreto(
    Gamma_2,
    n
):

    G = np.zeros(
        (
            n,
            n,
            n,
            n
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

                        G[
                            i,
                            j,
                            k,
                            l
                        ] = (

                            Gamma_2[
                                i,
                                j
                            ]

                            -

                            Gamma_2[
                                k,
                                l
                            ]

                        )

    return G

# ------------------------------------------------------------
# Operador K_rel*
# ------------------------------------------------------------

def construir_K_rel(

    Gamma_2,

    H_rel,

    P,

    n

):

    grad = gradiente_discreto(
        Gamma_2,
        n
    )

    grad_mat = tensor_para_matriz(
        grad,
        n
    )

    H_mat = tensor_para_matriz(
        H_rel,
        n
    )

    K = (

        P

        @

        grad_mat

        @

        H_mat

        @

        P

    )

    return K

# ------------------------------------------------------------
# Execução
# ------------------------------------------------------------

(

    n,

    A_R,

    kappa_eff,

    Gamma,

    Gamma_2,

    H_rel,

    C_phi,

    H_U

) = inicializar_ambiente()

P_R_star = construir_projetor(

    C_phi,

    H_U,

    n

)

K_rel_star = construir_K_rel(

    Gamma_2,

    H_rel,

    P_R_star,

    n

)

# ------------------------------------------------------------
# Registro
# ------------------------------------------------------------

results.record(
    "n",
    n
)

results.record(
    "matrix_dimension",
    int(K_rel_star.shape[0])
)

results.record(
    "projector_rank",
    int(np.trace(P_R_star))
)

save_array(
    "A_R.npy",
    A_R
)

save_array(
    "Gamma.npy",
    Gamma
)

save_array(
    "Gamma2.npy",
    Gamma_2
)

save_array(
    "P_R_star.npy",
    P_R_star
)

save_array(
    "K_rel_star.npy",
    K_rel_star
)

log("Operador K_rel* reconstruído.")

# ============================================================
# PARTE 3
# AUDITORIA ESTRUTURAL DO OPERADOR K_rel*
# ============================================================

log("")
log("=" * 60)
log("PARTE 3")
log("Auditoria estrutural")
log("=" * 60)

# ------------------------------------------------------------
# Simetria do grafo
# ------------------------------------------------------------

graph_symmetry = la.norm(
    A_R - A_R.T
)

# ------------------------------------------------------------
# Propriedades do projetor
# ------------------------------------------------------------

projector_trace = np.trace(
    P_R_star
)

projector_rank = np.linalg.matrix_rank(
    P_R_star
)

projector_error = la.norm(
    P_R_star @ P_R_star - P_R_star
)

projector_symmetry = la.norm(
    P_R_star - P_R_star.T
)

# ------------------------------------------------------------
# Operador
# ------------------------------------------------------------

operator_norm = la.norm(
    K_rel_star
)

operator_asymmetry = la.norm(
    K_rel_star - K_rel_star.T
)

# ------------------------------------------------------------
# Espectro
# ------------------------------------------------------------

eig = la.eigvals(
    K_rel_star
)

eig_real = np.real(eig)

eig_imag = np.imag(eig)

lambda_min = np.min(
    eig_real
)

lambda_max = np.max(
    eig_real
)

imag_max = np.max(
    np.abs(eig_imag)
)

# ------------------------------------------------------------
# Teste homogêneo
# ------------------------------------------------------------

K_zero = (

    P_R_star

    @

    np.zeros_like(
        K_rel_star
    )

    @

    P_R_star

)

homogeneous_norm = la.norm(
    K_zero
)

# ------------------------------------------------------------
# Impressão
# ------------------------------------------------------------

write("")
write("=" * 60)
write("AUDITORIA ESTRUTURAL")
write("=" * 60)

write(f"Grafo simétrico............. {graph_symmetry:.6e}")

write(f"Rank(P)..................... {projector_rank}")

write(f"Traço(P).................... {projector_trace:.6f}")

write(f"Erro P²-P................... {projector_error:.6e}")

write(f"Erro P-Pᵀ................... {projector_symmetry:.6e}")

write("")

write(f"Norma(K_rel*)............... {operator_norm:.6e}")

write(f"Assimetria(K_rel*).......... {operator_asymmetry:.6e}")

write("")

write(f"λ mínimo.................... {lambda_min:.6e}")

write(f"λ máximo.................... {lambda_max:.6e}")

write(f"Im(λ) máximo................ {imag_max:.6e}")

write("")

write(f"Norma homogênea............. {homogeneous_norm:.6e}")

# ------------------------------------------------------------
# Registro
# ------------------------------------------------------------

results.record(
    "graph_symmetry",
    graph_symmetry
)

results.record(
    "projector_rank",
    projector_rank
)

results.record(
    "projector_trace",
    projector_trace
)

results.record(
    "projector_error",
    projector_error
)

results.record(
    "projector_symmetry",
    projector_symmetry
)

results.record(
    "operator_norm",
    operator_norm
)

results.record(
    "operator_asymmetry",
    operator_asymmetry
)

results.record(
    "lambda_min",
    lambda_min
)

results.record(
    "lambda_max",
    lambda_max
)

results.record(
    "imaginary_max",
    imag_max
)

results.record(
    "homogeneous_norm",
    homogeneous_norm
)

# ------------------------------------------------------------
# CSV
# ------------------------------------------------------------

spectral_df = pd.DataFrame({

    "real": eig_real,

    "imag": eig_imag

})

save_dataframe(
    "eigenvalues.csv",
    spectral_df
)

# ------------------------------------------------------------
# Histograma
# ------------------------------------------------------------

plt.figure(figsize=(7,5))

plt.hist(
    eig_real,
    bins=20
)

plt.xlabel("Autovalor")

plt.ylabel("Frequência")

plt.title(
    "Espectro de K_rel*"
)

save_figure(
    "spectrum_histogram.png"
)

# ------------------------------------------------------------
# Plano complexo
# ------------------------------------------------------------

plt.figure(figsize=(6,6))

plt.scatter(
    eig_real,
    eig_imag,
    s=40
)

plt.axhline(
    0,
    linewidth=1
)

plt.axvline(
    0,
    linewidth=1
)

plt.xlabel("Re(λ)")

plt.ylabel("Im(λ)")

plt.title(
    "Plano espectral"
)

save_figure(
    "complex_spectrum.png"
)

# ------------------------------------------------------------
# Certificado estrutural
# ------------------------------------------------------------

audit = {

    "graph_symmetry":

        float(graph_symmetry),

    "projector_trace":

        float(projector_trace),

    "projector_rank":

        int(projector_rank),

    "projector_error":

        float(projector_error),

    "projector_symmetry":

        float(projector_symmetry),

    "operator_norm":

        float(operator_norm),

    "operator_asymmetry":

        float(operator_asymmetry),

    "lambda_min":

        float(lambda_min),

    "lambda_max":

        float(lambda_max),

    "imaginary_max":

        float(imag_max),

    "homogeneous_norm":

        float(homogeneous_norm)

}

save_json(
    "structural_audit.json",
    audit
)

log("Auditoria estrutural concluída.")

# ============================================================
# PARTE 4
# REFINAMENTO ESPECTRAL DO OPERADOR
# (S23-C.2.B → S23-C.2.H)
# ============================================================

log("")
log("=" * 60)
log("PARTE 4")
log("Refinamento espectral")
log("=" * 60)

# ------------------------------------------------------------
# Assimetria normalizada
# ------------------------------------------------------------

def assimetria_normalizada(K):

    norma = la.norm(K)

    if norma < 1e-12:
        return 0.0

    return la.norm(
        K - K.T
    ) / norma

# ------------------------------------------------------------
# Operador simétrico
# ------------------------------------------------------------

K_sym = 0.5 * (
    K_rel_star +
    K_rel_star.T
)

# ------------------------------------------------------------
# Estatísticas
# ------------------------------------------------------------

assim_original = assimetria_normalizada(
    K_rel_star
)

assim_sim = assimetria_normalizada(
    K_sym
)

eig_original = la.eigvals(
    K_rel_star
)

eig_sym = la.eigvalsh(
    K_sym
)

imag_original = np.max(
    np.abs(
        np.imag(
            eig_original
        )
    )
)

lambda_min_sym = np.min(
    eig_sym
)

lambda_max_sym = np.max(
    eig_sym
)

centro = np.mean(
    eig_sym
)

largura = (
    lambda_max_sym -
    lambda_min_sym
)

# ------------------------------------------------------------
# Registro
# ------------------------------------------------------------

results.record(
    "original_asymmetry",
    assim_original
)

results.record(
    "symmetrized_asymmetry",
    assim_sim
)

results.record(
    "spectral_center",
    centro
)

results.record(
    "spectral_width",
    largura
)

# ------------------------------------------------------------
# Impressão
# ------------------------------------------------------------

write("")
write("=" * 60)
write("REFINAMENTO ESPECTRAL")
write("=" * 60)

write(
    f"Assimetria original .... {assim_original:.6e}"
)

write(
    f"Assimetria simétrica ... {assim_sim:.6e}"
)

write(
    f"Im(λ) máximo ........... {imag_original:.6e}"
)

write("")

write(
    f"λ mínimo ............... {lambda_min_sym:.6e}"
)

write(
    f"λ máximo ............... {lambda_max_sym:.6e}"
)

write(
    f"Centro espectral ....... {centro:.6e}"
)

write(
    f"Largura espectral ...... {largura:.6e}"
)

# ------------------------------------------------------------
# Gráfico
# ------------------------------------------------------------

plt.figure(figsize=(8,4))

plt.plot(
    np.sort(eig_sym),
    marker="o"
)

plt.xlabel("Modo")

plt.ylabel("Autovalor")

plt.title(
    "Espectro simetrizado"
)

save_figure(
    "symmetrized_spectrum.png"
)

# ------------------------------------------------------------
# CSV
# ------------------------------------------------------------

df = pd.DataFrame({

    "lambda":

        np.sort(eig_sym)

})

save_dataframe(

    "symmetrized_spectrum.csv",

    df

)

# ------------------------------------------------------------
# Operador refinado
# ------------------------------------------------------------

K_refined = K_sym.copy()

# ------------------------------------------------------------
# Salva
# ------------------------------------------------------------

save_array(

    "K_refined.npy",

    K_refined

)

log("Operador refinado criado.")

# ============================================================
# Certificado
# ============================================================

certificate = {

    "original_asymmetry":

        float(assim_original),

    "refined_asymmetry":

        float(assim_sim),

    "lambda_min":

        float(lambda_min_sym),

    "lambda_max":

        float(lambda_max_sym),

    "spectral_center":

        float(centro),

    "spectral_width":

        float(largura)

}

save_json(

    "refined_operator_certificate.json",

    certificate

)

write("")
write("Operador refinado disponível.")

# ============================================================
# PARTE 5
# RENORMALIZAÇÃO ESPECTRAL
# (S23-D.3.D)
# ============================================================

log("")
log("=" * 60)
log("PARTE 5")
log("Renormalização espectral")
log("=" * 60)

# ------------------------------------------------------------
# Operador efetivo
# ------------------------------------------------------------

K_eff = K_refined - ALPHA * np.eye(
    K_refined.shape[0]
)

# ------------------------------------------------------------
# Espectro
# ------------------------------------------------------------

eig_before = la.eigvalsh(
    K_refined
)

eig_after = la.eigvalsh(
    K_eff
)

# ------------------------------------------------------------
# Estatísticas
# ------------------------------------------------------------

lambda_before_min = eig_before.min()

lambda_before_max = eig_before.max()

lambda_after_min = eig_after.min()

lambda_after_max = eig_after.max()

spectral_shift = np.mean(
    eig_before - eig_after
)

stable = bool(
    np.all(
        eig_after < 0
    )
)

# ------------------------------------------------------------
# Registro
# ------------------------------------------------------------

results.record(
    "alpha",
    ALPHA
)

results.record(
    "lambda_before_min",
    lambda_before_min
)

results.record(
    "lambda_before_max",
    lambda_before_max
)

results.record(
    "lambda_after_min",
    lambda_after_min
)

results.record(
    "lambda_after_max",
    lambda_after_max
)

results.record(
    "spectral_shift",
    spectral_shift
)

results.record(
    "linear_stability",
    stable
)

# ------------------------------------------------------------
# Relatório
# ------------------------------------------------------------

write("")
write("=" * 60)
write("RENORMALIZAÇÃO")
write("=" * 60)

write(f"α........................ {ALPHA:.6f}")

write("")

write(f"λmin antes............... {lambda_before_min:.6e}")
write(f"λmax antes............... {lambda_before_max:.6e}")

write("")

write(f"λmin depois.............. {lambda_after_min:.6e}")
write(f"λmax depois.............. {lambda_after_max:.6e}")

write("")

write(f"Shift médio.............. {spectral_shift:.6e}")

write(f"Estável.................. {stable}")

# ------------------------------------------------------------
# Figura
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(
    np.sort(eig_before),
    label="Original"
)

plt.plot(
    np.sort(eig_after),
    label="Renormalizado"
)

plt.xlabel("Modo")

plt.ylabel("Autovalor")

plt.title(
    "Renormalização Espectral"
)

plt.legend()

save_figure(
    "spectral_renormalization.png"
)

# ------------------------------------------------------------
# CSV
# ------------------------------------------------------------

spectral_df = pd.DataFrame({

    "before": np.sort(eig_before),

    "after": np.sort(eig_after)

})

save_dataframe(

    "spectral_renormalization.csv",

    spectral_df

)

# ------------------------------------------------------------
# Salva operador
# ------------------------------------------------------------

save_array(

    "K_eff.npy",

    K_eff

)

# ------------------------------------------------------------
# Certificado
# ------------------------------------------------------------

certificate = {

    "alpha": float(ALPHA),

    "lambda_before_min": float(lambda_before_min),

    "lambda_before_max": float(lambda_before_max),

    "lambda_after_min": float(lambda_after_min),

    "lambda_after_max": float(lambda_after_max),

    "spectral_shift": float(spectral_shift),

    "stable": stable

}

save_json(

    "spectral_renormalization_certificate.json",

    certificate

)

log("Renormalização espectral concluída.")

# ============================================================
# PARTE 6
# VALIDAÇÃO DINÂMICA
# (S23-D.3.E)
# ============================================================

log("")
log("=" * 60)
log("PARTE 6")
log("Validação dinâmica")
log("=" * 60)

# ------------------------------------------------------------
# Campo linear
# ------------------------------------------------------------

def campo(t, eta):

    return K_eff @ eta

# ------------------------------------------------------------
# Condição inicial
# ------------------------------------------------------------

eta0 = RNG.normal(
    0.0,
    1.0,
    size=K_eff.shape[0]
)

eta0 /= la.norm(eta0)

# ------------------------------------------------------------
# Integração
# ------------------------------------------------------------

t_eval = np.linspace(
    0.0,
    TMAX,
    NSTEPS + 1
)

sol = solve_ivp(

    campo,

    (0.0, TMAX),

    eta0,

    method="RK45",

    t_eval=t_eval,

    rtol=1e-9,

    atol=1e-12

)

eta_hist = sol.y.T

tempo = sol.t

# ------------------------------------------------------------
# Norma da trajetória
# ------------------------------------------------------------

norma = la.norm(
    eta_hist,
    axis=1
)

log_norma = np.log(
    np.maximum(
        norma,
        1e-30
    )
)

# ------------------------------------------------------------
# Ajuste exponencial
# ------------------------------------------------------------

coef = np.polyfit(

    tempo,

    log_norma,

    1

)

lambda_dyn = coef[0]

# ------------------------------------------------------------
# Crescimento observado
# ------------------------------------------------------------

growth = norma[-1] / norma[0]

stable_dynamic = bool(
    lambda_dyn < 0.0
)

# ------------------------------------------------------------
# Registro
# ------------------------------------------------------------

results.record(
    "dynamic_lyapunov",
    lambda_dyn
)

results.record(
    "growth_factor",
    growth
)

results.record(
    "dynamic_stability",
    stable_dynamic
)

results.record(
    "initial_norm",
    norma[0]
)

results.record(
    "final_norm",
    norma[-1]
)

# ------------------------------------------------------------
# Impressão
# ------------------------------------------------------------

write("")
write("=" * 60)
write("VALIDAÇÃO DINÂMICA")
write("=" * 60)

write(f"Norma inicial.............. {norma[0]:.6e}")

write(f"Norma final................ {norma[-1]:.6e}")

write("")

write(f"Fator crescimento.......... {growth:.6e}")

write("")

write(f"Lyapunov dinâmico.......... {lambda_dyn:.6e}")

write("")

write(f"Dinâmica estável........... {stable_dynamic}")

# ------------------------------------------------------------
# Figura
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(

    tempo,

    norma

)

plt.xlabel("Tempo")

plt.ylabel("||η||")

plt.title(
    "Norma da trajetória"
)

save_figure(
    "trajectory_norm.png"
)

# ------------------------------------------------------------
# Log
# ------------------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(

    tempo,

    log_norma

)

plt.xlabel("Tempo")

plt.ylabel("log ||η||")

plt.title(
    "Decaimento exponencial"
)

save_figure(
    "trajectory_lognorm.png"
)

# ------------------------------------------------------------
# Dados
# ------------------------------------------------------------

traj_df = pd.DataFrame({

    "time": tempo,

    "norm": norma,

    "log_norm": log_norma

})

save_dataframe(

    "trajectory.csv",

    traj_df

)

save_array(

    "trajectory.npy",

    eta_hist

)

# ------------------------------------------------------------
# Certificado
# ------------------------------------------------------------

certificate = {

    "dynamic_lyapunov":

        float(lambda_dyn),

    "growth_factor":

        float(growth),

    "dynamic_stability":

        stable_dynamic,

    "initial_norm":

        float(norma[0]),

    "final_norm":

        float(norma[-1])

}

save_json(

    "dynamic_validation_certificate.json",

    certificate

)

log("Validação dinâmica concluída.")

# ============================================================
# PARTE 7
# CONSOLIDAÇÃO FINAL DO EXPERIMENTO
# ============================================================

log("")
log("=" * 60)
log("PARTE 7")
log("Consolidação Final")
log("=" * 60)

# ------------------------------------------------------------
# Estatísticas gerais
# ------------------------------------------------------------

execution_time = time.time() - START_TIME

n_vertices = int(n)

matrix_dimension = int(K_eff.shape[0])

stable_linear = bool(
    np.all(
        la.eigvalsh(K_eff) < 0
    )
)

stable_dynamic = bool(
    results.results.get(
        "dynamic_stability",
        False
    )
)

dynamic_lyapunov = float(
    results.results.get(
        "dynamic_lyapunov",
        np.nan
    )
)

growth_factor = float(
    results.results.get(
        "growth_factor",
        np.nan
    )
)

# ------------------------------------------------------------
# Certificado Oficial
# ------------------------------------------------------------

certificate = {

    "experiment": EXPERIMENT,

    "title": TITLE,

    "author": AUTHOR,

    "version": VERSION,

    "date": datetime.now().isoformat(),

    "execution_time_seconds":

        round(
            execution_time,
            3
        ),

    "graph":{

        "vertices": n_vertices,

        "matrix_dimension": matrix_dimension

    },

    "spectral":{

        "alpha": ALPHA,

        "lambda_min":

            results.results["lambda_after_min"],

        "lambda_max":

            results.results["lambda_after_max"],

        "stable":

            stable_linear

    },

    "dynamic":{

        "lyapunov":

            dynamic_lyapunov,

        "growth_factor":

            growth_factor,

        "stable":

            stable_dynamic

    },

    "conclusion":{

        "linear_validation":

            stable_linear,

        "dynamic_validation":

            stable_dynamic,

        "experiment_success":

            stable_linear and stable_dynamic

    }

}

save_json(

    "S23_certificate.json",

    certificate

)

# ------------------------------------------------------------
# Relatório
# ------------------------------------------------------------

write("")
write("=" * 60)
write("CONCLUSÃO")
write("=" * 60)
write("")

if stable_linear:

    write("✔ Operador linearmente estabilizado.")

else:

    write("✘ Operador linearmente instável.")

if stable_dynamic:

    write("✔ Dinâmica estabilizada.")

else:

    write("✘ Dinâmica instável.")

write("")

write(f"Expoente de Lyapunov : {dynamic_lyapunov:.6e}")

write(f"Fator de crescimento : {growth_factor:.6e}")

write("")

write(f"Tempo total : {execution_time:.2f} s")

write("")

write("=" * 60)
write("FIM DO EXPERIMENTO")
write("=" * 60)

save_summary()

# ------------------------------------------------------------
# Relatório JSON completo
# ------------------------------------------------------------

results.save()

# ------------------------------------------------------------
# Mensagem Final
# ------------------------------------------------------------

log("")
log("=" * 60)
log("S23 FINALIZADO")
log("=" * 60)

log(f"Resultados : {RESULTS}")

log("Arquivos produzidos:")

for folder in [

    DATA,

    FIGURES,

    REPORTS

]:

    files = sorted(folder.glob("*"))

    log(f"")

    log(folder.name)

    for f in files:

        log(f"   {f.name}")

log("")
log("Experimento concluído com sucesso.")

def main():

    log("=" * 60)
    log("Iniciando S23_FINAL")

    # Parte 2
    ...

    # Parte 3
    ...

    # Parte 4
    ...

    # Parte 5
    ...

    # Parte 6
    ...

    # Parte 7
    ...

    log("S23_FINAL concluído.")

if __name__ == "__main__":
    main()
