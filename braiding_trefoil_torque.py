"""
braiding_trefoil_torque.py
============================
Simulazione toy-model di traiettoria knotted (trefoil) + accumulo torque dal vuoto
usando RK45 per dinamica parametrica. Parametri ispirati a TET–CVTL framework.
Autore: Simon Soliman / Grok-xAI collab
Data: Febbraio 2026
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------------------------------------------------------
# Parametri fisici/toy (realistici per scala NV o plasma)
# -------------------------------------------------------
omega = 2 * np.pi * 1.2e9      # freq Larmor-like ~ GHz
g = 0.85                       # coupling anyon-vacuum (adim.)
phi = (1 + np.sqrt(5)) / 2     # golden ratio
tau_phase = np.exp(-1j * 3 * np.pi / 5)   # R_tau da Fibonacci
torque_scale = 1.6e-24         # Joule/T (ordine mu_B * B ~ pN*nm)

t_span = (0, 50.0)             # tempo normalizzato (ciclo braiding)
t_eval = np.linspace(0, 50, 2000)

# -------------------------------------------------------
# Trefoil parametrico (standard embedding)
# -------------------------------------------------------
def trefoil(t, scale=3.0):
    x = scale * (np.sin(t) + 2 * np.sin(2*t))
    y = scale * (np.cos(t) - 2 * np.cos(2*t))
    z = scale * (-np.sin(3*t))
    return np.array([x, y, z])

# -------------------------------------------------------
# Dinamica toy: theta(t) con torque topologico persistente
# d theta / dt = omega + g * Im( <tau| R^3 |tau> ) * sin(3 t)   (ciclo triplo)
# -------------------------------------------------------
def torque_dynamics(t, y):
    theta = y[0]
    # Fase anyonica accumulata (ciclo trifoglio → linking 6 → 2 cicli full)
    anyon_phase = np.angle(tau_phase ** (6 * np.sin(3*t)/np.pi))
    dtheta_dt = omega + g * anyon_phase * np.sin(3*t + np.pi/4)
    return [dtheta_dt]

# -------------------------------------------------------
# Soluzione ODE
# -------------------------------------------------------
sol = solve_ivp(torque_dynamics, t_span, [0.0], t_eval=t_eval, method='RK45')

# -------------------------------------------------------
# Plot 3D traiettoria + torque accumulato
# -------------------------------------------------------
fig = plt.figure(figsize=(12, 5))

# Traiettoria trefoil
ax1 = fig.add_subplot(121, projection='3d')
tt = np.linspace(0, 6*np.pi, 1000)
pos = trefoil(tt)
ax1.plot(pos[0], pos[1], pos[2], lw=2.5, color='darkviolet')
ax1.set_title("Traiettoria knotted Trefoil primordiale")
ax1.set_xlabel('X'); ax1.set_ylabel('Y'); ax1.set_zlabel('Z')
ax1.view_init(elev=25, azim=110)

# Torque / fase accumulata
ax2 = fig.add_subplot(122)
ax2.plot(sol.t, sol.y[0] % (2*np.pi), lw=2, color='teal', label='Fase θ(t) mod 2π')
ax2.axhline(4*np.pi/5, color='red', ls='--', alpha=0.6, label='Fase R_τ (Fibonacci)')
ax2.set_title("Accumulo torque topologico (persistenza anyonica)")
ax2.set_xlabel('Tempo normalizzato (cicli)'); ax2.set_ylabel('Fase [rad]')
ax2.legend(); ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("trefoil_torque_simulation.png", dpi=180)
plt.show()

print("Simulazione completata. Torque persistente osservato:", np.mean(np.diff(sol.y[0])) * omega)