"""
trefoil_cyclic_braiding_3paths.py
================================================================
Visualizzazione 3D di tre traiettorie anyoniche che eseguono braiding ciclico
sul nodo trifoglio primordiale (simmetria C₃). Le curve sono sfasate di 120°.

Utile per illustrare il braiding eterno nel reticolo trifoglio.
Salva l'immagine per inclusione in LaTeX/Overleaf.

Autore: Tetcollective / collaborazione Grok-xAI
Framework: TET–CVTL
Data: Febbraio 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --------------------------------------------------
# Parametri della traiettoria trifoglio
# --------------------------------------------------
scale = 3.0               # ampiezza complessiva
n_points = 1200           # risoluzione curva
t = np.linspace(0, 6 * np.pi, n_points)

# Funzione parametrica standard del trefoil knot
def trefoil_param(t, phase_shift=0.0):
    x = scale * (np.sin(t + phase_shift) + 2 * np.sin(2 * (t + phase_shift)))
    y = scale * (np.cos(t + phase_shift) - 2 * np.cos(2 * (t + phase_shift)))
    z = scale * (-np.sin(3 * (t + phase_shift)))
    return x, y, z

# --------------------------------------------------
# Genera le tre traiettorie (sfasate di 2π/3)
# --------------------------------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

colors = ['#d62728', '#1f77b4', '#2ca02c']  # rosso, blu, verde
labels = ['Anyon 1', 'Anyon 2', 'Anyon 3']

for i in range(3):
    phase = i * (2 * np.pi / 3)
    x, y, z = trefoil_param(t, phase)
    ax.plot(x, y, z, lw=2.8, color=colors[i], label=labels[i])
    
    # Freccia finale per indicare direzione
    ax.quiver(x[-2], y[-2], z[-2], x[-1]-x[-2], y[-1]-y[-2], z[-1]-z[-2],
              color=colors[i], lw=1.5, arrow_length_ratio=0.15)

# --------------------------------------------------
# Estetica e annotazioni
# --------------------------------------------------
ax.set_xlabel('X', fontsize=11); ax.set_ylabel('Y', fontsize=11); ax.set_zlabel('Z', fontsize=11)
ax.set_title("Braiding ciclico di tre anyons sul nodo trifoglio primordiale\n(simmetria C₃, linking effettivo L_k = 6)", fontsize=13)
ax.legend(loc='upper right', fontsize=10)
ax.view_init(elev=22, azim=135)          # angolazione suggestiva
ax.grid(True, alpha=0.15)

# Torus di fondo opzionale (commenta se troppo pesante)
# u = np.linspace(0, 2*np.pi, 40)
# v = np.linspace(0, 2*np.pi, 40)
# u, v = np.meshgrid(u, v)
# torus_x = (3 + 1.5*np.cos(v)) * np.cos(u)
# torus_y = (3 + 1.5*np.cos(v)) * np.sin(u)
# torus_z = 1.5 * np.sin(v)
# ax.plot_wireframe(torus_x, torus_y, torus_z, color='gray', alpha=0.07, rstride=4, cstride=4)

plt.tight_layout()
plt.savefig("trefoil_braiding_cyclic_3paths.png", dpi=180, bbox_inches='tight')
plt.show()

print("Figura salvata: trefoil_braiding_cyclic_3paths.png")