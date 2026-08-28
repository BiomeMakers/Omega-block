# PREREGISTRO: ABLACION NO LINEAL — ¿aporta el bloque Omega dentro del
# paradigma ganador (arboles sobre caracteristicas)?
Fecha: 2026-08-22. Escrito ANTES de correr nada.

## Pregunta
Los 13 cierres eran lineales o univariantes. ¿Llevan las coordenadas de la
familia Omega valor MARGINAL NO LINEAL (interacciones) sobre el bloque
estandar, con objetivo de RIESGO?

## Montaje (unico; hiperparametros FIJOS, sin ajuste)
Panel 465 activos. Ventanas 250d dentro / 250d fuera; independientes paso
250 (9) y solapadas paso 21 (~96) para la inferencia.
Objetivo: MES futuro del activo (media de sus retornos en el 5% de peores
dias del sistema en la ventana FUERA).
Modelo: HistGradientBoostingRegressor(max_iter=300, max_depth=3,
learning_rate=0.05), identico en los dos brazos. Evaluacion: 5 pliegues
POR ACTIVO dentro de cada ventana (el modelo nunca ve los activos de
prueba); ambos brazos comparten pliegues y periodo, y el estadistico es la
DIFERENCIA pareada, asi que cualquier fuga temporal afecta igual a los dos.

## Bloques de caracteristicas (todos de la ventana DENTRO, 250d)
BASE (7): beta, vol21, vol250, momento (252d saltando 21), reversion (21d),
MES pasado, fuerza (suma de |corr|).
OMEGA (5): diag(A^3) crudo, tri_exc (exceso sobre el nulo de configuracion
por fuerzas, forma cerrada E[(A^3)_ii] = s_i^2 (Σs^2)^2 / S^3), respuesta
al FOMC (mediana de eventos de la ventana), deriva basal (placebos), y
Omega-R = respuesta/basal. Sin calcular: NaN -> mediana del dia (declarado).

## Estadistico y regla (PRIMARIA, unica)
DeltaR2 = R2(BASE+OMEGA) - R2(BASE), por ventana (media de pliegues).
Inferencia: block bootstrap pareado sobre las ~96 ventanas solapadas
(bloques de 12, 2.000 remuestreos), IC 95% de la media de DeltaR2.
PASA solo si el IC excluye el cero por arriba Y >=6 de las 9 ventanas
independientes tienen DeltaR2 > 0. Cualquier otra cosa: CIERRA (14º y
ultimo con datos de precio).

## Control de cordura obligatorio
Bloque PLACEBO de 5 columnas de ruido gaussiano con el mismo protocolo:
su DeltaR2 acota lo que "5 columnas mas" regalan por sobreajuste del
procedimiento. El DeltaR2 de Omega se lee CONTRA ese suelo.

## Lo que NO se reclama
Nada de retorno. Un solo disparo, sin rejillas de hiperparametros.
