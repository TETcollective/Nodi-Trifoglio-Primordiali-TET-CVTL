"""
phase_accumulation_vs_Lk.py
Plot fase accumulata vs linking number (Lk) per nodo trifoglio primordiale
Mostra fase totale, residuo mod 2π, sin(ΔΦ) e sin²(ΔΦ) per asimmetria chirale
Autore: Tetcollective collab
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# Imposta stile LaTeX-like per il paper
plt.rcParams.update({
    "text.usetex": False, # Changed from True to False to fix LaTeX error
    "font.family": "serif",
    # "font.serif": ["Computer Modern Roman"], # Removed as it's LaTeX-specific and usetex is False
    "font.size": 12,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# Dati dalla tabella (estesi per Lk multipli)
lk_values = np.array([0, 3, 6, 9, 12, 15, 18])  # Lk effettivi (multipli di 3 per trifoglio-like)
phase_per_crossing = 4 * np.pi / 5  # fase dominante per crossing
num_crossings = lk_values / 3  # Lk=6 → 2 cicli completi, ecc.

phase_total = num_crossings * phase_per_crossing
phase_residue = phase_total % (2 * np.pi)
sin_delta = np.sin(phase_residue)
sin2_delta = sin_delta**2

# Plot
fig, ax1 = plt.subplots(figsize=(9, 6))

# Asse sinistro: fase totale e residuo
ax1.plot(lk_values, phase_total / np.pi, 'o-', color='darkblue', linewidth=2, label='Fase totale / π')
ax1.plot(lk_values, phase_residue / np.pi, 's--', color='royalblue', linewidth=1.5, label='Residuo mod 2π / π')
ax1.set_xlabel('Linking number Lk') # Removed $ around L_k
ax1.set_ylabel('Fase (π units)') # Replaced LaTeX with Unicode
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(loc='upper left')
ax1.set_title('Fase accumulata vs Linking number (braiding trifoglio primordiale)\nFase per crossing dominante: 4π/5') # Replaced LaTeX with Unicode

# Asse destro: sin(ΔΦ) e sin²(ΔΦ) (asimmetria chirale per torque)
ax2 = ax1.twinx()
ax2.plot(lk_values, sin_delta, 'd-', color='darkred', linewidth=2, label='sin(ΔΦ)') # Replaced LaTeX with Unicode
ax2.plot(lk_values, sin2_delta, 'v--', color='firebrick', linewidth=1.5, label='sin²(ΔΦ)') # Replaced LaTeX with Unicode
ax2.set_ylabel('sin(ΔΦ) e sin²(ΔΦ)') # Replaced LaTeX with Unicode
ax2.legend(loc='upper right')
ax2.set_ylim(0, 1.05)

# Annotazioni chiave
ax1.annotate('Lk=6 (torque netto massimo)', xy=(6, 24*np.pi/5 / np.pi), xytext=(8, 4.5),
             arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)

plt.tight_layout()
plt.savefig('phase_accumulation_vs_Lk.png', dpi=300, bbox_inches='tight')
plt.show()

print("Plot salvato come 'phase_accumulation_vs_Lk.png'")

ax1.set_title('Fase accumulata vs Linking number (braiding trifoglio primordiale)\n' + # Replaced LaTeX with Unicode
               'Fase per crossing dominante: 4π/5') # Replaced LaTeX with Unicode

ax1.annotate('Lk=6 (torque netto massimo)', # Removed $ around L_k
             xy=(6, 24*np.pi/5 / np.pi),
             xytext=(8, 4.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=11, fontweight='bold')

ax2.set_ylabel('sin(ΔΦ) e sin²(ΔΦ)', fontsize=12) # Replaced LaTeX with Unicode

plt.savefig('phase_accumulation_vs_Lk.png', dpi=400, bbox_inches='tight')