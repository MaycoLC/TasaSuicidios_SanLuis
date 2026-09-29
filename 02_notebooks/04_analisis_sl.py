from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESADOS_DIR = ROOT_DIR / "01_datos" / "procesados"


def cargar_csv(nombre, columnas_requeridas):
    ruta = PROCESADOS_DIR / nombre
    datos = pd.read_csv(ruta, encoding="utf-8-sig")
    faltantes = set(columnas_requeridas) - set(datos.columns)
    if faltantes:
        raise ValueError(
            f"El archivo {ruta} no contiene las columnas requeridas: "
            f"{', '.join(sorted(faltantes))}"
        )
    return datos


departamentos = cargar_csv(
    "sl_por_departamento.csv",
    ["departamento", "casos_2017_2022"],
)
edad_sexo = cargar_csv(
    "sl_edad_sexo_anual.csv",
    ["grupo_etario", "año", "sexo", "casos"],
)

departamentos["casos_2017_2022"] = pd.to_numeric(
    departamentos["casos_2017_2022"], errors="raise"
)
edad_sexo["casos"] = pd.to_numeric(edad_sexo["casos"], errors="raise")
edad_sexo["año"] = pd.to_numeric(edad_sexo["año"], errors="raise")

if departamentos[["departamento", "casos_2017_2022"]].isna().any().any():
    raise ValueError("Hay valores faltantes en el resumen por departamento.")
if edad_sexo[["grupo_etario", "año", "sexo", "casos"]].isna().any().any():
    raise ValueError("Hay valores faltantes en el resumen por edad y sexo.")
if (departamentos["casos_2017_2022"] < 0).any() or (edad_sexo["casos"] < 0).any():
    raise ValueError("Los conteos de casos no pueden ser negativos.")
if departamentos["departamento"].duplicated().any():
    raise ValueError("El resumen por departamento contiene departamentos duplicados.")

total_departamentos = int(departamentos["casos_2017_2022"].sum())
total_edad_sexo = int(edad_sexo["casos"].sum())
if total_departamentos != total_edad_sexo:
    raise ValueError(
        "Los totales no coinciden entre los archivos de departamentos "
        f"({total_departamentos}) y edad-sexo ({total_edad_sexo})."
    )
if total_departamentos == 0:
    raise ValueError("No hay casos para analizar.")

periodo = f"{int(edad_sexo['año'].min())}-{int(edad_sexo['año'].max())}"

por_departamento = (
    departamentos[["departamento", "casos_2017_2022"]]
    .rename(columns={"casos_2017_2022": "casos"})
    .sort_values("casos", ascending=False)
    .reset_index(drop=True)
)
por_departamento["porcentaje"] = por_departamento["casos"] / total_departamentos * 100

por_sexo = (
    edad_sexo.groupby("sexo", as_index=False)["casos"]
    .sum()
    .sort_values("casos", ascending=False)
    .reset_index(drop=True)
)
por_sexo["porcentaje"] = por_sexo["casos"] / total_edad_sexo * 100

por_grupo_etario = (
    edad_sexo.groupby("grupo_etario", as_index=False)["casos"]
    .sum()
    .sort_values("casos", ascending=False)
    .reset_index(drop=True)
)
grupo_mas_afectado = por_grupo_etario.loc[
    por_grupo_etario["casos"] == por_grupo_etario["casos"].max()
]

departamentos_concentracion = [
    "Juan Martín de Pueyrredón",
    "General Pedernera",
]
casos_por_departamento = departamentos.set_index("departamento")["casos_2017_2022"]
faltantes = set(departamentos_concentracion) - set(casos_por_departamento.index)
if faltantes:
    raise ValueError(
        "No se encontraron los departamentos necesarios para calcular la "
        f"concentración: {', '.join(sorted(faltantes))}"
    )
casos_concentracion = int(casos_por_departamento.loc[departamentos_concentracion].sum())
porcentaje_concentracion = casos_concentracion / total_departamentos * 100

print(f"=== Análisis de suicidios en San Luis ({periodo}) ===")
print(f"Total de casos: {total_departamentos}\n")

print("=== Casos por departamento ===")
print(
    por_departamento.to_string(
        index=False,
        formatters={"porcentaje": "{:.1f}%".format},
    )
)

print("\n=== Distribución por sexo ===")
print(
    por_sexo.to_string(
        index=False,
        formatters={"porcentaje": "{:.1f}%".format},
    )
)

print("\n=== Casos por grupo etario ===")
print(por_grupo_etario.to_string(index=False))
grupos_mas_afectados = ", ".join(grupo_mas_afectado["grupo_etario"].astype(str))
print(
    f"Grupo etario más afectado: {grupos_mas_afectados} "
    f"({int(grupo_mas_afectado['casos'].iloc[0])} casos)"
)

print("\n=== Concentración en Pueyrredón y Pedernera ===")
for departamento in departamentos_concentracion:
    casos = int(casos_por_departamento.loc[departamento])
    porcentaje = casos / total_departamentos * 100
    print(f"{departamento}: {casos} casos ({porcentaje:.1f}%)")
print(
    f"Ambos departamentos: {casos_concentracion} casos "
    f"({porcentaje_concentracion:.1f}% del total provincial)"
)
