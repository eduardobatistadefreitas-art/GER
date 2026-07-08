import numpy as np


# ============================================================
# S26-B.2.2
# AUDITORIA DE TRANSFERÊNCIA MODAL
# ============================================================


def analyze_modal_transfer(result):
    """
    Analisa evolução espectral usando snapshots
    produzidos pelo ger_engine.

    Entrada:
        result = saída do run_engine()

    Retorno:
        dicionário com séries temporais
    """

    snapshots = result["snapshots"]

    times = []
    entropy = []
    spectral_center = []
    spectral_width = []
    dominant_modes = []

    low_energy = []
    mid_energy = []
    high_energy = []

    for snap in snapshots:

        p = np.array(
            snap["probability"],
            dtype=float
        )

        p = p / (np.sum(p) + 1e-15)

        modes = np.arange(len(p))


        # ---------------------------------
        # Entropia espectral
        # ---------------------------------

        S = -np.sum(
            p * np.log(p + 1e-15)
        )


        # ---------------------------------
        # Centro espectral
        # ---------------------------------

        kc = np.sum(
            modes * p
        )


        # ---------------------------------
        # Largura espectral
        # ---------------------------------

        width = np.sqrt(
            np.sum(
                (modes-kc)**2 * p
            )
        )


        # ---------------------------------
        # Faixas espectrais
        # ---------------------------------

        n = len(p)

        i1 = int(0.25*n)
        i2 = int(0.75*n)


        low = np.sum(
            p[:i1]
        )

        mid = np.sum(
            p[i1:i2]
        )

        high = np.sum(
            p[i2:]
        )


        # guardar

        times.append(
            snap["time"]
        )

        entropy.append(S)

        spectral_center.append(kc)

        spectral_width.append(width)

        dominant_modes.append(
            snap["dominant_mode"]
        )

        low_energy.append(low)

        mid_energy.append(mid)

        high_energy.append(high)



    return {

        "time": np.array(times),

        "entropy": np.array(entropy),

        "spectral_center": np.array(
            spectral_center
        ),

        "spectral_width": np.array(
            spectral_width
        ),

        "dominant_mode": np.array(
            dominant_modes
        ),

        "low_energy": np.array(
            low_energy
        ),

        "mid_energy": np.array(
            mid_energy
        ),

        "high_energy": np.array(
            high_energy
        )

    }



# ============================================================
# TAXAS DE TRANSFERÊNCIA
# ============================================================


def calculate_transfer_rates(data):

    """
    Calcula derivadas temporais discretas
    das grandezas espectrais.
    """

    t = data["time"]

    dt = np.diff(t)


    rates = {}


    for key in [

        "entropy",
        "spectral_center",
        "spectral_width",
        "high_energy"

    ]:

        values = data[key]


        rates[key+"_rate"] = (
            np.diff(values)
            /
            (dt + 1e-15)
        )


    return rates



# ============================================================
# RELATÓRIO
# ============================================================


def print_modal_report(data, rates):

    print("="*70)
    print("S26-B.2.2 — RELATÓRIO DE TRANSFERÊNCIA MODAL")
    print("="*70)


    print()

    print(
        "Entropia inicial/final:",
        data["entropy"][0],
        " --> ",
        data["entropy"][-1]
    )


    print(
        "Centro espectral:",
        data["spectral_center"][0],
        " --> ",
        data["spectral_center"][-1]
    )


    print(
        "Largura espectral:",
        data["spectral_width"][0],
        " --> ",
        data["spectral_width"][-1]
    )


    print(
        "Modo dominante:",
        data["dominant_mode"][0],
        " --> ",
        data["dominant_mode"][-1]
    )


    print()

    print(
        "Energia baixa frequência:",
        data["low_energy"][0],
        " --> ",
        data["low_energy"][-1]
    )


    print(
        "Energia média frequência:",
        data["mid_energy"][0],
        " --> ",
        data["mid_energy"][-1]
    )


    print(
        "Energia alta frequência:",
        data["high_energy"][0],
        " --> ",
        data["high_energy"][-1]
    )


    print()

    print(
        "Taxa média crescimento entropia:",
        np.mean(
            rates["entropy_rate"]
        )
    )


    print(
        "Taxa média transferência alta frequência:",
        np.mean(
            rates["high_energy_rate"]
        )
    )


    print("="*70)



# ============================================================
# EXECUÇÃO DIRETA
# ============================================================


def run_B22_case(engine_result):

    data = analyze_modal_transfer(
        engine_result
    )

    rates = calculate_transfer_rates(
        data
    )

    print_modal_report(
        data,
        rates
    )


    return {

        "analysis": data,

        "rates": rates

      }
