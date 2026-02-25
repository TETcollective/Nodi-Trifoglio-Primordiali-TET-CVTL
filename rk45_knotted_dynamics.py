"""
rk45_knotted_dynamics.py
================================================================
Simulazione della dinamica di fase θ(t) con torque topologico persistente
generato da braiding ciclico anyonico sul nodo trifoglio primordiale.
Utilizza scipy.integrate.solve_ivp con metodo RK45 (adattivo).

Autore: Tetcollective / collaborazione Grok-xAI
Framework: TET–CVTL
Data: Febbraio 2026
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --------------------------------------------------
# Parametri fisici / toy-model (scalabili)
# --------------------------------------------------
omega_base   = 2 * np.pi * 1.2e9       # rad/s   (es. ordine GHz, shift Larmor-like)
g_coupling   = 0.85                    # adimensionale (coupling anyon-vacuum)
phi_offset   = np.pi / 4               # fase di offset del drive trifoglio

# Fase anyonica di riferimento (modello Fibonacci-like)
R_tau_phase  = np.exp(-1j * 3 * np.pi / 5)   # ≈ e^{-i 108°} ≈ -0.309 - 0.951i

# Intervallo temporale (normalizzato per multipli di cicli trifoglio)
t_span = (0, 80.0)
t_eval = np.linspace(t_span[0], t_span[1], 4000)

# --------------------------------------------------
# Driver del torque topologico persistente
# --------------------------------------------------
def theta_dot(t, y):
    """
    Equazione: dθ/dt = ω + g · arg(R^{6 sin(3t)/π}) · sin(3t + φ₀)
    Il termine 6 deriva dal linking number Lk=6 del trefoil.
    """
    theta = y[0]
    exponent = 6 * np.sin(3 * t) / np.pi          # modulazione ciclica
    anyon_factor = np.angle(R_tau_phase ** exponent)
    drive = g_coupling * anyon_factor * np.sin(3 * t + phi_offset)
    return [omega_base + drive]

# --------------------------------------------------
# Integrazione adattiva RK45
# --------------------------------------------------
sol = solve_ivp(theta_dot, t_span, [0.0], method='RK45',
                t_eval=t_eval, rtol=1e-9, atol=1e-12)

# --------------------------------------------------
# Plot di verifica
# --------------------------------------------------
plt.figure(figsize=(11, 4.5))
plt.plot(sol.t, sol.y[0] % (2 * np.pi), lw=1.5, color='teal', label=r'$	heta(t) \operatorname{mod} 2\pi$')
plt.axhline(4 * np.pi / 5, color='red', ls='--', alpha=0.6, label=r'Fase $4\pi/5$ (ref. R-matrix)')
plt.axhline(-3 * np.pi / 5, color='orange', ls=':', alpha=0.5, label=r'Fase $-3\pi/5$ (ref.)')

plt.title("Accumulo persistente di fase/torque topologico – Braiding trifoglio eterno")
plt.xlabel("Tempo normalizzato (unità arbitrarie)")
plt.ylabel("Fase θ(t) [rad]")
plt.grid(True, alpha=0.25)
plt.legend(loc='upper right', fontsize=9)
plt.tight_layout()

# Salva per Overleaf
plt.savefig("rk45_phase_accumulation.png", dpi=180, bbox_inches='tight')
plt.show()

# --------------------------------------------------
# Risultati riassuntivi
# --------------------------------------------------
drift_mean = np.mean(np.diff(sol.y[0][2000:])) / np.mean(np.diff(sol.t[2000:]))
print(f"Drift medio osservato (seconda metà): {drift_mean:.4e} rad/s")
print(f"Fase finale mod 2π: {sol.y[0][-1] % (2*np.pi):.4f} rad")