"""
=============================================================
E10_1_2_F_geometry_certificate.py
=============================================================

GER — Geometria da Superfície Relacional
E10.1.2.F — Geometry Certificate

Objetivo
--------
Consolidar todos os resultados produzidos pelos módulos
A–E em um certificado geométrico único da superfície
relacional.

Este módulo NÃO realiza novos cálculos geométricos.

Sua função é integrar os diagnósticos produzidos por:

A — Gradient
B — Continuity
C — Boundaries
D — Connected Regions
E — Effective Dimension

e produzir um certificado estrutural único.

Entradas
---------
gradient_summary.json
continuity_summary.json
boundary_summary.json
connected_regions_summary.json
effective_dimension_summary.json

Saídas
------
geometry_certificate.json
geometry_certificate.txt

=============================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

ROOT = (
    Path("/content/drive/MyDrive/GER_RESULTS")
    / "S29"
    / "E10"
)

GRADIENT = ROOT / "E10_1_2_A_Gradient"
CONTINUITY = ROOT / "E10_1_2_B_Continuity"
BOUNDARIES = ROOT / "E10_1_2_C_Boundaries"
CONNECTED = ROOT / "E10_1_2_D_ConnectedRegions"
DIMENSION = ROOT / "E10_1_2_E_Dimension"

OUTPUT = (
    ROOT
    / "E10_1_2_F_GeometryCertificate"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS
# ============================================================

GRADIENT_JSON = (
    GRADIENT / "gradient_summary.json"
)

CONTINUITY_JSON = (
    CONTINUITY / "continuity_summary.json"
)

BOUNDARY_JSON = (
    BOUNDARIES / "boundary_summary.json"
)

CONNECTED_JSON = (
    CONNECTED / "connected_regions_summary.json"
)

DIMENSION_JSON = (
    DIMENSION / "effective_dimension_summary.json"
)

CERTIFICATE_JSON = (
    OUTPUT / "geometry_certificate.json"
)

CERTIFICATE_TXT = (
    OUTPUT / "geometry_certificate.txt"
)


# ============================================================
# LEITURA DOS RESULTADOS
# ============================================================

print("=" * 60)
print("GER")
print("E10.1.2.F")
print("Geometry Certificate")
print("=" * 60)

print("\nCarregando resultados...")

with open(GRADIENT_JSON, encoding="utf-8") as fp:
    gradient = json.load(fp)

with open(CONTINUITY_JSON, encoding="utf-8") as fp:
    continuity = json.load(fp)

with open(BOUNDARY_JSON, encoding="utf-8") as fp:
    boundaries = json.load(fp)

with open(CONNECTED_JSON, encoding="utf-8") as fp:
    connected = json.load(fp)

with open(DIMENSION_JSON, encoding="utf-8") as fp:
    dimension = json.load(fp)

components = sorted(
    gradient["components"].keys()
)

print(
    f"Componentes analisadas : {len(components)}"
)

print("\nTodos os produtos foram carregados.")

print("=" * 60)

# ============================================================
# CONSOLIDAÇÃO DO CERTIFICADO
# ============================================================

print("\nConstruindo certificado geométrico...")

certificate = {

    "experiment": "E10.1.2",
    "module": "Geometry Certificate",

    "components": {},

    "global_summary": {}

}

# ============================================================
# CONSOLIDAÇÃO POR COMPONENTE
# ============================================================

gradient_zero = 0
fully_continuous = 0
boundary_free = 0
single_region = 0
dimension_zero = 0

for component in components:

    # --------------------------------------------------------
    # Gradient
    # --------------------------------------------------------

    g = gradient["components"][component]

    max_gradient = g["max_gradient"]

    gradient_is_zero = (
        abs(max_gradient) <= 1e-12
    )

    if gradient_is_zero:
        gradient_zero += 1

    # --------------------------------------------------------
    # Continuity
    # --------------------------------------------------------

    c = continuity["components"][component]

    continuity_ok = (
    c["continuous_fraction"] == 1.0
    )

    if continuity_ok:
        fully_continuous += 1

    # --------------------------------------------------------
    # Boundaries
    # --------------------------------------------------------

    b = boundaries["components"][component]

    boundary_fraction = (
        b["boundary_fraction"]
    )

    boundary_free_component = (
        boundary_fraction == 0.0
    )

    if boundary_free_component:
        boundary_free += 1

    # --------------------------------------------------------
    # Connected regions
    # --------------------------------------------------------

    r = connected["components"][component]

    regions = r["number_of_regions"]

    single_component = (
        regions == 1
    )

    if single_component:
        single_region += 1

    # --------------------------------------------------------
    # Effective Dimension
    # --------------------------------------------------------

    d = dimension["components"][component]

    effective_dimension = (
        d["effective_dimension"]
    )

    zero_dimension = (
        effective_dimension == 0
    )

    if zero_dimension:
        dimension_zero += 1

    # --------------------------------------------------------
    # Certificado individual
    # --------------------------------------------------------

    certificate["components"][component] = {

        "gradient_zero":
            gradient_is_zero,

        "fully_continuous":
            continuity_ok,

        "boundary_free":
            boundary_free_component,

        "connected_regions":
            regions,

        "single_region":
            single_component,

        "effective_dimension":
            effective_dimension,

    }

# ============================================================
# RESUMO GLOBAL
# ============================================================

n = len(components)

certificate["global_summary"] = {

    "number_of_components":
        n,

    "zero_gradient":
        gradient_zero,

    "fully_continuous":
        fully_continuous,

    "boundary_free":
        boundary_free,

    "single_region":
        single_region,

    "dimension_zero":
        dimension_zero,

    "fraction_zero_gradient":
        gradient_zero / n,

    "fraction_continuous":
        fully_continuous / n,

    "fraction_boundary_free":
        boundary_free / n,

    "fraction_single_region":
        single_region / n,

    "fraction_dimension_zero":
        dimension_zero / n,

}

print("Certificado consolidado.")

print("=" * 60)

# ============================================================
# PERSISTÊNCIA DO CERTIFICADO
# ============================================================

print("\nGravando certificado...")

with open(
    CERTIFICATE_JSON,
    "w",
    encoding="utf-8",
) as fp:

    json.dump(
        certificate,
        fp,
        indent=4,
        ensure_ascii=False,
    )

print("Certificado JSON salvo.")

# ============================================================
# RELATÓRIO TEXTO
# ============================================================

with open(
    CERTIFICATE_TXT,
    "w",
    encoding="utf-8",
) as fp:

    fp.write("=" * 60 + "\n")
    fp.write("GER\n")
    fp.write("E10.1.2.F\n")
    fp.write("Geometry Certificate\n")
    fp.write("=" * 60 + "\n\n")

    summary = certificate["global_summary"]

    fp.write("RESUMO GLOBAL\n")
    fp.write("-" * 60 + "\n")

    fp.write(
        f"Componentes analisadas : "
        f"{summary['number_of_components']}\n"
    )

    fp.write(
        f"Gradiente nulo         : "
        f"{summary['zero_gradient']}\n"
    )

    fp.write(
        f"Superfícies contínuas  : "
        f"{summary['fully_continuous']}\n"
    )

    fp.write(
        f"Sem fronteiras         : "
        f"{summary['boundary_free']}\n"
    )

    fp.write(
        f"Região única           : "
        f"{summary['single_region']}\n"
    )

    fp.write(
        f"Dimensão efetiva zero  : "
        f"{summary['dimension_zero']}\n"
    )

    fp.write("\n")

    fp.write(
        f"Fração gradiente nulo  : "
        f"{summary['fraction_zero_gradient']:.6f}\n"
    )

    fp.write(
        f"Fração contínua        : "
        f"{summary['fraction_continuous']:.6f}\n"
    )

    fp.write(
        f"Fração sem fronteiras  : "
        f"{summary['fraction_boundary_free']:.6f}\n"
    )

    fp.write(
        f"Fração região única    : "
        f"{summary['fraction_single_region']:.6f}\n"
    )

    fp.write(
        f"Fração dimensão zero   : "
        f"{summary['fraction_dimension_zero']:.6f}\n"
    )

    fp.write("\n\n")

    fp.write("=" * 60 + "\n")
    fp.write("RESULTADOS POR COMPONENTE\n")
    fp.write("=" * 60 + "\n\n")

    for component in components:

        c = certificate["components"][component]

        fp.write(component + "\n")
        fp.write("-" * len(component) + "\n")

        fp.write(
            f"Gradient Zero      : "
            f"{c['gradient_zero']}\n"
        )

        fp.write(
            f"Fully Continuous   : "
            f"{c['fully_continuous']}\n"
        )

        fp.write(
            f"Boundary Free      : "
            f"{c['boundary_free']}\n"
        )

        fp.write(
            f"Connected Regions  : "
            f"{c['connected_regions']}\n"
        )

        fp.write(
            f"Single Region      : "
            f"{c['single_region']}\n"
        )

        fp.write(
            f"Effective Dimension: "
            f"{c['effective_dimension']}\n"
        )

        fp.write("\n")

print("Relatório TXT salvo.")

# ============================================================
# RESUMO OPERACIONAL
# ============================================================

print("\n" + "=" * 60)
print("CERTIFICADO GEOMÉTRICO GERADO")
print("=" * 60)

print(f"Componentes : {len(components)}")
print(f"JSON        : {CERTIFICATE_JSON.name}")
print(f"TXT         : {CERTIFICATE_TXT.name}")

print("=" * 60)

# ============================================================
# AUDITORIA E CONCLUSÃO
# ============================================================

print("\nExecutando auditoria do certificado...")

audit = {}

audit["components"] = len(components)

audit["certificate_entries"] = len(
    certificate["components"]
)

audit["missing_entries"] = (
    len(components)
    -
    len(certificate["components"])
)

audit["status"] = "PASS"

if audit["missing_entries"] != 0:
    audit["status"] = "FAIL"

# ------------------------------------------------------------
# Consistência entre módulos
# ------------------------------------------------------------

audit["gradient_consistent"] = (
    certificate["global_summary"]["zero_gradient"]
    <= len(components)
)

audit["continuity_consistent"] = (
    certificate["global_summary"]["fully_continuous"]
    <= len(components)
)

audit["boundary_consistent"] = (
    certificate["global_summary"]["boundary_free"]
    <= len(components)
)

audit["regions_consistent"] = (
    certificate["global_summary"]["single_region"]
    <= len(components)
)

audit["dimension_consistent"] = (
    certificate["global_summary"]["dimension_zero"]
    <= len(components)
)

if not all([
    audit["gradient_consistent"],
    audit["continuity_consistent"],
    audit["boundary_consistent"],
    audit["regions_consistent"],
    audit["dimension_consistent"],
]):
    audit["status"] = "FAIL"

certificate["audit"] = audit

# ============================================================
# DIAGNÓSTICO GLOBAL
# ============================================================

print("\nDiagnóstico geométrico:")

gs = certificate["global_summary"]

print(
    f"Gradiente nulo           : "
    f"{gs['zero_gradient']}/{len(components)}"
)

print(
    f"Continuidade completa    : "
    f"{gs['fully_continuous']}/{len(components)}"
)

print(
    f"Sem fronteiras           : "
    f"{gs['boundary_free']}/{len(components)}"
)

print(
    f"Região única             : "
    f"{gs['single_region']}/{len(components)}"
)

print(
    f"Dimensão efetiva zero    : "
    f"{gs['dimension_zero']}/{len(components)}"
)

# ------------------------------------------------------------
# Classificação global da superfície
# ------------------------------------------------------------

if (
    gs["zero_gradient"] == len(components)
    and
    gs["fully_continuous"] == len(components)
    and
    gs["boundary_free"] == len(components)
    and
    gs["single_region"] == len(components)
    and
    gs["dimension_zero"] == len(components)
):

    geometry_class = (
        "GEOMETRICALLY UNIFORM SURFACE"
    )

elif (
    gs["fully_continuous"] == len(components)
):

    geometry_class = (
        "CONTINUOUS SURFACE"
    )

else:

    geometry_class = (
        "STRUCTURED SURFACE"
    )

certificate["global_summary"][
    "geometry_class"
] = geometry_class

print(f"\nClassificação : {geometry_class}")

# ============================================================
# SALVAMENTO FINAL
# ============================================================

with open(
    CERTIFICATE_JSON,
    "w",
    encoding="utf-8",
) as fp:

    json.dump(
        certificate,
        fp,
        indent=4,
        ensure_ascii=False,
    )

with open(
    CERTIFICATE_TXT,
    "w",
    encoding="utf-8",
) as fp:

    fp.write("=" * 60 + "\n")
    fp.write("GER\n")
    fp.write("E10.1.2.F\n")
    fp.write("Geometry Certificate\n")
    fp.write("=" * 60 + "\n\n")

    fp.write(
        f"Componentes : {len(components)}\n"
    )

    fp.write(
        f"Classe geométrica : {geometry_class}\n\n"
    )

    fp.write("Resumo Global\n")
    fp.write("-" * 40 + "\n")

    for key, value in gs.items():
        fp.write(f"{key}: {value}\n")

    fp.write("\n")

    fp.write("Auditoria\n")
    fp.write("-" * 40 + "\n")

    for key, value in audit.items():
        fp.write(f"{key}: {value}\n")

print("\nCertificado salvo.")

# ============================================================
# CONCLUSÃO
# ============================================================

print("\n" + "=" * 60)
print("GER")
print("E10.1.2.F")
print("Geometry Certificate")
print("=" * 60)

print(f"Status          : {audit['status']}")
print(f"Classe          : {geometry_class}")
print(f"Componentes     : {len(components)}")

print("\nProdutos gerados:")

print(f"  • {CERTIFICATE_JSON.name}")
print(f"  • {CERTIFICATE_TXT.name}")

print("=" * 60)
print("Módulo E10.1.2.F concluído.")
print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():
    """
    O certificado geométrico é produzido
    automaticamente durante a execução do módulo.

    Esta função é mantida para padronização
    de todos os módulos da série E10.
    """
    pass


if __name__ == "__main__":
    main()
