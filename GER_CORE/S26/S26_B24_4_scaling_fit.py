import numpy as np


def extract_critical_data(curve):

    beta = []
    dtcrit = []

    for item in curve:

        if item["critical_dt"] is not None:

            beta.append(
                item["beta"]
            )

            dtcrit.append(
                item["critical_dt"]
            )

    return (
        np.array(beta),
        np.array(dtcrit)
    )



def fit_scaling_law(curve):

    beta, dtcrit = extract_critical_data(
        curve
    )


    if len(beta) < 2:
        raise RuntimeError(
            "Dados insuficientes para ajuste."
        )


    x = np.log(beta)
    y = np.log(dtcrit)


    slope, intercept = np.polyfit(
        x,
        y,
        1
    )


    alpha = -slope
    C = np.exp(intercept)


    y_pred = (
        slope*x + intercept
    )


    ss_res = np.sum(
        (y-y_pred)**2
    )

    ss_tot = np.sum(
        (y-np.mean(y))**2
    )


    r2 = (
        1 -
        ss_res/ss_tot
        if ss_tot != 0
        else np.nan
    )


    return {
        "alpha": alpha,
        "C": C,
        "r2": r2,
        "beta": beta,
        "dtcrit": dtcrit
    }



def print_scaling_fit(result):

    print("\nSCALING ANALYSIS\n")

    print(
        f"alpha = {result['alpha']}"
    )

    print(
        f"C = {result['C']}"
    )

    print(
        f"R² = {result['r2']}"
    )

    print("\nLaw:")
    print(
        "dt_crit ~ C * beta^(-alpha)"
    )
