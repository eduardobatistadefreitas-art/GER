from GER_CORE.S26_B24_3_critical_curve import (
    find_critical_dt
)


def run_transition_scan():

    betas = [
        8,
        10,
        12,
        14,
        16,
        18,
        20,
        25
    ]


    curve = []


    for beta in betas:

        result = find_critical_dt(
            beta=beta,
            dts=[
                2.5e-4,
                1.25e-4,
                6.25e-5,
                3.125e-5
            ]
        )


        curve.append(result)


    return curve



def print_transition_scan(curve):

    print(
        "\nTRANSITION REGIME SCAN\n"
    )


    for item in curve:

        print(
            f"β={item['beta']:>5} | "
            f"dt_crit={item['critical_dt']}"
        )
