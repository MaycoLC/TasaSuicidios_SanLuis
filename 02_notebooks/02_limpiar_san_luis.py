# Finalidad del Script

# Construye los datasets de San Luis directamente en Pyhton a partir de los datos
# extraídos del informe oficial de la Dirección de Estadística y Censos de San Luis.

# Fuente: "Cantidad de suicidios consumados. Años 2917-2022"
# Datos originales: https://datos.gob.ar/ar/dataset/seguridad-suicidios-sistema-alerta-temprana-estadisticas-criminales-republica-argentina

import pandas as pd
import os

# ====================================================================
# Tabla 1 - Casos totales por año en San Luis (Tabla N° 5 del informe)
# ====================================================================
print("\nConstruyendo: casos_anuales_san_luis.csv")

casos_anuales = pd.DataFrame({
    'mes': ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
            'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
    'num_mes': list(range(1, 13)),
    '2017': [4,1,2,3,4,2,3,5,4,3,4,3],
    '2018': [3,2,0,5,1,7,2,7,9,7,5,4],
    '2019': [6,7,7,9,4,2,6,4,4,10,6,10],
    '2020': [7,5,7,9,2,4,6,2,2,5,6,7],
    '2021': [4,7,6,5,6,4,10,5,8,2,4,5],
    '2022': [4,7,2,6,3,3,6,6,4,5,4,5],
})

# Formato largo
largo = pd.melt(
    casos_anuales,
    id_vars=['mes', 'num_mes'],
    value_vars=['2017','2018','2019','2020','2021','2022'],
    var_name='año',
    value_name='casos'
)

largo['año'] = largo['año'].astype(int)
largo = largo.sort_values(['año', 'num_mes']).reset_index(drop=True)

largo.to_csv('01_datos/procesados/sl_casos_mensuales.csv', index=False, encoding='utf-8')
print(f" -> {len(largo)} filas | Total 2018-2022: {largo['casos'].sum()} casos")

# ====================================================================
# Tabla 2 - Casos por departamento (Gráfico 13 del informe)
# ====================================================================
print("\nConstruyendo: sl_por_departamento.csv")

departamentos = pd.DataFrame({
    'departamento': [
        'Ayacucho', 'Belgrano', 'Chacabuco', 'Coronel Pringles',
        'General Pedernera', 'Gobernador Dupuy', 'Junín',
        'Juan Martín de Pueyrredón',  # "La Capital" en el informe
        'Libertador General San Martín'
    ],
    'casos_2017_2022': [20, 5, 24, 15, 90, 8, 29, 152, 5],
})
departamentos['porcentaje'] = (
    departamentos['casos_2017_2022'] / departamentos['casos_2017_2022'].sum() * 100
).round(1)

departamentos = departamentos.sort_values('casos_2017_2022', ascending=False).reset_index(drop=True)

departamentos.to_csv('01_datos/procesados/sl_por_departamento.csv', index=False, encoding='utf-8')
print(f" -> {len(departamentos)} departamentos | Total: {departamentos['casos_2017_2022'].sum()} casos")
print(f"  → Juan Martín de Pueyrredón: {departamentos.loc[departamentos['departamento']=='Juan Martín de Pueyrredón','porcentaje'].values[0]}% del total")

# =========================================================================
# Tabla 3 - Casos por grupo etario y sexo en San Luis (Tabla 3 del informe)
# =========================================================================
print("\nConstruyendo: sl_edad_sexo_anual.csv")

grupos = ['10-14','15-19','20-24','25-29','30-34','35-39',
          '40-44','45-49','50-54','55-59','60-64','65-69',
          '70-74','75-79','80 y más']

# Datos de Tabla 3 del informe: femenino y masculino por año y grupo etario
# Formato: fila = grupo etario, col= año_sexo

datos_edad = {
    'grupo_etario': grupos,
    # 2017
    'f_2017': [0,1,1,1,1,0,0,1,0,3,0,0,1,0,0],
    'm_2017': [0,1,5,7,4,2,2,1,3,0,1,1,1,1,0],
    # 2018
    'f_2018': [0,1,1,1,0,1,0,1,0,0,0,1,0,0,0],
    'm_2018': [0,1,8,7,7,3,3,3,3,4,1,1,3,0,2],
    # 2019
    'f_2019': [1,1,2,1,2,0,3,0,1,1,1,0,0,1,0],
    'm_2019': [0,11,11,6,7,5,3,4,2,4,3,3,2,0,0],
    # 2020
    'f_2020': [1,3,1,0,0,2,3,2,0,1,0,0,0,0,2],
    'm_2020': [0,5,6,2,3,5,3,2,5,1,2,3,3,5,2],
    # 2021
    'f_2021': [0,2,3,4,0,1,2,2,0,1,1,0,1,0,1],
    'm_2021': [1,1,8,9,6,2,4,3,2,2,1,3,4,1,1],
    # 2022
    'f_2022': [2,4,1,2,0,0,0,0,0,2,0,1,0,0,0],
    'm_2022': [0,6,6,6,5,1,6,1,1,2,4,4,0,1,0],
}

df_edad = pd.DataFrame(datos_edad)

# Convertir a formato largo
registros = []

for _, row in df_edad.iterrows():
    grupo = row['grupo_etario']
    for año in [2017, 2018, 2019, 2020, 2021, 2022]:
        registros.append({
            'grupo_etario': grupo,
            'año': año,
            'sexo': 'Femenino',
            'casos': row[f'f_{año}']        
        })
        registros.append({
            'grupo_etario': grupo,
            'año': año,
            'sexo': 'Masculino',
            'casos': row[f'm_{año}']
        })

df_largo = pd.DataFrame(registros)
df_largo.to_csv('01_datos/procesados/sl_edad_sexo_anual.csv', index=False, encoding='utf-8')

# Totales para verificar

total_f = df_largo[df_largo['sexo']=='Femenino']['casos'].sum()
total_m = df_largo[df_largo['sexo']=='Masculino']['casos'].sum()
print(f" -> Total Femenino: {total_f} | Total Masculino: {total_m} | Total Final: {total_f + total_m}")
print(f' -> Proporción masculino: {total_m/(total_f + total_m)*100:.1f}%')

# ============================================================
# Tabla 4 - Localidad de Zanjitas (Juan Martín de Pueyrredón)
# ============================================================
print("\nConstruyendo: sl_zanjitas.csv")

zanjitas_anuales = pd.DataFrame({
    'año': [2017, 2018, 2019, 2020, 2021, 2022],
    'femenino': [4, 4, 6, 7, 4, 2],
    'masculino': [13,19,21,13,17,12],
})
zanjitas_anuales['total'] = zanjitas_anuales['femenino'] + zanjitas_anuales['masculino']
zanjitas_anuales['localidad'] = 'Zanjitas'
zanjitas_anuales['departamento'] = 'Juan Martín de Pueyrredón'

zanjitas_anuales.to_csv('01_datos/procesados/sl_zanjitas.csv', index=False, encoding='utf-8')
print(f" -> Total 2017-2022: {zanjitas_anuales['total'].sum()} casos")
print(f"  → Pico: {zanjitas_anuales.loc[zanjitas_anuales['total'].idxmax(), 'año']} ({zanjitas_anuales['total'].max()} casos)")

# ======================================
# Tabla 5 - Localidad de Villa Mercedes 
# ======================================
print("\nConstruyendo: sl_villa_mercedes.csv")

vm_anuales = pd.DataFrame({
    'año': [2017, 2018, 2019, 2020, 2021, 2022],
    'femenino': [1, 0, 3, 0, 4, 5],
    'masculino': [10,12,16,16,9,10],
})

vm_anuales['total'] = vm_anuales['femenino'] + vm_anuales['masculino']
vm_anuales['localidad'] = 'Villa Mercedes'
vm_anuales['departamento'] = 'General Pedernera'

vm_anuales.to_csv('01_datos/procesados/sl_villa_mercedes.csv', index=False, encoding='utf-8')
print(f" -> Total 2017-2022: {vm_anuales['total'].sum()} casos")

# ==================================================
# Tabla 6 - Lugar del hecho (Gráfico 11 del infrome) 
# ==================================================
print("\nConstruyendo: sl_lugar_hecho.csv")

lugar_hecho = pd.DataFrame({
    'lugar': [
        'Domicilio particular', 'Vía pública', 'Cárcel/comisaría',
        'Campo/descampado/zona rural', 'Río/dique', 'Otro lugar',
        'Hotel/hospedaje', 'Establecimiento comercial', 'Vías del FFCC'
    ],
    'casos': [265, 66, 8, 2, 2, 2, 1, 1, 1],
})

lugar_hecho['porcentaje'] = (lugar_hecho['casos'] / lugar_hecho['casos'].sum() * 100).round(1)
lugar_hecho = lugar_hecho.sort_values('casos', ascending=False).reset_index(drop=True)

lugar_hecho.to_csv('01_datos/procesados/sl_lugar_hecho.csv', index=False, encoding='utf-8')
print(f" -> {lugar_hecho.iloc[0]['lugar']}: {lugar_hecho.iloc[0]['porcentaje']}% de los casos")

# ========================================================
# Tabla 7 - Horario de ocurrencia (Gráfico 12 del infrome) 
# ========================================================
print("\nConstruyendo: sl_horario.csv")

horario = pd.DataFrame({
    'franja_horaria': [
        '00:00-01:00', '01:00-03:00', '04:00-06:00', '07:00-09:00',
        '10:00-12:00', '13:00-15:00', '16:00-18:00', '19:00-21:00', '22:00-24:00'
    ],
    'casos': [7,17,25,56,58,48,49,68,20],
})

horario['porcentaje'] = (horario['casos'] / horario['casos'].sum() * 100).round(1)
horario.to_csv('01_datos/procesados/sl_horario.csv', index=False, encoding='utf-8')
pico = horario.loc[horario['casos'].idxmax()]
print(f"  → Pico horario: {pico['franja_horaria']} ({pico['casos']} casos, {pico['porcentaje']}%)")

# ══════════════════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("RESUMEN — Archivos generados en 01_datos/procesados/:")
archivos = [
    ('sl_casos_mensuales.csv',   'Casos por mes y año 2017-2022'),
    ('sl_por_departamento.csv',  'Casos totales por departamento'),
    ('sl_edad_sexo_anual.csv',   'Casos por grupo etario, sexo y año'),
    ('sl_zanjitas.csv',          'Casos en Zanjitas por año y sexo'),
    ('sl_villa_mercedes.csv',    'Casos en Villa Mercedes por año y sexo'),
    ('sl_lugar_hecho.csv',       'Distribución por lugar del hecho'),
    ('sl_horario.csv',           'Distribución por franja horaria'),
]
for fname, desc in archivos:
    print(f"  ✓ {fname:<35} — {desc}")
 
print("\nHALLAZGOS CLAVE del informe:")
print(f"  • Total provincial 2017-2022: 348 casos")
print(f"  • Juan Martín de Pueyrredón: 152 casos (43.7% del total)")
print(f"  • General Pedernera: 90 casos (25.9% del total)")
print(f"  • Ambos departamentos: 69.5% del total provincial")
print(f"  • Proporción masculino: ~80% de los casos")
print(f"  • Grupo más afectado: 15-34 años (varones)")
print(f"  • Lugar más frecuente: domicilio particular (76.4%)")
print(f"  • Horario pico: 19:00-21:00 (68 casos)")
print(f"  • Año con más casos: 2019 (75 casos)")
print(f"  • Modalidad dominante: ahorcamiento")