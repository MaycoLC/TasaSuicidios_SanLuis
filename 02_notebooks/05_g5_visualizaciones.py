# === G5: CASOS por FRANJA HORARIA en SAN LUIS ===

import pandas as pd
import matplotlib.pyplot as plt

sl = pd.read_csv('01_datos/procesados/sl_horario.csv')

franjas = sl['franja_horaria']
casos = sl['casos']
porcentajes = sl['porcentaje']

# Destacar la franja con más casos.
indice_pico = casos.idxmax()
colores = [
    '#E07020' if indice == indice_pico else '#2E6DA4'
    for indice in sl.index
]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(franjas, casos, color=colores, edgecolor='white', width=0.7)

for barra, cantidad, porcentaje in zip(bars, casos, porcentajes):
    ax.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height() + 1,
        f'{cantidad} ({porcentaje:.1f}%)',
        ha='center',
        va='bottom',
        fontsize=9,
    )

ax.set_title(
    'CASOS de SUICIDIO por FRANJA HORARIA · San Luis 2017–2022',
    fontsize=12,
    fontweight='bold',
    pad=15,
)
ax.set_xlabel('Franja Horaria', fontsize=10, fontweight='bold')
ax.set_ylabel('Casos', fontsize=10, fontweight='bold')
ax.set_ylim(0, casos.max() * 1.2)
ax.grid(axis='y', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('04_outputs/G5_horario_casos.png', dpi=150, bbox_inches='tight')
plt.show()
