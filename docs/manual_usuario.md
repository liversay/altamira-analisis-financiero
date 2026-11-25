# Manual de uso — Altamira · Análisis Financiero

Sistema web que genera los estados y análisis financieros de Industrias Plásticas Altamira, S.A. en dólares estadounidenses (US$). Todas las cifras se calculan a partir de las cuentas capturadas.

## 1. Instalación y arranque

Requiere Python 3.12 o superior. En una terminal, dentro de la carpeta `sistema`:

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python app.py

En Windows use `.venv\Scripts\pip` y `.venv\Scripts\python`. Abra **http://127.0.0.1:5000** en el navegador y presione `Ctrl + C` en la terminal para detener el sistema. Si el puerto 5000 está ocupado (en macOS suele usarlo AirPlay), inicie con `PORT=5050 .venv/bin/python app.py` y abra el puerto 5050.

Las pruebas automáticas se ejecutan con `.venv/bin/pytest`.

## 2. Navegación

La barra lateral de íconos lleva al menú principal, a los siete módulos y a este manual. Al pasar el cursor se muestra el nombre de cada uno. La parte superior indica:

| Indicador | Significado |
|---|---|
| Balance cuadrado / descuadrado | Activos = Pasivos + Capital en 2023, 2024 y 2025 |
| 2024 reproducido / no coincide | Las cifras calculadas de 2024 son iguales a los estados publicados |
| Datos modificados | Los datos actuales difieren de los originales |
| Imprimir | Imprime la pantalla o la guarda como PDF |

Cuando hay un problema aparece una **alerta roja** en todas las pantallas, con la diferencia en US$. En los estados financieros, haga clic en el título de una sección para ocultar o mostrar sus cuentas.

## 3. Captura y modificación de datos

La pantalla **Captura de datos** tiene cuatro pestañas: balanza 2025 (50 cuentas, columnas Debe y Haber), estados 2024, balance 2023 (base del flujo de efectivo 2024) y datos complementarios (acciones, tasa de impuesto, ventas por producto, precio de mercado opcional y promedios de la industria). El panel **Cuadre 2025** muestra Debe, Haber, Activos y Pasivos + Capital.

Escriba los montos con o sin separador de miles; los negativos pueden ir entre paréntesis. Pulse **Guardar y recalcular** o la tecla Enter. Si un valor no es válido, se informa el error y no se guarda ningún cambio. Guarde cada pestaña antes de cambiar a otra.

### Modificar una sola cuenta de 2025

1. En **Modificar una cuenta 2025** elija la cuenta. Debajo del monto se ve su saldo actual.
2. Escriba el **nuevo saldo** (no el aumento).
3. Elija la **contrapartida**, es decir, la otra cuenta del asiento.
4. Pulse **Aplicar** o Enter.

Con contrapartida se registra la partida doble y el sistema recalcula el impuesto sobre la renta del periodo y lo lleva contra el impuesto por pagar, por lo que el balance sigue cuadrado. Si elige como contrapartida o como cuenta el impuesto del periodo, ese ajuste automático no se realiza. Sin contrapartida solo cambia la cuenta elegida y verá la alerta de descuadre.

| Situación | Cuenta | Contrapartida sugerida |
|---|---|---|
| Se cobra más lento | Cuentas por cobrar comerciales | Caja y bancos |
| Más ventas a crédito | Cuentas por cobrar comerciales | Ventas brutas |
| Se pagan más intereses | Gastos por intereses | Caja y bancos |
| Nueva compra de maquinaria con préstamo | Maquinaria y equipo | Préstamo bancario a largo plazo |

La tabla **Razones que cambiaron** compara cada razón con los datos originales, con su dirección y si mejora o empeora. El botón **Restaurar datos originales** deshace todos los cambios. Las cuentas de 2024 se editan directamente en su pestaña; si deja de cumplirse el balance o la conciliación, aparece la alerta.

## 4. Módulos de resultados

**Estado de resultados.** 2025 frente a 2024, desde ventas brutas hasta utilidad neta y utilidad por acción. El ISR se calcula con la tasa capturada sobre la utilidad antes de impuestos; si la cuenta de ISR de la balanza difiere, se muestra un aviso.

**Balance general.** Comparativo 2025 y 2024. La balanza 2025 está antes del cierre: el sistema cierra utilidad neta y dividendos contra utilidades retenidas y muestra la conciliación (saldo inicial + utilidad neta − dividendos = saldo final).

**Flujo de efectivo.** Método indirecto; use el selector 2025 / 2024. Muestra la conciliación con Caja y bancos y el flujo de efectivo libre (flujo de operación − compra de activos fijos − dividendos pagados). La deuda a largo plazo se presenta como cambio neto.

**Razones financieras.** Las 13 razones en cuatro categorías, con un comentario por categoría que cambia según los datos, y el sistema Du Pont (ROA = margen × rotación de activos; ROE = ROA ÷ (1 − deudas/activos)). El semáforo compara con el promedio de la industria:

| Color | Texto | Regla |
|---|---|---|
| Verde | Cumple | Igual o mejor que la industria |
| Ámbar | Cerca | Hasta 10 % peor |
| Rojo | Alerta | Más de 10 % peor |
| Gris | n/d | No se puede calcular (denominador cero) |

En el periodo de cobranza y en deudas a activos es mejor un valor menor; en las demás razones, uno mayor. En las barras, la línea vertical oscura marca el promedio de la industria.

**Horizontal y vertical.** Variación en US$ y en % de cada cuenta, y cada partida como % de las ventas netas o del activo total, con cuatro gráficos. Una variación sobre base cero se muestra como «n/d».

**Indicadores complementarios.** a) escudo fiscal de depreciación y amortización; b) intereses y arrendamientos antes y después de impuestos; c) valor en libros, utilidad y dividendo por acción, y P/U si se captura un precio de mercado; d) conciliación de ventas por producto; e) utilidad neta frente a flujo de operación y las tres partidas de capital de trabajo de mayor efecto; f) descomposición de la variación del ROE por sustitución en cadena (margen, rotación, endeudamiento); g) efectivo inmovilizado por cobrar más lento que la industria.

## 5. Las 13 razones y sus fórmulas

Se usan saldos de fin de año, ventas netas como numerador de las rotaciones y cuentas por cobrar netas de la estimación para incobrables.

| N.º | Razón | Cálculo |
|---|---|---|
| 1 | Margen de utilidad | Utilidad neta / Ventas netas |
| 2 | Rendimiento sobre los activos (ROA) | Utilidad neta / Activos totales |
| 3 | Rendimiento sobre el capital (ROE) | Utilidad neta / Capital contable |
| 4 | Rotación de las cuentas por cobrar | Ventas netas / Cuentas por cobrar netas |
| 5 | Periodo promedio de cobranza | Cuentas por cobrar netas / (Ventas netas / 360) |
| 6 | Rotación del inventario | Ventas netas / Inventarios totales |
| 7 | Rotación de los activos fijos | Ventas netas / Activos fijos netos |
| 8 | Rotación de los activos totales | Ventas netas / Activos totales |
| 9 | Razón circulante | Activos circulantes / Pasivos circulantes |
| 10 | Razón rápida | (Activos circulantes - Inventarios) / Pasivos circulantes |
| 11 | Deudas a activos totales | Pasivos totales / Activos totales |
| 12 | Rotación del interés ganado | UAII / Gastos por intereses |
| 13 | Cobertura de los cargos fijos | (UAII + Arrendamientos) / (Intereses + Arrendamientos) |

## 6. Cómo interpretar un cambio

Antes de aplicar una modificación, identifique en qué fórmulas participa la cuenta y la contrapartida. Dos ejemplos, partiendo de los datos originales:

| Cambio | Razones afectadas y motivo |
|---|---|
| Cuentas por cobrar +US$100,000 contra Caja y bancos | Baja la rotación de cuentas por cobrar y sube el periodo de cobranza. Las demás no cambian porque un activo circulante sustituye a otro y la utilidad es la misma. |
| Gastos por intereses +US$50,000 pagados con Caja y bancos | Bajan margen, ROA, ROE y las dos coberturas porque hay menos utilidad o más cargos. Bajan los activos, por lo que suben las rotaciones de activos totales y las deudas a activos. El ISR y el ISR por pagar disminuyen; aun así, la caja cae más que los pasivos circulantes y bajan la razón circulante y la rápida. |

## 7. Validación y respaldo

En el menú principal, la **Prueba de validación** compara 23 cifras calculadas de 2024 con las publicadas: resultados, balance, flujo de efectivo y utilidad por acción. Las cifras publicadas solo sirven para comparar.

Los datos originales están en `data/datos_base.json` y no se modifican. Sus cambios se guardan en `data/datos_actuales.json`; borrar ese archivo equivale a restaurar. El PDF de este manual se regenera con `.venv/bin/python herramientas/generar_manual.py`.
