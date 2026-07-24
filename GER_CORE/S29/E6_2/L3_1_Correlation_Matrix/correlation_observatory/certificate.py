"""
============================================================
GER

L3.1 Correlation Matrix

Certificate

============================================================
"""

import numpy as np


def build_certificate(results):

    variables = results["variables"]

    n = len(variables)

    checks = {

        "dataset_loaded": True,

        "variables": n,

        "pearson_valid": False,

        "spearman_valid": False,

        "kendall_valid": False,

        "same_variables": False,

        "same_order": False,

        "status": "FAIL",

    }

    names = None

    success = True

    for method in (

        "pearson",

        "spearman",

        "kendall",

    ):

        matrix = results[method]["matrix"]

        valid = True

        if matrix.shape != (n, n):

            valid = False

        if np.isnan(matrix.values).any():

            valid = False

        if not np.allclose(

            np.diag(matrix),

            np.ones(n),

            atol=1e-10,

        ):

            valid = False

        checks[f"{method}_valid"] = valid

        success &= valid

        current = list(matrix.columns)

        if names is None:

            names = current

        else:

            if current != names:

                success = False

    checks["same_variables"] = True

    checks["same_order"] = success

    if (

        checks["pearson_valid"]

        and checks["spearman_valid"]

        and checks["kendall_valid"]

        and checks["same_order"]

    ):

        checks["status"] = "PASS"

    return checks
