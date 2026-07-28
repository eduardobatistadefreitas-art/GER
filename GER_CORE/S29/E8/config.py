"""
============================================================

GER
S29-E8

Trajectory Observatory

config.py

============================================================

Configuração central do experimento.

Toda a parametrização do E8 deve estar definida
neste arquivo.

Nenhum módulo deve conter caminhos ou constantes
fixas.

============================================================
"""

from __future__ import annotations

from pathlib import Path

# ==========================================================
# Identificação
# ==========================================================

EXPERIMENT_NAME = "S29_E8"

EXPERIMENT_TITLE = (
    "Trajectory Observatory"
)

VERSION = "1.0"

# ==========================================================
# Diretório principal
# ==========================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/GER_RESULTS/S29"
)

# ==========================================================
# Execução
# ==========================================================

AUTO_RESUME = True

RANDOM_SEED = 42

# ==========================================================
# Trajetória
# ==========================================================

MAX_STATES = 1000

SAVE_EVERY = 5

CHECKPOINT_EVERY = 25

# ==========================================================
# Parâmetro controlado
# ==========================================================

PARAMETER_NAME = "sigma"

PARAMETER_START = 0.1000

PARAMETER_STOP = 0.2000

PARAMETER_STEP = 0.0001

# ==========================================================
# Dashboard
# ==========================================================

SHOW_PROGRESS = True

REFRESH_EVERY = 1

# ==========================================================
# Benchmark
# ==========================================================

ENABLE_BENCHMARK = True

# ==========================================================
# Certificado
# ==========================================================

GENERATE_CERTIFICATE = True

# ==========================================================
# Relatório
# ==========================================================

GENERATE_REPORT = True
