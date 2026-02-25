"""
rk45_knotted_trajectories.py
Simulazione base della dinamica di fase θ(t) con torque persistente
dal braiding ciclico trifoglio. Metodo RK45.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --------------------------------------------------
# Parametri di riferimento
# --------------------------------------------------
omega = 2 * np.pi * 1.2e9          # rad/s (~1.2 GHz)
g     = 0.85                       # coupling tipico
phi_offset = np.pi / 4

R_tau = np.exp(-1j * 3 * np.pi / 5)   # fase Fibonacci-like

t_span = (0, 60.0)
t_eval = np.linspace(0, 60, 2500)

# --------------------------------------------------
# Equazione del moto
# --------------------------------------------------
def dtheta(t, y):
    expn = 6 * np.sin(3 * t) / np.pi
    phase = np.angle(R_tau ** expn)
    drive = g * phase * np.sin(3 * t + phi_offset)
    return [omega + drive]

# --------------------------------------------------
# Integrazione
# --------------------------------------------------
sol = solve_ivp(dtheta, t_span, [0.0], method='RK45',
                t_eval=t_eval, rtol=1e-9, atol=1e-12)

# --------------------------------------------------
# Plot accumulo fase
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(sol.t, sol.y[0] % (2 * np.pi), lw=1.6, color='teal',
        label=r'$\%theta(t) \operatorname{mod} 2\pi$')
ax.axhline(4 * np.pi / 5, color='red', ls='--', alpha=0.65,
           label=r'$4\pi/5$ (ref R-matrix)')
ax.axhline(-3 * np.pi / 5, color='orange', ls=':', alpha=0.5,
           label=r'$-3\pi/5$ (ref)')

ax.set_title("Accumulo persistente di fase/torque topologico")
ax.set_xlabel("Tempo normalizzato")
ax.set_ylabel("Fase [rad]")
ax.grid(True, alpha=0.2)
ax.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig("rk45_knotted_phase_accumulation.png", dpi=180, bbox_inches='tight')
plt.show()

# --------------------------------------------------
# Statistiche
# --------------------------------------------------
drift = np.mean(np.diff(sol.y[0][-800:])) / np.mean(np.diff(sol.t[-800:]))
print(f"Drift medio (ultima parte): {drift:.4e} rad/s")
print(f"Fase finale mod 2π: {sol.y[0][-1] % (2*np.pi):.4f} rad")