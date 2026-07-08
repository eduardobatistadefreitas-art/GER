"""
===============================================================================
S26_B2_core.py
Núcleo Computacional da Série S26-B

Parte 1A
Infraestrutura básica
===============================================================================
"""

import numpy as np
import scipy.linalg as la


# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

ENERGY_TOL = 1e-4
DIVERGENCE_AMPLITUDE = 1e6
EPS = 1e-15


# =============================================================================
# CONSTRUÇÃO DA REDE
# =============================================================================

def build_ring_graph(n):
    """
    Constrói o grafo periódico F1.

    Retorna
    -------
    A : matriz de adjacência
    L : Laplaciano
    theta : coordenadas angulares
    """

    A = np.zeros((n, n))

    for i in range(n):
        A[i, (i + 1) % n] = 1.0
        A[i, (i - 1) % n] = 1.0

    D = np.diag(np.sum(A, axis=1))

    L = D - A

    theta = np.linspace(
        0.0,
        2.0*np.pi,
        n,
        endpoint=False
    )

    return A, L, theta


# =============================================================================
# BASE ESPECTRAL
# =============================================================================

def spectral_basis(L):
    """
    Diagonalização do Laplaciano.
    """

    eigenvalues, eigenvectors = la.eigh(L)

    eigenvalues[np.abs(eigenvalues) < 1e-12] = 0.0

    return eigenvalues, eigenvectors


# =============================================================================
# CONDIÇÃO INICIAL
# =============================================================================

def gaussian_packet(theta,
                    center=np.pi,
                    sigma=0.10):
    """
    Pulso gaussiano inicial.
    """

    return np.exp(
        -(theta-center)**2 /
        (2*sigma**2)
    )


# =============================================================================
# POTENCIAIS
# =============================================================================

class Potential:

    @staticmethod
    def evaluate(gamma, model):

        if model == "A":

            F = gamma**2

            V = gamma**3 / 3.0

        elif model == "B":

            F = gamma**2 / (1.0 + gamma**2)

            V = gamma - np.arctan(gamma)

        elif model == "C":

            F = gamma**3

            V = gamma**4 / 4.0

        else:

            raise ValueError(
                f"Potencial desconhecido: {model}"
            )

        return F, V


# =============================================================================
# INICIALIZAÇÃO DE VERLET (O(dt²))
# =============================================================================

def initialize_verlet(
    gamma0,
    L,
    beta,
    potential,
    dt
):
    """
    Inicialização consistente de segunda ordem.
    """

    F0, _ = Potential.evaluate(
        gamma0,
        potential
    )

    accel0 = -(L @ gamma0) + beta*F0

    gamma_minus = (
        gamma0
        + 0.5*dt**2*accel0
    )

    return gamma_minus


# =============================================================================
# DETECTOR DE DIVERGÊNCIA
# =============================================================================

def check_divergence(
    gamma,
    energy_error=None
):

    amp = np.max(np.abs(gamma))

    if np.isnan(amp):
        return True

    if np.isinf(amp):
        return True

    if amp > DIVERGENCE_AMPLITUDE:
        return True

    if energy_error is not None:
        if np.isnan(energy_error):
            return True

        if np.isinf(energy_error):
            return True

    return False
  # =============================================================================
# HAMILTONIANA
# =============================================================================

def compute_hamiltonian(
    gamma,
    velocity,
    L,
    beta,
    potential
):
    """
    Calcula a Hamiltoniana total do sistema.
    """

    _, V = Potential.evaluate(
        gamma,
        potential
    )

    kinetic = 0.5 * np.sum(velocity**2)

    potential_linear = (
        0.5 *
        np.dot(
            gamma,
            L @ gamma
        )
    )

    potential_nonlinear = (
        -beta *
        np.sum(V)
    )

    return (
        kinetic
        + potential_linear
        + potential_nonlinear
    )


# =============================================================================
# NORMA L2
# =============================================================================

def compute_l2_norm(gamma):

    return np.sqrt(
        np.sum(gamma**2)
    )


# =============================================================================
# AMPLITUDE MÁXIMA
# =============================================================================

def compute_max_amplitude(gamma):

    return np.max(
        np.abs(gamma)
    )


# =============================================================================
# PROJEÇÃO ESPECTRAL
# =============================================================================

def modal_projection(
    gamma,
    eigenvectors
):
    """
    Projeta o campo na base modal.
    """

    modal = (
        eigenvectors.T
        @ gamma
    )

    energy = modal**2

    probability = (
        energy /
        (
            np.sum(energy)
            + EPS
        )
    )

    return (
        modal,
        energy,
        probability
    )


# =============================================================================
# ENTROPIA ESPECTRAL
# =============================================================================

def compute_spectral_entropy(
    probability
):

    return -np.sum(
        probability *
        np.log(
            probability + EPS
        )
    )


# =============================================================================
# MODO DOMINANTE
# =============================================================================

def dominant_mode(
    probability
):

    return int(
        np.argmax(
            probability
        )
    )


# =============================================================================
# CENTRO MODAL
# =============================================================================

def modal_center(
    probability
):

    modes = np.arange(
        len(probability)
    )

    return np.sum(
        modes *
        probability
    )


# =============================================================================
# LARGURA MODAL
# =============================================================================

def modal_width(
    probability
):

    modes = np.arange(
        len(probability)
    )

    center = modal_center(
        probability
    )

    variance = np.sum(
        probability *
        (modes-center)**2
    )

    return np.sqrt(
        variance
    )


# =============================================================================
# MÉTRICAS CIRCULARES
# =============================================================================

def compute_circular_metrics(
    gamma,
    theta
):
    """
    Estatística circular consistente
    para topologia periódica.
    """

    weight = np.abs(gamma)

    norm = np.sum(weight)

    if norm < EPS:

        return {
            "center":0.0,
            "width":0.0,
            "R":0.0,
            "skewness":0.0
        }

    weight = weight / norm

    C = np.sum(
        weight *
        np.cos(theta)
    )

    S = np.sum(
        weight *
        np.sin(theta)
    )

    R = np.sqrt(
        C**2 + S**2
    )

    theta_mean = np.arctan2(
        S,
        C
    )

    theta_dev = np.arctan2(
        np.sin(theta-theta_mean),
        np.cos(theta-theta_mean)
    )

    width = np.sqrt(
        max(
            0.0,
            -2.0*np.log(
                max(R,EPS)
            )
        )
    )

    skewness = np.sum(
        weight *
        np.sin(
            3.0*theta_dev
        )
    )

    return {

        "center":theta_mean,

        "width":width,

        "R":R,

        "skewness":skewness
    }


# =============================================================================
# ERRO RELATIVO DE ENERGIA
# =============================================================================

def relative_energy_error(
    energy_initial,
    energy_final
):

    return (
        np.abs(
            energy_final
            -
            energy_initial
        )
        /
        (
            np.abs(
                energy_initial
            )
            +
            EPS
        )
    )


# =============================================================================
# SNAPSHOT PADRONIZADO
# =============================================================================

def build_snapshot(
    step,
    time,
    gamma,
    velocity,
    L,
    beta,
    potential,
    eigenvectors,
    theta
):
    """
    Gera um snapshot completo do estado.
    """

    H = compute_hamiltonian(
        gamma,
        velocity,
        L,
        beta,
        potential
    )

    l2 = compute_l2_norm(
        gamma
    )

    amp = compute_max_amplitude(
        gamma
    )

    modal,
    modal_energy,
    probability = modal_projection(
        gamma,
        eigenvectors
    )

    entropy = compute_spectral_entropy(
        probability
    )

    circle = compute_circular_metrics(
        gamma,
        theta
    )

    return {

        "step":step,

        "time":time,

        "energy":H,

        "l2":l2,

        "amplitude":amp,

        "dominant_mode":
            dominant_mode(
                probability
            ),

        "modal_center":
            modal_center(
                probability
            ),

        "modal_width":
            modal_width(
                probability
            ),

        "spectral_entropy":
            entropy,

        "circular":
            circle,

        "probability":
            probability,

        "modal_energy":
            modal_energy
      # =============================================================================
# MOTOR DE EVOLUÇÃO TEMPORAL
# =============================================================================

def run_engine(
    n=384,
    timesteps=2000,
    dt=2.5e-4,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    sigma=0.10
):
    """
    Motor único da série S26-B.

    Retorna toda a evolução necessária para qualquer auditoria.
    """

    _, L, theta = build_ring_graph(n)

    eigenvalues, eigenvectors = spectral_basis(L)

    gamma = gaussian_packet(
        theta,
        sigma=sigma
    )

    gamma_old = initialize_verlet(
        gamma,
        L,
        beta,
        potential,
        dt
    )

    velocity0 = (gamma - gamma_old) / dt

    energy0 = compute_hamiltonian(
        gamma,
        velocity0,
        L,
        beta,
        potential
    )

    snapshots = []

    diverged = False

    for step in range(timesteps):

        force, _ = Potential.evaluate(
            gamma,
            potential
        )

        acceleration = (
            -(L @ gamma)
            +
            beta*force
        )

        gamma_new = (
            2.0*gamma
            -
            gamma_old
            +
            dt*dt*acceleration
        )

        velocity = (
            gamma_new
            -
            gamma_old
        ) / (2.0*dt)

        energy = compute_hamiltonian(
            gamma,
            velocity,
            L,
            beta,
            potential
        )

        error = relative_energy_error(
            energy0,
            energy
        )

        if check_divergence(
            gamma,
            error
        ):
            diverged = True

        if (
            step % snapshot_stride == 0
            or step == timesteps-1
        ):

            snap = build_snapshot(
                step=step,
                time=step*dt,
                gamma=gamma,
                velocity=velocity,
                L=L,
                beta=beta,
                potential=potential,
                eigenvectors=eigenvectors,
                theta=theta
            )

            snap["energy_error"] = error

            snapshots.append(snap)

        gamma_old = gamma
        gamma = gamma_new

    final_velocity = (
        gamma-gamma_old
    )/dt

    final_energy = compute_hamiltonian(
        gamma,
        final_velocity,
        L,
        beta,
        potential
    )

    final_error = relative_energy_error(
        energy0,
        final_energy
    )

    return {

        "configuration":{

            "n":n,

            "dt":dt,

            "timesteps":timesteps,

            "beta":beta,

            "potential":potential

        },

        "initial":{

            "energy":energy0,

            "l2":compute_l2_norm(gamma_old),

            "amplitude":compute_max_amplitude(gamma_old)

        },

        "final":{

            "energy":final_energy,

            "l2":compute_l2_norm(gamma),

            "amplitude":compute_max_amplitude(gamma),

            "energy_error":final_error

        },

        "snapshots":snapshots,

        "gamma":gamma,

        "laplacian":L,

        "eigenvalues":eigenvalues,

        "eigenvectors":eigenvectors,

        "diverged":diverged

    }


# =============================================================================
# EXECUTOR DE MATRIZ DE PARÂMETROS
# =============================================================================

def run_parameter_grid(
    beta_values,
    potentials,
    **kwargs
):
    """
    Executa automaticamente todas
    as combinações Potencial × Beta.
    """

    results = {}

    for pot in potentials:

        results[pot] = {}

        for beta in beta_values:

            results[pot][beta] = run_engine(
                beta=beta,
                potential=pot,
                **kwargs
            )

    return results


# =============================================================================
# RESUMO NUMÉRICO
# =============================================================================

def summarize_run(result):

    return {

        "energy_error":
            result["final"]["energy_error"],

        "final_l2":
            result["final"]["l2"],

        "final_amplitude":
            result["final"]["amplitude"],

        "diverged":
            result["diverged"]

    }


# =============================================================================
# FIM DO NÚCLEO
# =============================================================================
    }
