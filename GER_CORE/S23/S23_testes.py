import numpy as np
from pathlib import Path
from scipy.integrate import solve_ivp

# ============================================================
# CARREGAMENTO
# ============================================================

ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S23/S23_FINAL/data")

K_rel = np.load(ROOT / "K_rel_star.npy")
K_refined = np.load(ROOT / "K_refined.npy")
K_eff = np.load(ROOT / "K_eff.npy")

print("=" * 70)
print("OPERADORES")
print("=" * 70)

print(f"K_rel      : {K_rel.shape}")
print(f"K_refined  : {K_refined.shape}")
print(f"K_eff      : {K_eff.shape}")

# ============================================================
# DECOMPOSIÇÃO
# ============================================================

S = 0.5 * (K_rel + K_rel.T)
A = 0.5 * (K_rel - K_rel.T)

print()
print("=" * 70)
print("DECOMPOSIÇÃO")
print("=" * 70)

print(f"||K_rel|| = {np.linalg.norm(K_rel):.6e}")
print(f"||S||     = {np.linalg.norm(S):.6e}")
print(f"||A||     = {np.linalg.norm(A):.6e}")

print()
print(f"Erro reconstrução = {np.linalg.norm(K_rel - (S+A)):.6e}")

# ============================================================
# VETOR INICIAL
# ============================================================

rng = np.random.default_rng(12345)

x0 = rng.normal(size=K_rel.shape[0])
x0 /= np.linalg.norm(x0)

# ============================================================
# INTEGRAÇÃO
# ============================================================

def analyze_operator(name, K):

    def rhs(t, x):
        return K @ x

    sol = solve_ivp(
        rhs,
        (0.0, 1000.0),
        x0,
        t_eval=np.linspace(0, 1000, 500),
        rtol=1e-9,
        atol=1e-12,
    )

    norms = np.linalg.norm(sol.y, axis=0)

    growth = max(norms[-1] / norms[0], 1e-300)

    lyap = np.log(growth) / (sol.t[-1] - sol.t[0])

    eig = np.linalg.eigvals(K)

    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    print(f"Norma operador ............ {np.linalg.norm(K):.6e}")

    print()
    print("ESPECTRO")

    print(f"Maior Re(λ) ............... {eig.real.max():.6e}")
    print(f"Menor Re(λ) ............... {eig.real.min():.6e}")
    print(f"Maior |Im(λ)| ............. {np.abs(eig.imag).max():.6e}")
    print(f"Raio espectral ............ {np.max(np.abs(eig)):.6e}")

    print()
    print("DINÂMICA")

    print(f"Norma inicial ............. {norms[0]:.6e}")
    print(f"Norma final ............... {norms[-1]:.6e}")
    print(f"Growth factor ............. {growth:.6e}")
    print(f"Lyapunov estimado ......... {lyap:.6e}")

    if lyap < 0:
        print("Resultado ................. ESTÁVEL")
    elif lyap > 0:
        print("Resultado ................. INSTÁVEL")
    else:
        print("Resultado ................. NEUTRO")

# ============================================================
# EXECUÇÃO
# ============================================================

analyze_operator("K_rel*", K_rel)

analyze_operator("Parte Simétrica S", S)

analyze_operator("Parte Antissimétrica A", A)

analyze_operator("Reconstrução S+A", S + A)

analyze_operator("K_refined", K_refined)

analyze_operator("K_eff", K_eff)

print()
print("=" * 70)
print("FIM DOS TESTES")
print("=" * 70)
