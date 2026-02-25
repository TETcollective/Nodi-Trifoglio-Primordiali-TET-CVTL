"""
phase_accumulation_vs_Lk_futuristic.py
Plot futuristico: Fase accumulata vs Linking number Lk
con curva teorica sin²(ΔΦ) - stile cyber-scientifico neon
Autore: Tetcollective / Grok-xAI collab
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ====================== STILE FUTURISTICO ======================
rcParams.update({
    'figure.figsize': (11, 6.5),
    'figure.dpi': 300,
    'axes.facecolor': '#0a0a1f',
    'figure.facecolor': '#05050f',
    'text.color': '#ffffff',
    'axes.labelcolor': '#00ffff',
    'xtick.color': '#00ffff',
    'ytick.color': '#00ffff',
    'grid.color': '#00ffff',
    'grid.alpha': 0.15,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 13,
    'legend.fontsize': 11,
    'lines.linewidth': 2.5,
})

# ====================== DATI ======================
lk_values = np.array([0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30])
phase_per_crossing = 4 * np.pi / 5
num_crossings = lk_values / 3.0

phase_total = num_crossings * phase_per_crossing
phase_residue = phase_total % (2 * np.pi)
sin_delta = np.sin(phase_residue)
sin2_delta = sin_delta ** 2

# Curva teorica continua (sin²(ΔΦ) periodica)
lk_theory = np.linspace(0, 30, 500)
phase_theory = (lk_theory / 3.0) * phase_per_crossing
res_theory = phase_theory % (2 * np.pi)
sin2_theory = np.sin(res_theory) ** 2

# ====================== PLOT ======================
fig, ax1 = plt.subplots()

# Asse sinistro - Fase totale e residuo
ax1.plot(lk_values, phase_total / np.pi, 'o-', color='#00ffff', label=r'Fase totale / $\pi$')
ax1.plot(lk_values, phase_residue / np.pi, 's--', color='#00ffcc', label=r'Residuo mod $2\pi$ / $\pi$')
ax1.set_xlabel('Linking number $L_k$', color='white')
ax1.set_ylabel(r'Fase ($\pi$ units)', color='#00ffff')
ax1.tick_params(colors='white')
ax1.grid(True, linestyle='--', alpha=0.25)

# Asse destro - sin(ΔΦ) e sin²(ΔΦ)
ax2 = ax1.twinx()
ax2.plot(lk_values, sin_delta, 'd-', color='#ff00ff', label=r'$\sin(\Delta\Phi)$')
ax2.plot(lk_values, sin2_delta, 'v--', color='#ff66ff', label=r'$\sin^2(\Delta\Phi)$')
ax2.plot(lk_theory, sin2_theory, '-', color='#ff99ff', alpha=0.6, linewidth=1.8, label=r'$\sin^2(\Delta\Phi)$ teorica')
ax2.set_ylabel(r'$\sin(\Delta\Phi)$ e $\sin^2(\Delta\Phi)$', color='#ff00ff')
ax2.tick_params(colors='#ff00ff')

# Titolo e annotazione Lk=6 (torque massimo)
ax1.set_title('Fase Accumulata vs Linking Number\nBraiding Trifoglio Primordiale', 
              color='white', pad=20, fontsize=16)
ax1.annotate(r'$L_k=6$ (torque netto massimo)', 
             xy=(6, 24*np.pi/5 / np.pi), 
             xytext=(9.5, 4.8),
             arrowprops=dict(facecolor='#ffff00', edgecolor='#ffff00', shrink=0.05, width=2, headwidth=9),
             fontsize=12, fontweight='bold', color='#ffff00', ha='left')

# Legenda combinata
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, 
           facecolor='#1a1a2e', edgecolor='#00ffff')

plt.tight_layout()
plt.savefig('phase_accumulation_vs_Lk_futuristic.png', dpi=400, bbox_inches='tight', facecolor='#05050f')
plt.show()

print("✅ Plot futuristico salvato come 'phase_accumulation_vs_Lk_futuristic.png'")
print("   Risoluzione 400 dpi - pronto per Overleaf")