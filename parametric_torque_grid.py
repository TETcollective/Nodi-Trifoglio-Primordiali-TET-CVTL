"""
parametric_torque_grid.py
================================================================
Grid search parametrico per il torque netto medio in funzione di:
- g (coupling anyon-vacuum)
- omega_base (velocità di shift / frequenza base)
- golden_factor (modulazione scala aurea sul drive)

Calcola il drift medio (torque netto) per ogni combinazione e produce heatmap/contour.

Autore: Tetcollective collab
Data: 2026
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# Parametri base fissi
# --------------------------------------------------
phi_offset   = np.pi / 4
R_tau_phase  = np.exp(-1j * 3 * np.pi / 5)
t_span       = (0, 60.0)
t_eval       = np.linspace(t_span[0], t_span[1], 3000)
mid_idx      = len(t_eval) // 2   # usiamo seconda metà per drift stabile

# --------------------------------------------------
# Range parametrici (grid)
# --------------------------------------------------
n_g      = 18
n_omega  = 16
n_golden = 11

g_values     = np.linspace(0.1, 1.8, n_g)
omega_values = np.logspace(np.log10(1e8), np.log10(5e9), n_omega)   # da 0.1 a 5 GHz
golden_f     = np.linspace(0.80, 1.20, n_golden)                     # ±20% intorno a φ

# Matrice per salvare torque netto medio [rad/s]
torque_grid_g_omega   = np.zeros((n_g, n_omega))
torque_grid_g_golden  = np.zeros((n_g, n_golden))

# --------------------------------------------------
# Funzione dinamica (stessa di prima)
# --------------------------------------------------
def theta_dot(t, y, g, omega, golden_scale=1.0):
    theta = y[0]
    exponent = 6 * np.sin(3 * t) / np.pi * golden_scale
    anyon_factor = np.angle(R_tau_phase ** exponent)
    drive = g * anyon_factor * np.sin(3 * t + phi_offset)
    return [omega + drive]

# --------------------------------------------------
# Grid search 1: g vs omega (golden fisso = 1)
# --------------------------------------------------
print("Computing g vs omega grid...")
for i, g in enumerate(g_values):
    for j, omega in enumerate(omega_values):
        sol = solve_ivp(
            lambda t, y: theta_dot(t, y, g, omega, golden_scale=1.0),
            t_span, [0.0], method='RK45', t_eval=t_eval,
            rtol=1e-8, atol=1e-10
        )
        if sol.success:
            drift = np.mean(np.diff(sol.y[0][mid_idx:])) / np.mean(np.diff(sol.t[mid_idx:]))
            torque_grid_g_omega[i, j] = drift
        else:
            torque_grid_g_omega[i, j] = np.nan

# --------------------------------------------------
# Grid search 2: g vs golden_factor (omega fisso medio)
# --------------------------------------------------
omega_fixed = np.median(omega_values)
print("Computing g vs golden_factor grid...")
for i, g in enumerate(g_values):
    for k, gf in enumerate(golden_f):
        sol = solve_ivp(
            lambda t, y: theta_dot(t, y, g, omega_fixed, golden_scale=gf),
            t_span, [0.0], method='RK45', t_eval=t_eval,
            rtol=1e-8, atol=1e-10
        )
        if sol.success:
            drift = np.mean(np.diff(sol.y[0][mid_idx:])) / np.mean(np.diff(sol.t[mid_idx:]))
            torque_grid_g_golden[i, k] = drift
        else:
            torque_grid_g_golden[i, k] = np.nan

# --------------------------------------------------
# Plot heatmap 1: torque vs g e omega
# --------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

sns.heatmap(
    torque_grid_g_omega / 1e9,  # in Grad/s per leggibilità
    xticklabels=np.round(omega_values / 1e9, 1),
    yticklabels=np.round(g_values, 2),
    cmap='viridis', ax=ax1, cbar_kws={'label': 'Torque netto medio [Grad/s]'}
)
ax1.set_title("Torque netto vs coupling g e frequenza base ω")
ax1.set_xlabel("ω [GHz]")
ax1.set_ylabel("g (coupling)")

# --------------------------------------------------
# Plot heatmap 2: torque vs g e scala aurea
# --------------------------------------------------
sns.heatmap(
    torque_grid_g_golden / 1e9,
    xticklabels=np.round(golden_f, 2),
    yticklabels=np.round(g_values, 2),
    cmap='magma', ax=ax2, cbar_kws={'label': 'Torque netto medio [Grad/s]'}
)
ax2.set_title(f"Torque netto vs g e modulazione aurea\n(ω fissato a {omega_fixed/1e9:.1f} GHz)")
ax2.set_xlabel("Fattore scala aurea")
ax2.set_ylabel("g (coupling)")

plt.tight_layout()
plt.savefig("torque_parametric_grid.png", dpi=160, bbox_inches='tight')
plt.show()

print("Massimo torque netto osservato:", np.nanmax(torque_grid_g_omega) / 1e9, "Grad/s")