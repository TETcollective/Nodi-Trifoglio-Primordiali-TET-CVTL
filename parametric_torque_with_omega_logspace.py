"""
parametric_torque_with_omega_logspace.py
Versione estesa per il paper: griglia 3D ridotta (g × ω logspace × fattore aurea)
Mostra dipendenza del torque netto medio da tutti e tre i parametri principali.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --------------------------------------------------
# Parametri fissi comuni
# --------------------------------------------------
phi_offset = np.pi / 4
R_tau = np.exp(-1j * 3 * np.pi / 5)
t_span = (0, 50.0)
t_eval = np.linspace(0, 50, 1800)          # risoluzione sufficiente
mid = len(t_eval) // 2                     # seconda metà per drift stabile

# --------------------------------------------------
# Griglie parametriche (bilanciate per ~10-20 min di calcolo)
# --------------------------------------------------
g_vals       = np.linspace(0.2, 1.6, 12)               # 12 valori
omega_vals   = np.logspace(np.log10(0.1e9), np.log10(5e9), 10)   # 10 valori log da 0.1 a 5 GHz
golden_f     = np.linspace(0.85, 1.15, 9)              # 9 valori intorno a 1

# Matrici per salvare torque netto [rad/s]
torque_g_omega   = np.full((len(g_vals), len(omega_vals)), np.nan)
torque_g_golden  = np.full((len(g_vals), len(golden_f)), np.nan)

# --------------------------------------------------
# Funzione driver (stessa per tutti)
# --------------------------------------------------
def dtheta(t, y, g, omega, golden_scale=1.0):
    expn = 6 * np.sin(3 * t) / np.pi * golden_scale
    phase = np.angle(R_tau ** expn)
    drive = g * phase * np.sin(3 * t + phi_offset)
    return [omega + drive]

# --------------------------------------------------
# 1. Griglia g vs omega (golden_scale = 1 fisso)
# --------------------------------------------------
print("Calcolo griglia g vs ω ...")
for i, g in enumerate(g_vals):
    for j, omega in enumerate(omega_vals):
        sol = solve_ivp(
            lambda t, y: dtheta(t, y, g, omega, golden_scale=1.0),
            t_span, [0.0], method='RK45', t_eval=t_eval,
            rtol=1e-8, atol=1e-10
        )
        if sol.success:
            drift = np.mean(np.diff(sol.y[0][mid:])) / np.mean(np.diff(sol.t[mid:]))
            torque_g_omega[i, j] = drift

# --------------------------------------------------
# 2. Griglia g vs golden_factor (ω medio fisso)
# --------------------------------------------------
omega_fixed = np.median(omega_vals)   # ~1 GHz circa
print(f"Calcolo griglia g vs fattore aureo (ω fissato a {omega_fixed/1e9:.2f} GHz)...")
for i, g in enumerate(g_vals):
    for k, gf in enumerate(golden_f):
        sol = solve_ivp(
            lambda t, y: dtheta(t, y, g, omega_fixed, golden_scale=gf),
            t_span, [0.0], method='RK45', t_eval=t_eval,
            rtol=1e-8, atol=1e-10
        )
        if sol.success:
            drift = np.mean(np.diff(sol.y[0][mid:])) / np.mean(np.diff(sol.t[mid:]))
            torque_g_golden[i, k] = drift

# --------------------------------------------------
# Plot combinato
# --------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8))

# Heatmap 1: g vs ω
im1 = ax1.contourf(omega_vals / 1e9, g_vals, torque_g_omega / 1e9,
                   levels=18, cmap='viridis')
fig.colorbar(im1, ax=ax1, label='Torque netto medio [Grad/s]')
ax1.set_xscale('log')
ax1.set_xlabel('ω base [GHz]')
ax1.set_ylabel('Coupling g')
ax1.set_title('Torque netto vs g e ω (aurea = 1)')

# Heatmap 2: g vs golden_factor
im2 = ax2.contourf(golden_f, g_vals, torque_g_golden / 1e9,
                   levels=18, cmap='magma')
fig.colorbar(im2, ax=ax2, label='Torque netto medio [Grad/s]')
ax2.axvline(1.0, color='white', ls='--', alpha=0.75, label='φ = 1 (aurea)')
ax2.set_xlabel('Fattore scala aurea')
ax2.set_ylabel('Coupling g')
ax2.set_title(f'Torque netto vs g e aurea\n(ω fissato a {omega_fixed/1e9:.2f} GHz)')
ax2.legend()

plt.tight_layout()
plt.savefig('torque_parametric_omega_logspace.png', dpi=160, bbox_inches='tight')
plt.show()

# --------------------------------------------------
# Risultati chiave
# --------------------------------------------------
print(f"Massimo torque netto (g vs ω):     {np.nanmax(torque_g_omega)/1e9:.3f} Grad/s")
print(f"Massimo torque netto (vs aurea):   {np.nanmax(torque_g_golden)/1e9:.3f} Grad/s")