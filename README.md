# Práctica de limpieza de datos

## Análisis y Visualización de la Información

En esta práctica trabajé con el dataset **Cafe Sales – Dirty Data for Cleaning Training**, con el objetivo de aplicar técnicas de limpieza y transformación de datos usando Python.

La base original contiene **10,000 registros y 8 columnas**, pero varios datos vienen con errores intencionales, por ejemplo valores vacíos, textos como `ERROR` y `UNKNOWN`, tipos de datos incorrectos y registros que necesitan ser reconstruidos usando otras columnas.

Mi objetivo fue dejar la base lo más limpia y consistente posible sin inventar información que realmente no se pudiera recuperar.

## Archivos del repositorio

- `dirty_cafe_sales.csv`: base de datos original.
- `limpieza_cafe.py`: código que utilicé para limpiar la base.
- `cafe_sales_clean.csv`: base resultante después del proceso de limpieza.
- `README.md`: explicación del procedimiento y de las decisiones tomadas.

## Columnas del dataset

La base contiene las siguientes columnas:

- Transaction ID
- Item
- Quantity
- Price Per Unit
- Total Spent
- Payment Method
- Location
- Transaction Date

## Procedimiento

Primero cargué el archivo con Pandas para revisar sus dimensiones, tipos de datos, valores faltantes y posibles registros duplicados.

Después revisé las columnas y encontré valores como `ERROR`, `UNKNOWN` y espacios vacíos. Para poder trabajar todos estos casos de una manera más uniforme, los convertí primero a valores nulos.

También corregí los tipos de datos. Las columnas `Quantity`, `Price Per Unit` y `Total Spent` deberían ser numéricas, mientras que `Transaction Date` debía manejarse como fecha.

Una de las partes que más me sirvió fue aprovechar la relación entre algunas columnas para recuperar información faltante.

La relación principal es:

```text
Total Spent = Quantity × Price Per Unit
```

Entonces también pude obtener:

```text
Quantity = Total Spent / Price Per Unit
```

y:

```text
Price Per Unit = Total Spent / Quantity
```

De esta forma, en vez de rellenar datos con una media o con cualquier valor, intenté recuperar la información usando datos reales del mismo registro.

También analicé la relación entre los productos y sus precios. Cuando conocía el producto pero faltaba el precio, utilicé el precio observado para ese producto dentro de los registros válidos.

En algunos casos también pude recuperar el producto a partir del precio, pero solamente cuando ese precio correspondía claramente a un solo producto. Si había varias opciones, preferí no inventar nada.

Para columnas como `Payment Method` y `Location`, cuando no fue posible recuperar el dato, utilicé el valor `No registrado`.

No quise llenar estos datos usando simplemente la categoría más frecuente porque eso habría hecho parecer que conocíamos información que en realidad no estaba disponible xd.

También eliminé registros cuando faltaban datos numéricos importantes y no existía una forma lógica de reconstruirlos.

En el caso de las fechas inválidas o faltantes, decidí eliminar esos registros porque no había forma confiable de saber en qué fecha había ocurrido realmente la transacción.

Finalmente revisé que `Total Spent` fuera consistente con la multiplicación de `Quantity` por `Price Per Unit` y exporté la base limpia.

## Tabla resumen

| Problema encontrado | Registros afectados | Acción realizada | Justificación |
|---|---:|---|---|
| Valores inválidos o faltantes en `Item` | 969 | Recuperé algunos productos usando precios únicos y marqué los demás como `No registrado` | Evité asignar un producto cuando existían varias posibilidades |
| Valores inválidos o faltantes en `Quantity` | 479 | Calculé la cantidad con `Total Spent / Price Per Unit` cuando fue posible | Pude recuperar el dato usando una relación matemática real |
| Valores inválidos o faltantes en `Price Per Unit` | 533 | Utilicé el precio conocido del producto o calculé `Total Spent / Quantity` | Aproveché datos válidos que ya existían en la base |
| Valores inválidos o faltantes en `Total Spent` | 502 | Calculé el total usando `Quantity × Price Per Unit` | Es una relación directa entre las columnas |
| Valores inválidos o faltantes en `Payment Method` | 3,178 | Los cambié por `No registrado` | No tenía forma segura de saber qué método de pago se utilizó |
| Valores inválidos o faltantes en `Location` | 3,961 | Los cambié por `No registrado` | No era correcto elegir entre `In-store` o `Takeaway` sin evidencia |
| Fechas inválidas o faltantes | 460 | Eliminé los registros | No había una manera confiable de reconstruir la fecha |
| Datos numéricos que no pudieron reconstruirse | 26 | Eliminé los registros | Sin cantidad, precio o total suficientes no podía representar correctamente la venta |
| Filas duplicadas | 0 | No realicé cambios | No encontré registros completamente duplicados |

## Decisiones tomadas

Una decisión importante fue no rellenar automáticamente todos los valores faltantes usando media, mediana o moda.

Consideré que hacerlo así podía modificar demasiado los datos originales y generar valores que nunca existieron realmente.

En las columnas numéricas preferí intentar recuperar los datos usando relaciones entre las mismas variables.

Para las variables categóricas, como método de pago y ubicación, preferí utilizar `No registrado` antes que asumir que correspondían a la categoría más frecuente.

También eliminé los registros cuya fecha no podía recuperarse, porque mantenerlos con una fecha inventada podía afectar análisis posteriores relacionados con el tiempo.

En general, intenté que cada cambio tuviera una justificación y no limpiar datos solamente por hacerlo.

## Resultado

Después del proceso de limpieza, la base terminó con aproximadamente **9,514 registros válidos**.

La versión final:

- no contiene valores `ERROR`;
- no contiene valores `UNKNOWN`;
- tiene tipos de datos adecuados;
- mantiene consistencia entre cantidad, precio y total;
- no contiene registros duplicados;
- conserva como `No registrado` los datos categóricos que no pude recuperar de forma segura.

La base limpia quedó guardada como:

```text
cafe_sales_clean.csv
```

## Tecnologías utilizadas

Para realizar la práctica utilicé:

- Python
- Pandas
- NumPy
