# PREREGISTRO: REPLICAS del positivo de ablacion no lineal
Fecha: 2026-08-22. Escrito ANTES de correr nada.
Mismo protocolo que PREREGISTRO_ABLACION (mismos bloques, mismos
hiperparametros fijos, mismo objetivo MES futuro). Tres replicas:

## R1 — REPLICA TEMPORAL: panel de 447 (2012-2017)
Datos: espejo publico liorsidi/sp500-stock-similarity-time-series
(el mismo que usa el repo del TSI). Periodo 2012-08 a 2017-08, casi
disjunto del panel principal (2016-2025). FOMC 2012-2017 codificado a mano.
Potencia DECLARADA baja: ~3 ventanas independientes, ~36 solapadas.
REGLA: replica si dR2 Omega tiene IC95 block bootstrap (bloques de 6)
excluyendo el cero por arriba Y >=2/3 independientes positivas.

## R2 — REPLICA HACIA DELANTE (la que decide el alcance): panel de 465
Entrenamiento SOLO con ventanas PASADAS: para la ventana independiente k
(k=2..9), el modelo se entrena con las secciones cruzadas apiladas de las
ventanas 1..k-1 y se evalua en la seccion cruzada de la ventana k (que el
modelo no ha visto ni en activos ni en tiempo). dR2 = R2(base+Omega) -
R2(base) por ventana de prueba (8 puntos).
REGLA: replica si Wilcoxon de signos con rangos da p<0,05 a favor Y >=6/8
positivas. Si pasa, la reclamacion sube de atribucional a PREDICTIVA
transversal. Si falla pero el diseño por pliegues aguanta, la reclamacion
queda explicitamente atribucional y asi se escribe.

## R3 — ESTABILIDAD POR MITADES (solo ventanas independientes)
Particion aleatoria fija de los 465 en dos mitades disjuntas; protocolo de
pliegues dentro de cada mitad. Se REPORTA la consistencia (sin regla de
pase; es descriptivo).

## Multiplicidad y lectura conjunta
R1 y R2 son confirmatorias con reglas propias; se reportan las dos pasen o
no. El positivo original solo se declara REPLICADO si pasa al menos UNA de
las dos confirmatorias; su alcance (atribucional o predictivo) lo decide R2.
