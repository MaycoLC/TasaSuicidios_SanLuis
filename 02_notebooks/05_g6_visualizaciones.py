# === G6: SUICIDIO | LUGAR de HECHO en SAN LUIS ===

import pandas as pd
import matplotlib.pyplot as plt

sl = pd.read_csv('01_datos/procesados/sl_lugar_hecho.csv')
sl = sl.sort_values('casos', ascending=True)

lugar_hecho = sl['lugar']
casos = sl['casos']
porcentajes = sl['porcentaje']

# Destacar el lugar de hecho con más casos.
indice_pico = casos.idxmax()
colores = [
    '#E07020' if indice == indice_pico else '#2E6DA4'
    for indice in sl.index
]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(lugar_hecho, casos, color=colores, edgecolor='white', height=0.7)

for barra, cantidad, porcentaje in zip(bars, casos, porcentajes):
    ax.text(
        barra.get_width() + 3,
        barra.get_y() + barra.get_height() / 2,
        f'{cantidad} ({porcentaje:.1f}%)',
        ha='left',
        va='center',
        fontsize=9,
    )

ax.set_title(
    'SUICIDIO | LUGAR de HECHO · San Luis 2017–2022',
    fontsize=12,
    fontweight='bold',
    pad=15,
)
ax.set_xlabel('Casos', fontsize=10, fontweight='bold')
ax.set_xlim(0, casos.max() * 1.35)
ax.grid(axis='x', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('04_outputs/G6_lugar_hecho.png', dpi=150, bbox_inches='tight')
plt.show()