import pandas as pd
import numpy as np

# 1. Cargar la base de datos

df = pd.read_csv("dirty_cafe_sales.csv")

print("=== INFORMACIÓN INICIAL ===")
print("Dimensiones:", df.shape)
print("\nTipos de datos:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

print("\nPrimeros registros:")
print(df.head())

# 2. Revisar duplicados

duplicados = df.duplicated().sum()
ids_duplicados = df["Transaction ID"].duplicated().sum()

print("\n=== DUPLICADOS ===")
print("Filas duplicadas:", duplicados)
print("IDs duplicados:", ids_duplicados)

# En esta base no existen duplicados completos.
df = df.drop_duplicates()

# 3. Estandarizar valores inválidos

# ERROR y UNKNOWN representan datos que no son válidos
# o que no fueron registrados correctamente.
df = df.replace(["ERROR", "UNKNOWN"], pd.NA)

# Eliminar espacios innecesarios en columnas de texto
columnas_texto = ["Item", "Payment Method", "Location"]

for columna in columnas_texto:
    df[columna] = df[columna].astype("string").str.strip()

# 4. Corregir tipos de datos

columnas_numericas = [
    "Quantity",
    "Price Per Unit",
    "Total Spent"
]

for columna in columnas_numericas:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

df["Transaction Date"] = pd.to_datetime(
    df["Transaction Date"],
    errors="coerce"
)

# 5. Obtener relación entre producto y precio

# Se utilizan solamente registros donde tanto el producto
# como el precio son válidos.

datos_validos = df.dropna(
    subset=["Item", "Price Per Unit"]
)

precio_por_producto = (
    datos_validos
    .groupby("Item")["Price Per Unit"]
    .agg(lambda x: x.mode().iloc[0])
    .to_dict()
)

print("\n=== PRECIO POR PRODUCTO ===")
print(precio_por_producto)

# 6. Recuperar precios faltantes usando el producto

mascara = (
    df["Price Per Unit"].isna()
    & df["Item"].notna()
)

df.loc[mascara, "Price Per Unit"] = (
    df.loc[mascara, "Item"]
    .map(precio_por_producto)
)

print("\nPrecios recuperados usando Item:", mascara.sum())

# 7. Recuperar cantidades usando Total / Precio

mascara = (
    df["Quantity"].isna()
    & df["Total Spent"].notna()
    & df["Price Per Unit"].notna()
)

cantidad_calculada = (
    df.loc[mascara, "Total Spent"]
    / df.loc[mascara, "Price Per Unit"]
)

# En el dataset las cantidades válidas van de 1 a 5.
validas = (
    cantidad_calculada.between(1, 5)
    & ((cantidad_calculada - cantidad_calculada.round()).abs() < 0.0001)
)

indices = cantidad_calculada[validas].index

df.loc[indices, "Quantity"] = (
    cantidad_calculada.loc[indices].round()
)

print("Cantidades recuperadas:", len(indices))

# 8. Recuperar precios usando Total / Cantidad

mascara = (
    df["Price Per Unit"].isna()
    & df["Total Spent"].notna()
    & df["Quantity"].notna()
)

precio_calculado = (
    df.loc[mascara, "Total Spent"]
    / df.loc[mascara, "Quantity"]
)

precios_validos = set(precio_por_producto.values())

validos = precio_calculado.isin(precios_validos)

indices = precio_calculado[validos].index

df.loc[indices, "Price Per Unit"] = (
    precio_calculado.loc[indices]
)

print("Precios recuperados usando Total / Quantity:", len(indices))

# 9. Recuperar Total Spent

mascara = (
    df["Total Spent"].isna()
    & df["Quantity"].notna()
    & df["Price Per Unit"].notna()
)

df.loc[mascara, "Total Spent"] = (
    df.loc[mascara, "Quantity"]
    * df.loc[mascara, "Price Per Unit"]
)

print("Totales recuperados:", mascara.sum())

# 10. Recuperar Item cuando el precio es único

# Algunos precios solamente pertenecen a un producto.
# En esos casos sí podemos recuperar el Item de forma segura.

productos_por_precio = (
    datos_validos
    .groupby("Price Per Unit")["Item"]
    .apply(lambda x: sorted(set(x)))
)

precio_item_unico = {
    precio: productos[0]
    for precio, productos in productos_por_precio.items()
    if len(productos) == 1
}

mascara = (
    df["Item"].isna()
    & df["Price Per Unit"].isin(precio_item_unico.keys())
)

df.loc[mascara, "Item"] = (
    df.loc[mascara, "Price Per Unit"]
    .map(precio_item_unico)
)

print("Productos recuperados por precio:", mascara.sum())

# 11. Eliminar registros numéricos imposibles de recuperar

# Si faltan Quantity, Price Per Unit o Total Spent y no fue
# posible calcularlos, no se puede conocer correctamente
# el valor económico de la venta.

filas_sin_datos_numericos = df[
    ["Quantity", "Price Per Unit", "Total Spent"]
].isna().any(axis=1)

print(
    "Filas eliminadas por datos numéricos insuficientes:",
    filas_sin_datos_numericos.sum()
)

df = df.loc[~filas_sin_datos_numericos].copy()

# 12. Eliminar fechas imposibles de recuperar

# No es correcto inventar una fecha o sustituirla por una media.
filas_sin_fecha = df["Transaction Date"].isna()

print(
    "Filas eliminadas por fecha no válida:",
    filas_sin_fecha.sum()
)

df = df.loc[~filas_sin_fecha].copy()

# 13. Tratar datos categóricos faltantes

# Item, Payment Method y Location pueden mantenerse como
# "No registrado" cuando no existe información suficiente
# para deducirlos de manera confiable.

for columna in ["Item", "Payment Method", "Location"]:
    df[columna] = df[columna].fillna("No registrado")

# 14. Ajustar tipos finales

df["Quantity"] = df["Quantity"].astype(int)
df["Price Per Unit"] = df["Price Per Unit"].astype(float)
df["Total Spent"] = df["Total Spent"].astype(float)

# 15. Validar resultado

print("\n=== INFORMACIÓN FINAL ===")
print("Dimensiones finales:", df.shape)

print("\nValores nulos:")
print(df.isnull().sum())

print("\nTipos de datos:")
print(df.dtypes)

print("\nResumen estadístico:")
print(df.describe())


# Comprobar que Total Spent sea correcto
errores_total = ~np.isclose(
    df["Total Spent"],
    df["Quantity"] * df["Price Per Unit"]
)

print(
    "\nRegistros con Total Spent inconsistente:",
    errores_total.sum()
)

# 16. Exportar base limpi

df.to_csv(
    "cafe_sales_clean.csv",
    index=False,
    date_format="%Y-%m-%d"
)

print("\nBase limpia exportada como cafe_sales_clean.csv")