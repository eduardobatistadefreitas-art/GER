"""
=============================================================
E8_PIPELINE_AUDIT.py
=============================================================

Objetivo
---------

Auditar completamente o pipeline oficial do GER.

Este script NÃO executa um experimento.

Ele apenas mostra:

1) saída do run_engine()
2) estrutura dos snapshots
3) estrutura dos observables
4) estrutura da Signature
5) estrutura do Certificate

=============================================================
"""

from pprint import pprint

from GER.CORE.bootstrap import initialize
from GER.CORE.ger_engine import run_engine
from GER.CORE.ger_observational_snapshot import (
    build_observational_snapshot,
)
from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)
from GER.CORE.experiment_pipeline import (
    run_signature_pipeline,
)


# ---------------------------------------------------------
# Utilitário
# ---------------------------------------------------------

def header(title):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


# ---------------------------------------------------------
# Inicialização
# ---------------------------------------------------------

initialize()


# ---------------------------------------------------------
# Motor
# ---------------------------------------------------------

header("RUN ENGINE")

simulation = run_engine()

print(type(simulation))

if isinstance(simulation, dict):

    print()
    print("Keys:")
    pprint(list(simulation.keys()))


# ---------------------------------------------------------
# Snapshots
# ---------------------------------------------------------

header("SNAPSHOTS")

snapshots = simulation.get("snapshots")

print(type(snapshots))

print("Length:", len(snapshots))

first_snapshot = snapshots[0]

print()
print(type(first_snapshot))

if isinstance(first_snapshot, dict):

    print()
    pprint(first_snapshot.keys())


# ---------------------------------------------------------
# Observational Snapshot
# ---------------------------------------------------------

header("OBSERVATIONAL SNAPSHOT")

obs_snapshot = build_observational_snapshot(

    first_snapshot

)

print(type(obs_snapshot))

if isinstance(obs_snapshot, dict):

    pprint(obs_snapshot.keys())


# ---------------------------------------------------------
# Persistence Observatory
# ---------------------------------------------------------

header("PERSISTENCE OBSERVATORY")

observables = run_persistence_observatory(

    snapshots

)

print(type(observables))

if isinstance(observables, dict):

    print()

    pprint(observables.keys())

    print()

    for k, v in observables.items():

        print(k, type(v))


# ---------------------------------------------------------
# Signature Pipeline
# ---------------------------------------------------------

header("SIGNATURE PIPELINE")

result = run_signature_pipeline(

    observables,

    simulation["configuration"]["dt"],

)

print(type(result))

print()

pprint(result.keys())


signature = result["signature"]

certificate = result["certificate"]


# ---------------------------------------------------------
# Signature
# ---------------------------------------------------------

header("SIGNATURE")

print(type(signature))

print()

print(signature)


# ---------------------------------------------------------
# Certificate
# ---------------------------------------------------------

header("CERTIFICATE")

print(type(certificate))

print()

if isinstance(certificate, dict):

    pprint(certificate.keys())

    print()

    pprint(certificate)
