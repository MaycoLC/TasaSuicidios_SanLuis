# === G4: PIRÁMIDE por EDAD y SEXO en SAN LUIS ===

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

sl = pd.read_csv('01_datos/procesados/sl_edad_sexo_anual.csv')

piramide = sl.groupby(['grupo_etario', 'sexo'])['casos'].sum().unstack(fill_value=0)

grupos = [
    '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
    '40-44', '45-49', '50-54', '55-59', '60-64', '65-69',
    '70-74', '75-79', '80 y más'
]
piramide = piramide.reindex(grupos, fill_value=0)

varones = piramide['Masculino'].values
mujeres = piramide['Femenino'].values

fig, ax = plt.subplots(figsize=(9, 6))
y = np.arange(len(grupos))

ax.barh(y, -varones, color='#1A3A5C', label='Masculino', height=0.7)
ax.barh(y, mujeres, color='#CE6B8A', label='Femenino', height=0.7)

ax.set_yticks(y)
ax.set_yticklabels(grupos, fontsize=10)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{abs(x):g}'))

ax.set_xlabel('Casos', fontsize=10)
ax.set_title(
    'Distribución por edad y sexo · Suicidios San Luis 2017–2022',
    fontsize=12, fontweight='bold', pad=15
)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.legend(fontsize=10)
ax.grid(axis='x', alpha=0.3)

ax.text(
    0.01, -0.12,
    'Nota: Datos hasta 2022. Fuente: Dir. Estadística y Censos San Luis.',
    transform=ax.transAxes, fontsize=8, color='gray', style='italic'
)

plt.tight_layout()
plt.savefig('04_outputs/G4_piramide_edad_sexo.png', dpi=150, bbox_inches='tight')
plt.show()