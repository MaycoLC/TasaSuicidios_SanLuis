import pandas as pd

# --- Dataset construido manualmente desde la Tabla 4 del Informe SNIC 2024. ---
# Fuente: cloud-snic.minseg.gob.ar/Informes/SAT/SAT_SS/Informe_Suicidios_2024.pdf

datos = {
    'provincia': ['Buenos Aires', 'Catamarca', 'Chaco', 'Chubut', 'CABA',
        'Córdoba', 'Corrientes', 'Entre Ríos', 'Formosa', 'Jujuy',
        'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquén',
        'Río Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz',
        'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucumán'
    ],

    # Valores absolutos.
    'casos_2022':
    [1206,51,137,61,242,253,60,239,78,50,56,52,219,99,53,42,209,76,55,44,371,128,22,156],
    'casos_2023': 
    [1399,56,153,52,184,289,78,247,78,61,43,54,207,82,62,46,184,76,79,38,382,130,20,205],
    'casos_2024': 
    [1267,60,111,65,171,366,80,263,93,75,46,59,239,78,61,37,179,92,86,38,460,106,18,199],

    # Tasa cada 100.000 habitantes.
    'tasa_2022':  
    [7.3,13.1,12.3,10.4,8.4,7.1,5.8,18.4,14.0,6.9,16.6,14.0,11.7,8.5,8.5,5.9,15.8,10.4,11.5,12.6,11.2,14.1,13.2,9.8],
    'tasa_2023':  
    [8.4,14.3,13.6,8.7,6.4,8.1,7.4,18.8,13.8,8.4,12.6,14.4,11.0,6.9,9.8,6.4,13.7,10.3,16.3,10.6,11.4,14.2,11.7,12.8],
    'tasa_2024':  
    [7.5,15.2,9.7,10.7,5.9,10.1,7.6,19.8,16.4,10.2,13.4,15.5,12.5,6.5,9.5,5.1,13.2,12.3,17.5,10.3,13.6,11.4,10.3,12.3],
}

df = pd.DataFrame(datos)

# Agregamos total nacional como referencia. 
total = pd.DataFrame([{
    'provincia': 'Total País',
    'casos_2022': 3959, 'casos_2023': 4205, 'casos_2024': 4249,
    'tasa_2022': 9.3,   'tasa_2023': 9.8,   'tasa_2024': 9.8 
}])

df = pd.concat([df, total], ignore_index=True)

# Resultado
print(df.sort_values('tasa_2024', ascending=False).to_string())

# Guardar dataset
df.to_csv('01_datos/procesados/tasas_nacionales.csv', index=False, encoding='utf-8')
print('Guardado: tasas_nacionales.csv')
print(f'\nTotal filas: {len(df)}')

# Script adicional para Tableau | Conversión a formato largo
df_largo = pd.melt(
    df[df['provincia'] != 'Total Páis'],
    id_vars=['provincia'],
    value_vars=['tasa_2022', 'tasa_2023', 'tasa_2024'],
    var_name='año_col',
    value_name='tasa'
)

# Extraer año del nombre de la columna.
df_largo['año'] = df_largo['año_col'].str.extract(r'(\d{4})').astype(int)
df_largo = df_largo.drop(columns=['año_col'])
df_largo = df_largo.sort_values(['provincia', 'año']).reset_index(drop=False)

df_largo.to_csv('01_datos/procesados/tasas_nacionales_largo.csv', index=False)
print('Guardado: tasas_nacionales_largo.csv')

# Resultado
# print(df_largo.head(10))