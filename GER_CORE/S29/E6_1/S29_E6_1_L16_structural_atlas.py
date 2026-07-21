from pathlib import Path
import json
import numpy as np
import pandas as pd

# ============================================================
# GER
# S29-E6.1-L16
# Structural Atlas of the Observable Space
# ============================================================

ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S29_E6.1")

OUT = ROOT / "L16_StructuralAtlas"
OUT.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GER")
print("S29-E6.1-L16")
print("Structural Atlas of the Observable Space")
print("=" * 70)

# ============================================================
# HELPERS
# ============================================================

def load_csv(path):

    if path.exists():
        return pd.read_csv(path)

    print(f"[WARNING] Missing: {path.name}")
    return None


# ============================================================
# LOAD FILES
# ============================================================

centrality = load_csv(
    ROOT /
    "L15_StructuralNetwork" /
    "centrality_metrics.csv"
)

communities = load_csv(
    ROOT /
    "L15_StructuralNetwork" /
    "communities.csv"
)

bond = load_csv(
    ROOT /
    "L14_PairStabilityAnalysis" /
    "structural_bond_strength.csv"
)

independence = load_csv(
    ROOT /
    "L5_IndependenceRanking" /
    "independence_ranking.csv"
)

minimal = load_csv(
    ROOT /
    "L9_MinimalObservableSet" /
    "minimal_observable_sets.csv"
)

# ============================================================
# OBSERVABLES
# ============================================================

observables = sorted(
    centrality["Observable"].tolist()
)

atlas = pd.DataFrame({

    "Observable": observables

})

# ============================================================
# COMMUNITY
# ============================================================

community_map = {}

if communities is not None:

    for _, row in communities.iterrows():

        community_map[row.Observable] = row.Community

atlas["Community"] = atlas.Observable.map(community_map)

# ============================================================
# CENTRALITY
# ============================================================

atlas = atlas.merge(

    centrality,

    on="Observable",

    how="left"

)

# ============================================================
# SBS
# ============================================================

if bond is not None:

    sbs = {}

    for _, row in bond.iterrows():

        sbs[row.Observable] = row.StructuralBondStrength

    atlas["StructuralBondStrength"] = atlas.Observable.map(sbs)

else:

    atlas["StructuralBondStrength"] = np.nan

# ============================================================
# INDEPENDENCE
# ============================================================

if independence is not None:

    score_column = None

    for c in independence.columns:

        if c.lower() != "observable":

            score_column = c

            break

    ind = {}

    for _, row in independence.iterrows():

        ind[row.Observable] = row[score_column]

    atlas["IndependenceScore"] = atlas.Observable.map(ind)

else:

    atlas["IndependenceScore"] = np.nan

# ============================================================
# MINIMAL PREDICTORS
# ============================================================

predictors = {}
predicted_by = {}

if minimal is not None:

    target_col = minimal.columns[0]

    pred_col = minimal.columns[1]

    for _, row in minimal.iterrows():

        target = row[target_col]

        plist = str(row[pred_col])

        predictors[target] = plist

        try:

            n = len(
                [
                    x
                    for x in plist.split(",")
                    if x.strip()
                ]
            )

        except:

            n = np.nan

        predicted_by[target] = n

atlas["PredictedBy"] = atlas.Observable.map(predictors)

atlas["MinimalPredictors"] = atlas.Observable.map(predicted_by)

atlas["CanPredict"] = atlas["PredictedBy"].notna()

# ============================================================
# DETERMINISTIC IDENTITIES
# ============================================================

atlas["DeterministicIdentity"] = False

for obs in atlas.Observable:

    if obs in [

        "AverageDistance",

        "MaximumDistance",

        "Diameter"

    ]:

        atlas.loc[
            atlas.Observable == obs,
            "DeterministicIdentity"
        ] = True

# ============================================================
# STRUCTURAL ROLE
# ============================================================

roles = []

for _, row in atlas.iterrows():

    pr = row.PageRank
    deg = row.DegreeCentrality
    sbs = row.StructuralBondStrength

    role = "Peripheral"

    if row.DeterministicIdentity:

        role = "Derived Observable"

    elif pr >= atlas.PageRank.quantile(0.90):

        role = "Hub"

    elif sbs >= atlas.StructuralBondStrength.quantile(0.75):

        role = "Connector"

    elif deg >= atlas.DegreeCentrality.quantile(0.75):

        role = "Module Core"

    elif deg == 0:

        role = "Isolated"

    roles.append(role)

atlas["StructuralRole"] = roles

# ============================================================
# RANKING
# ============================================================

ranking = atlas.sort_values(

    [

        "PageRank",

        "StructuralBondStrength",

        "DegreeCentrality"

    ],

    ascending=False

)

ranking.to_csv(

    OUT / "observable_ranking.csv",

    index=False

)

# ============================================================
# ROLES
# ============================================================

atlas[

    [

        "Observable",

        "StructuralRole"

    ]

].to_csv(

    OUT / "structural_roles.csv",

    index=False

)

# ============================================================
# PROFILES
# ============================================================

atlas.to_csv(

    OUT / "observable_profiles.csv",

    index=False

)

atlas.to_csv(

    OUT / "structural_atlas.csv",

    index=False

)

# ============================================================
# SUMMARY
# ============================================================

summary = atlas.groupby(

    "StructuralRole"

).size().reset_index()

summary.columns = [

    "Role",

    "Count"

]

summary.to_csv(

    OUT / "atlas_summary.csv",

    index=False

)

# ============================================================
# REPORT
# ============================================================

with open(

    OUT / "atlas_report.txt",

    "w"

) as f:

    f.write("=" * 60 + "\n")

    f.write("GER\n")

    f.write("S29-E6.1-L16\n")

    f.write("Structural Atlas\n")

    f.write("=" * 60 + "\n\n")

    f.write(f"Observables : {len(atlas)}\n\n")

    f.write("Structural Roles\n")

    f.write("----------------\n")

    for _, row in summary.iterrows():

        f.write(

            f"{row.Role:20s}"

            f"{row.Count}\n"

        )

    f.write("\n")

    f.write("Top Structural Ranking\n")

    f.write("----------------------\n")

    for _, row in ranking.head(10).iterrows():

        f.write(

            f"{row.Observable:20s}"

            f"{row.StructuralRole:20s}"

            f"PR={row.PageRank:.4f}\n"

        )

# ============================================================
# CERTIFICATE
# ============================================================

certificate = {

    "observables": int(len(atlas)),

    "communities": int(

        atlas.Community.nunique()

    ),

    "roles": int(

        atlas.StructuralRole.nunique()

    ),

    "hub_count": int(

        (atlas.StructuralRole == "Hub").sum()

    ),

    "connector_count": int(

        (atlas.StructuralRole == "Connector").sum()

    ),

    "derived_count": int(

        (atlas.StructuralRole == "Derived Observable").sum()

    )

}

with open(

    OUT / "scientific_certificate.json",

    "w"

) as f:

    json.dump(

        certificate,

        f,

        indent=4

    )

print()
print("=" * 70)
print("Experiment completed.")
print("Results saved to:")
print(OUT)
print("=" * 70)
