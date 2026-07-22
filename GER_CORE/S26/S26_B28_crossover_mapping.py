from GER_CORE.S26_B24_3_critical_curve import (
    find_critical_dt
)


def run_crossover_mapping():

    betas = [
        14,
        15,
        16,
        17,
        18,
        20
    ]


    dts = [
        2.5e-4,
        2.25e-4,
        2.0e-4,
        1.75e-4,
        1.5e-4,
        1.25e-4
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



def print_crossover_mapping(curve):

    print(
        "\nCROSSOVER MAPPING\n"
    )


    for item in curve:

        print(
            f"β={item['beta']:>5} | "
            f"dt_crit={item['critical_dt']}"
        )
