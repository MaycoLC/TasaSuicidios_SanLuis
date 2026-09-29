import pandas as pd

df = pd.read_csv('01_datos/procesados/tasas_nacionales.csv')

# --- Ranking 2024 --- 
ranking = (df[df['provincia'] != 'Total País']
           .sort_values('tasa_2024', ascending=False)
           .reset_index(drop=True))

ranking.index += 1 # Comenzar ranking en 1.
print("==== Ranking 2024 ====")
print(ranking[['provincia','tasa_2024']].head(24))

# --- Variación Interanual 2022 -> 2024 ---
df['var_abs_22_24'] = df['tasa_2024'] - df['tasa_2022']
df['var_rel_22_24'] = ((df['tasa_2024'] - df['tasa_2022']) * 100).round(1)

# --- San Luis vs. Promedio Nacional ---
tasa_pais = df.loc[df['provincia']=='Total País', 'tasa_2024'].values[0]
tasa_sl = df.loc[df['provincia']=='San Luis', 'tasa_2024'].values[0]
print(f'\nSan Luis 2024: {tasa_sl} | Nacional: {tasa_pais}')
print(f'San Luis supera el promedio nacional en: {tasa_sl - tasa_pais:.1f} puntos.')

# --- Categoría por Nivel de Tasa ---
prom = tasa_pais
def categoria(tasa):
    if tasa >= prom * 1.5: return 'Muy Alta'
    if tasa >= prom: return 'Alta'
    if tasa >= prom * 0.7: return 'Media'
    return 'Baja'

df['categoria_2024'] = df['tasa_2024'].apply(categoria)
print('\nDistribución por categoría:')
print(df['categoria_2024'].value_counts())

# Guardar análisis completo.
df.to_csv('01_datos/procesados/analisis_completo.csv', index=False, encoding='utf-8')
print('\nGuardado: analisis_completo.csv')