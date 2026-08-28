# PREREGISTRO E5: TAMAÑO/LIQUIDEZ y ESTABILIDAD DEL SORTEO DE PLACEBOS
Fecha: 2026-08-23. Escrito ANTES de correr. Motivado por el riesgo "rival
barato fuera del baseline" (el patron TIM).

## E5a — baseline MAX + tamaño/liquidez (la prueba que decide)
Al baseline MAX de 24 columnas se añaden DOS proxies computables del panel:
log del dolar-volumen medio de la ventana (tamaño/liquidez) y log del
iliquidez de Amihud (media de |ret|/dolar-volumen). Total 26.
Misma maquinaria que E4 (96/37 ventanas solapadas, placebo 5 ruido,
block bootstrap 12/6). REGLA: el bloque sobrevive si su IC95 excluye el
cero por arriba Y despeja el techo del placebo, EN LOS DOS universos.
Si no sobrevive, se corrige el preprint ANTES de publicar y el titular
baja a la version que sea verdad.

## E5b — estabilidad de Q3-Q5 al sorteo de dias placebo
En el universo A, recomputar el bloque con TRES sorteos independientes de
dias placebo (semillas 31, 101, 202). Se mide: (1) Spearman mediano de
omr entre pares de semillas (sobre las 9 ventanas independientes);
(2) dR2 del bloque (9 independientes) por semilla.
REGLA declarativa: se reporta; se declara INESTABLE si el Spearman
mediano < 0,8 o si el signo del dR2 medio cambia entre semillas, y en ese
caso la definicion de Q4 pasa a mediana sobre sorteos multiples en el
preprint (cambio declarado).
