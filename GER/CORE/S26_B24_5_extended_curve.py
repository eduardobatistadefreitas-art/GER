%%writefile GER_CORE/S26_B24_5_extended_curve.py

from GER_CORE.S26_B24_3_critical_curve import (
    find_critical_dt
)


def run_extended_curve():

    betas = [
        0.5,
        1,
        2,
        5,
        10,
        20,
        30,
        50,
        75,
        100
    ]


    curve = []


    for beta in betas:

        result = find_critical_dt(
            beta=beta,
            dts=[
                2.5e-4,
                1.25e-4,
                6.25e-5,
                3.125e-5,
                1.5625e-5,
                7.8125e-6
            ]
        )


        curve.append(result)


    return curve



def print_extended_curve(curve):

    print("\nEXTENDED CRITICAL DT CURVE\n")

    for item in curve:

        print(
            f"β={item['beta']:>6} | "
            f"dt_crit={item['critical_dt']}"
        )
