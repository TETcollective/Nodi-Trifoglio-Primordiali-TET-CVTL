"""
parametric_torque_minimal.py – versione leggera per il paper
Solo coupling g vs modulazione aurea (omega fisso)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parametri fissi
omega = 2 * np.pi * 1.2e9
phi_offset = np.pi / 4
R_tau = np.exp(-1j * 3 * np.pi / 5)
t_span = (0, 50.0)
t_eval = np.linspace(0, 50, 2000)
mid = len(t_eval) // 2

g_vals = np.linspace(0.2, 1.5, 14)
golden_f = np.linspace(0.85, 1.15, 11)

torque = np.zeros((len(g_vals), len(golden_f)))

for i, g in enumerate(g_vals):
    for j, gf in enumerate(golden_f):
        def dtheta(t, y):
            expn = 6 * np.sin(3*t) / np.pi * gf
            phase = np.angle(R_tau ** expn)
            drive = g * phase * np.sin(3*t + phi_offset)
            return [omega + drive]

        sol = solve_ivp(dtheta, t_span, [0.0], t_eval=t_eval, method='RK45', rtol=1e-8)
        if sol.success:
            drift = np.mean(np.diff(sol.y[0][mid:])) / np.mean(np.diff(sol.t[mid:]))
            torque[i,j] = drift
        else:
            torque[i,j] = np.nan

# Plot
plt.figure(figsize=(7,5.5))
plt.contourf(golden_f, g_vals, torque / 1e9, levels=20, cmap='viridis')
plt.colorbar(label='Torque netto medio [Grad/s]')
plt.xlabel('Fattore scala aurea')
plt.ylabel('Coupling g')
plt.title('Torque persistente vs g e modulazione aurea\n(ω = 1.2 GHz fissato)')
plt.axvline(1.0, color='white', ls='--', alpha=0.7, label='φ = 1 (aurea esatta)')
plt.legend()
plt.tight_layout()
plt.savefig('torque_g_vs_golden.png', dpi=160)
plt.show()

print("Max torque netto:", np.nanmax(torque)/1e9, "Grad/s")