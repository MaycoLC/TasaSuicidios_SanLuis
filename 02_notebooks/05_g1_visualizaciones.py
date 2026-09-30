# === G1: RANKING PROVINCIAL 2024 === 

import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches

df = pd.read_csv('01_datos/procesados/analisis_completo.csv')
df = df[df['provincia'] != 'Total País'].sort_values('tasa_2024')

tasa_nac = 9.8 # Promedio Nacional 2024

# Colores: 
# Rojo oscuro si supera el promedio. Azul si está por debajo.
colores = ['#B7310E' if t > tasa_nac else '#2E6DA4' for t in df['tasa_2024']]

# Resaltar San Luis
colores = ['#E07020' if p == 'San Luis' else c 
           for p, c in zip(df['provincia'], colores)]

fig, ax = plt.subplots(figsize=(10,10))
bars = ax.barh(df['provincia'], df['tasa_2024'], color=colores, edgecolor='white', height=0.7)

for bar, val in zip(bars, df['tasa_2024']):
    ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
    f'{val:.1f}', va='center', fontsize=9)

# Línea de Referencia Nacional
ax.axvline(x=tasa_nac, color='black', linestyle='--', linewidth=1.2, alpha=0.6)
ax.text(tasa_nac + 0.2, 0, f'Promedio\nNacional\n{tasa_nac}', fontsize=8, va='bottom')

ax.set_title('Tasa de Suicidios por Provincia - Argentina 2024\n(cada 100.000 habitantes)')
ax.set_xlabel('Tasa cada 100.000 hab.', fontsize=10)
ax.set_xlim(0, 24)
ax.grid(axis='x', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Leyenda

ley = [mpatches.Patch(color='#B7410E', label='Sobre el Promedio Nacional'),
       mpatches.Patch(color='#E07020', label='San Luis'),
       mpatches.Patch(color='#2E6DA4', label='Bajo el Promedio Nacional')]
ax.legend(handles=ley, fontsize=9, loc='lower right')

plt.tight_layout()
plt.savefig('04_outputs/G1_ranking_provincial.png', dpi=150, bbox_inches='tight')
plt.show()