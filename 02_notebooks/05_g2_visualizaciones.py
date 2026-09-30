# === G2: EVOLUCIÓN TEMPORAL 2022-2024 (Top 8 Provincias) === 

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('01_datos/procesados/tasas_nacionales_largo.csv')

# Selección de las 8 provincias con mayor tasa en 2024 + total país.
df_24 = pd.read_csv('01_datos/procesados/analisis_completo.csv')
top8 = (df_24[df_24['provincia'] != 'Total País']
        .nlargest(8, 'tasa_2024')['provincia'].tolist())

# ── Paleta con jerarquía visual ──────────────────────────────────────────────
# San Luis y Entre Ríos destacados.
colores_fijos = {
    'San Luis':    '#E07020',   # naranja — protagonista del análisis
    'Entre Ríos':  '#8B0000',   # rojo oscuro — tasa más alta del país
}

# Paleta para las otras 6: colores distinguibles pero sin competir con los destacados.
paleta_resto = [
    '#2E6DA4',   # azul medio
    '#1D9E75',   # verde
    '#7B57D4',   # violeta
    '#5B9FD4',   # azul claro
    '#B8860B',   # dorado oscuro
    '#888888',   # gris
]

fig, ax = plt.subplots(figsize=(12, 6))

# Línea Total Nacional (punteada)
df_nac = df_24[df_24['provincia'] == 'Total País']
años = [2022, 2023, 2024]
tasas_nac = [df_nac['tasa_2022'].values[0], 
             df_nac['tasa_2023'].values[0], 
             df_nac['tasa_2024'].values[0]]
ax.plot(años, tasas_nac, 'k--', linewidth=2, label='Total País', zorder=5)

# Líneas por Provincia
idx_resto = 0
for prov in top8:
    sub = df[df['provincia'] == prov].sort_values('año')

    if prov in colores_fijos:
        color = colores_fijos[prov]
        lw    = 2.8
        ms    = 7
        zord  = 4
    else:
        color = paleta_resto[idx_resto]
        idx_resto += 1
        lw    = 1.5
        ms    = 5
        zord  = 3

    ax.plot(sub['año'], sub['tasa'],
            marker='o', markersize=ms,
            linewidth=lw, label=prov,
            color=color, zorder=zord)

# ── Anotaciones directas al final de cada línea (para evita buscar en la leyenda) ─
for prov in top8:
    sub = df[df['provincia'] == prov].sort_values('año')
    ultimo_año  = sub['año'].max()
    ultima_tasa = sub.loc[sub['año'] == ultimo_año, 'tasa'].values[0]
    color = colores_fijos.get(prov, 'gray')
    ax.annotate(prov,
                xy=(ultimo_año, ultima_tasa),
                xytext=(5, 0), textcoords='offset points',
                fontsize=8, color=color,
                va='center')

# Anotación Total País
ax.annotate('Total País',
            xy=(2024, tasas_nac[-1]),
            xytext=(5, 0), textcoords='offset points',
            fontsize=8, color='black', va='center')

ax.set_title('Evolución de la Tasa de Suicidios - Top 8 Provincias y Total País 2022-2024',
             fontsize=12, fontweight='bold', pad=15)

ax.set_xlabel('Año', fontsize=10)
ax.set_ylabel('Tasa c/100.000 Habitantes', fontsize=10)
ax.set_xticks([2022, 2023, 2024])
ax.set_xlim(2021.9, 2024.6)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Leyenda solo para los destacados + Total País (más limpia)
handles, labels = ax.get_legend_handles_labels()
orden = ['Total País', 'San Luis', 'Entre Ríos']
h_filtrados = [(h, l) for h, l in zip(handles, labels) if l in orden]
ax.legend([h for h,l in h_filtrados], [l for h,l in h_filtrados],
          fontsize=9, loc='upper left',
          framealpha=0.9, edgecolor='#CCCCCC')

plt.tight_layout()
plt.savefig('04_outputs/G2_evolucion_top8.png', dpi=150, bbox_inches='tight')
plt.show()