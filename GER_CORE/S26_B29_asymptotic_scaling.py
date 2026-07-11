from GER_CORE.S26_B24_3_critical_curve import (
    find_critical_dt
)


def run_asymptotic_scaling():

    betas = [
        25,
        30,
        40,
        50,
        75,
        100
    ]


    dts = [
        1.5e-4,
        1.25e-4,
        1.0e-4,
        7.5e-5,
        5.0e-5
    ]


    curve = []


    for beta in betas:

        result = find_critical_dt(
            beta=beta,
            dts=dts
        )

        curve.append(
            result
        )


    return curve



def print_asymptotic_scaling(curve):

    print(
        "\nASYMPTOTIC SCALING\n"
    )


    for item in curve:

        print(
            f"β={item['beta']:>5} | "
            f"dt_crit={item['critical_dt']}"
        )
