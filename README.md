# Práctica de limpieza de datos

## Análisis y Visualización de la Información

Esta práctica tiene como objetivo aplicar técnicas de limpieza y transformación de datos utilizando Python y la biblioteca Pandas.

Se utilizó el dataset **Cafe Sales – Dirty Data for Cleaning Training**, el cual contiene errores intencionales como valores faltantes, valores `ERROR` y `UNKNOWN`, tipos de datos incorrectos y datos que requieren ser reconstruidos a partir de otras columnas.

La base original contiene **10,000 registros y 8 columnas**.

## Archivos del repositorio

- `dirty_cafe_sales.csv`: base de datos original.
- `limpieza_cafe.py`: código utilizado para realizar la limpieza.
- `cafe_sales_clean.csv`: base de datos resultante después del proceso de limpieza.
- `README.md`: descripción del procedimiento y decisiones tomadas.

## Columnas del dataset

El conjunto de datos contiene las siguientes variables:

- Transaction ID
- Item
- Quantity
- Price Per Unit
- Total Spent
- Payment Method
- Location
- Transaction Date

## Procedimiento

Primero se cargó e inspeccionó el dataset utilizando Pandas. Se revisaron sus dimensiones, tipos de datos, valores faltantes y posibles registros duplicados.

Posteriormente se detectó que diferentes columnas contenían los valores `ERROR`, `UNKNOWN` y datos vacíos. Estos valores se transformaron inicialmente en valores nulos para poder tratarlos de manera uniforme.

Las columnas `Quantity`, `Price Per Unit` y `Total Spent` fueron convertidas a datos numéricos, mientras que `Transaction Date` fue transformada a un tipo de fecha.

Para recuperar algunos datos faltantes se utilizaron las relaciones existentes entre las variables.

Por ejemplo:

```text
Total Spent = Quantity × Price Per Unit
```

Por lo tanto, también fue posible obtener:

```text
Quantity = Total Spent / Price Per Unit
```

y:

```text
Price Per Unit = Total Spent / Quantity
```

También se obtuvo la relación existente entre cada producto y su precio utilizando los registros válidos del dataset. Esto permitió recuperar precios faltantes cuando se conocía el producto.

En algunos casos también fue posible recuperar el producto a partir del precio, pero solamente cuando dicho precio correspondía de manera exclusiva a un producto. Cuando existían varias posibilidades no se realizó ninguna suposición.

Los datos categóricos que no pudieron recuperarse de forma confiable fueron etiquetados como `No registrado`.

Los registros donde no fue posible recuperar los datos numéricos necesarios para conocer correctamente una venta fueron eliminados.

También se eliminaron los registros cuya fecha era desconocida o inválida, debido a que no existe una forma confiable de determinar la fecha real de una transacción sin inventar información.

Finalmente se verificó que el valor de `Total Spent` fuera consistente con la multiplicación de cantidad por precio unitario y se exportó la información resultante a `cafe_sales_clean.csv`.

## Tabla resumen

| Problema encontrado | Registros afectados | Acción realizada | Justificación |
|---|---:|---|---|
| Valores inválidos o faltantes en `Item` | 969 | Se recuperaron algunos productos utilizando precios únicos y los restantes se marcaron como `No registrado` | No se asignó un producto cuando existían varias posibilidades |
| Valores inválidos o faltantes en `Quantity` | 479 | Se calculó la cantidad mediante `Total Spent / Price Per Unit` cuando fue posible | La relación matemática permite recuperar el valor sin realizar una estimación |
| Valores inválidos o faltantes en `Price Per Unit` | 533 | Se utilizó el precio conocido del producto o la relación `Total Spent / Quantity` | Se utilizaron datos existentes del mismo registro y del catálogo observado de productos |
| Valores inválidos o faltantes en `Total Spent` | 502 | Se calculó mediante `Quantity × Price Per Unit` | Es una relación directa entre las variables del dataset |
| Valores inválidos o faltantes en `Payment Method` | 3,178 | Se sustituyeron por `No registrado` | No existe información suficiente para determinar el método de pago real |
| Valores inválidos o faltantes en `Location` | 3,961 | Se sustituyeron por `No registrado` | No es correcto asignar arbitrariamente `In-store` o `Takeaway` |
| Fechas inválidas o faltantes | 460 | Se eliminaron los registros | No existe una forma confiable de recuperar la fecha real de la transacción |
| Datos numéricos que no pudieron reconstruirse | 26 | Se eliminaron los registros | Sin cantidad, precio o total suficientes no se puede representar correctamente la venta |
| Filas duplicadas | 0 | No fue necesario realizar cambios | No se encontraron registros completamente duplicados |

## Decisiones tomadas

Se evitó sustituir automáticamente todos los valores faltantes utilizando la media, mediana o moda, porque este procedimiento podría introducir información que nunca ocurrió realmente.

En las variables numéricas se intentó recuperar primero la información mediante relaciones matemáticas entre las columnas.

Para variables categóricas como método de pago y ubicación se utilizó la categoría `No registrado`, ya que asignar la categoría más frecuente habría modificado artificialmente la distribución de los datos.

En el caso de las fechas se decidió eliminar los registros sin una fecha válida, debido a que inventar o estimar una fecha podría afectar cualquier análisis temporal realizado posteriormente.

## Resultado

Después del proceso de limpieza, la base contiene aproximadamente **9,514 registros válidos**.

La versión final:

- no contiene valores `ERROR`;
- no contiene valores `UNKNOWN`;
- tiene tipos de datos adecuados;
- mantiene consistencia entre cantidad, precio y total;
- no contiene registros duplicados;
- conserva como `No registrado` los datos categóricos que no podían recuperarse de forma segura.

La base resultante se encuentra en:

`cafe_sales_clean.csv`

## Tecnologías utilizadas

- Python
- Pandas
- NumPy
