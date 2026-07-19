"""
============================================================
GER
S29-E5

REGION CONSTRUCTION

============================================================

Objective
---------
Construct the first permanent Signature Space of the
Relational Spectral Geometry (RSG) framework.

This experiment converts the experimental stability regions
identified in S29 into permanent geometric objects belonging
to the CORE geometry infrastructure.

Inputs
------
RESULTS/S29_E3_1_signature_map.csv
RESULTS/S29_E3_2_stability_regions.csv
RESULTS/S29_E3_3_region_geometry.csv

Outputs
-------
RESULTS/S29_E5_signature_space.json
RESULTS/S29_E5_regions.json
RESULTS/S29_E5_summary.txt

Author
------
GER Project
"""

from pathlib import Path
import json

import pandas as pd

from GER.CORE.geometry.region import Region
from GER.CORE.geometry.signature_space import SignatureSpace
from GER.CORE.geometry.region_io import RegionIO


# ============================================================
# PATHS
# ============================================================

INPUT_DIR = Path("RESULTS")

SIGNATURE_FILE = (
    INPUT_DIR /
    "S29_E3_1_signature_map.csv"
)

REGION_FILE = (
    INPUT_DIR /
    "S29_E3_2_stability_regions.csv"
)

GEOMETRY_FILE = (
    INPUT_DIR /
    "S29_E3_3_region_geometry.csv"
)


OUTPUT_DIR = Path("RESULTS")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


SPACE_JSON = (
    OUTPUT_DIR /
    "S29_E5_signature_space.json"
)

REGIONS_JSON = (
    OUTPUT_DIR /
    "S29_E5_regions.json"
)

SUMMARY_FILE = (
    OUTPUT_DIR /
    "S29_E5_summary.txt"
)


# ============================================================
# AUXILIARY SIGNATURE
# ============================================================

class ExperimentalSignature:
    """
    Minimal wrapper allowing the experimental signatures
    produced during S29 to be inserted into the permanent
    SignatureSpace object.

    Only the public interface required by SignatureSpace
    is implemented.
    """

    def __init__(self, signature_id, data):

        self.id = signature_id

        self.data = dict(data)

    def as_dict(self):

        return dict(self.data)

# ============================================================
# DATA LOADING
# ============================================================

def load_inputs():

    print()

    print("Reading experimental results...")

    signatures = pd.read_csv(
        SIGNATURE_FILE
    )

    regions = pd.read_csv(
        REGION_FILE
    )

    geometry = pd.read_csv(
        GEOMETRY_FILE
    )

    signatures.columns = (
        signatures.columns
        .str.strip()
    )

    regions.columns = (
        regions.columns
        .str.strip()
    )

    geometry.columns = (
        geometry.columns
        .str.strip()
    )

    print(
        f"Signatures : {len(signatures)}"
    )

    print(
        f"Regions    : {len(regions)}"
    )

    return (
        signatures,
        regions,
        geometry,
    )


# ============================================================
# SIGNATURE SPACE CONSTRUCTION
# ============================================================

def build_signature_space(
    signatures_df,
):

    print()

    print(
        "Creating SignatureSpace..."
    )

    space = SignatureSpace()

    signature_objects = {}

    for index, row in (
        signatures_df.iterrows()
    ):

        signature_id = (
            f"S{index:05d}"
        )

        signature = (
            ExperimentalSignature(
                signature_id,
                row.to_dict(),
            )
        )

        space.add_signature(
            signature
        )

        signature_objects[
            signature_id
        ] = signature

    print(
        f"Registered signatures : "
        f"{len(signature_objects)}"
    )

    return (
        space,
        signature_objects,
    )


# ============================================================
# AUXILIARY SEARCH
# ============================================================

def signatures_inside_interval(
    signatures_df,
    gamma0,
    gamma1,
):

    subset = signatures_df[
        (
            signatures_df["gamma"]
            >= gamma0
        )
        &
        (
            signatures_df["gamma"]
            <= gamma1
        )
    ]

    ids = []

    for idx in subset.index:

        ids.append(
            f"S{idx:05d}"
        )

    return ids

# ============================================================
# REGION CONSTRUCTION
# ============================================================

def build_regions(

    space,
    signatures_df,
    regions_df,
    geometry_df,

):

    print()

    print(
        "Constructing Regions..."
    )

    region_objects = []

    for _, region in regions_df.iterrows():

        gamma0 = region["gamma_start"]

        gamma1 = region["gamma_end"]

        label = region["classification"]

        geometry = geometry_df[
            geometry_df["Region"] == label
        ].iloc[0]

        signature_ids = signatures_inside_interval(
            signatures_df,
            gamma0,
            gamma1,
        )

        centroid = (

            float(
                geometry["CentroidDiameter"]
            ),

            float(
                geometry["CentroidConvergence"]
            ),

            float(
                geometry["CentroidRecurrence"]
            ),

            float(
                geometry["CentroidDrift"]
            ),

        )

        radius = float(
            geometry["MeanRadius"]
        )

        attributes = {

            "gamma_start": float(gamma0),

            "gamma_end": float(gamma1),

            "delta_gamma": float(
                geometry["DeltaGamma"]
            ),

            "n_signatures": int(
                geometry["N"]
            ),

            "compactness": float(
                geometry["Compactness"]
            ),

            "packing": float(
                geometry["Packing"]
            ),

            "anisotropy": float(
                geometry["Anisotropy"]
            ),

            "uniformity": float(
                geometry["Uniformity"]
            ),

            "internal_diameter": float(
                geometry["InternalDiameter"]
            ),

        }

        region_object = Region(

            id=f"R{len(region_objects)+1:03d}",

            label=label,

            signature_ids=tuple(
                signature_ids
            ),

            centroid=centroid,

            radius=radius,

            attributes=attributes,

        )

        space.add_region(
            region_object
        )

        for signature_id in signature_ids:

            space.assign_signature(

                signature_id,

                region_object.id,

            )

        region_objects.append(
            region_object
        )

        print(

            f"{region_object.id}"

            f" -> "

            f"{len(signature_ids)} signatures"

        )

    print()

    print(

        "Regions constructed:",

        len(region_objects),

    )

    return region_objects
# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    space,
    region_objects,
):

    print()

    print(
        "Saving geometry objects..."
    )

    RegionIO.save_signature_space(
        space,
        SPACE_JSON,
    )

    regions_data = [

        region.as_dict()

        for region in region_objects

    ]

    with open(

        REGIONS_JSON,

        "w",

        encoding="utf-8",

    ) as fp:

        json.dump(

            regions_data,

            fp,

            indent=4,

            ensure_ascii=False,

        )

    print("Done.")


# ============================================================
# SUMMARY
# ============================================================

def save_summary(
    space,
    region_objects,
):

    lines = []

    lines.append("=" * 60)

    lines.append(
        "GER S29-E5"
    )

    lines.append(
        "REGION CONSTRUCTION"
    )

    lines.append("=" * 60)

    lines.append("")

    lines.append(
        f"Regions              : {len(region_objects)}"
    )

    lines.append(
        f"Signatures           : {len(space._signatures)}"
    )

    lines.append("")

    lines.append(
        "Region Summary"
    )

    lines.append("-" * 60)

    for region in region_objects:

        lines.append("")

        lines.append(
            f"{region.id} ({region.label})"
        )

        lines.append(
            f"  Signatures : {len(region.signature_ids)}"
        )

        lines.append(
            f"  Radius     : {region.radius:.6f}"
        )

        lines.append(
            f"  Dimension  : {region.dimension()}"
        )

        lines.append(
            f"  Centroid   : {region.centroid}"
        )

    lines.append("")
    lines.append("-" * 60)

    lines.append(
        "SignatureSpace Summary"
    )

    summary = space.summary()

    for key, value in summary.items():

        lines.append(
            f"{key} : {value}"
        )

    with open(

        SUMMARY_FILE,

        "w",

        encoding="utf-8",

    ) as fp:

        fp.write(
            "\n".join(lines)
        )

    print(
        "Summary saved."
    )

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("GER S29-E5")
    print("REGION CONSTRUCTION")
    print("=" * 60)

    # --------------------------------------------------------
    # Read previous experimental results
    # --------------------------------------------------------

    (
        signatures_df,
        regions_df,
        geometry_df,
    ) = load_inputs()

    # --------------------------------------------------------
    # Create Signature Space
    # --------------------------------------------------------

    (
        space,
        _,
    ) = build_signature_space(
        signatures_df,
    )

    # --------------------------------------------------------
    # Construct Regions
    # --------------------------------------------------------

    region_objects = build_regions(

        space,

        signatures_df,

        regions_df,

        geometry_df,

    )

    # --------------------------------------------------------
    # Persist objects
    # --------------------------------------------------------

    save_results(

        space,

        region_objects,

    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    save_summary(

        space,

        region_objects,

    )

    print()
    print("=" * 60)
    print("S29-E5 COMPLETED")
    print("=" * 60)
    print()
    print(f"Signature Space : {SPACE_JSON}")
    print(f"Regions         : {REGIONS_JSON}")
    print(f"Summary         : {SUMMARY_FILE}")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
