"""
=============================================================
GER
S29 E8

SIGNATURE AUDIT
=============================================================
"""

from pprint import pprint

from GER.CORE.bootstrap import initialize
from GER.CORE.ger_engine import run_engine
from GER.CORE.experiment_pipeline import run_signature_pipeline

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)


print("=" * 60)
print("INITIALIZING")
print("=" * 60)

initialize()

print()
print("=" * 60)
print("RUN ENGINE")
print("=" * 60)

simulation = run_engine(
    n=384,
    timesteps=2000,
    dt=0.00025,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    sigma=0.10,
)

snapshots = simulation["snapshots"]

configuration = simulation["configuration"]

print()
print("=" * 60)
print("PERSISTENCE")
print("=" * 60)

observables = run_persistence_observatory(
    snapshots,
    configuration["dt"],
)

print(type(observables))

print()
print("=" * 60)
print("PIPELINE")
print("=" * 60)

pipeline = run_signature_pipeline(
    observables,
    configuration["dt"],
)

print(type(pipeline))

if isinstance(pipeline, dict):

    print()
    print("PIPELINE KEYS")
    print("-" * 60)

    print(list(pipeline.keys()))

print()
print("=" * 60)
print("SIGNATURE")
print("=" * 60)

signature = pipeline["signature"]

print("TYPE")
print(type(signature))

print()

print("DIR")
print("-" * 60)

print(dir(signature))

print()

print("DICT")
print("-" * 60)

if hasattr(signature, "__dict__"):

    pprint(signature.__dict__)

else:

    print("No __dict__")

print()

print("TO_DICT")
print("-" * 60)

if hasattr(signature, "to_dict"):

    pprint(signature.to_dict())

else:

    print("No to_dict()")

print()

print("STRING REPRESENTATION")
print("-" * 60)

print(signature)

print()

print("=" * 60)
print("EXTRACT SIGNATURE")
print("=" * 60)

try:

    from GER.CORE.ger_geometric_signature import extract_signature

    extracted = extract_signature(signature)

    print(type(extracted))

    pprint(extracted)

except Exception as e:

    print(e)
