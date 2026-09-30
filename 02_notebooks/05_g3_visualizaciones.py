# === G3: CASOS en SAN LUIS por DEPARTAMENTO 2017-2022 ===

import pandas as pd
import matplotlib.pyplot as plt

sl = pd.read_csv('01_datos/procesados/sl_por_departamento.csv')

# Totales por Departamento
por_depto = sl.groupby('departamento')['casos_2017_2022'].sum().sort_values()

# Color: destacando Pueyrredón y Pedernera
colores = ['#B7410E' if d in ['Juan Martín de Pueyrredón', 'General Pedernera'] 
           else '#2E6DA4' for d in por_depto.index]

fig, ax = plt.subplots(figsize=(10,6))
bars = ax.barh(por_depto.index, por_depto.values, color=colores, edgecolor='white', height=0.7)

for bar, val in zip(bars, por_depto.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            str(int(val)), va='center', fontsize=10, fontweight='bold')

ax.set_title('Suicidios por Departamento - San Luis 2017-2022\n(Total de casos acumulados)',
             fontsize=12, fontweight='bold', pad=15)

ax.set_xlabel('Casos acumulados 2017-2022', fontsize=12)
ax.grid(axis='x', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Nota de Limitación

ax.text(0.01, -0.12,
        'Nota: Datos disponibles solo hasta 2022. Fuente: Dir. Estadística y Censos de San Luis.',
        transform=ax.transAxes, fontsize=8, color='gray', style='italic')

plt.tight_layout()
plt.savefig('04_outputs/G3_sanluis_por_departamento.png', dpi=150, bbox_inches='tight')
plt.show()