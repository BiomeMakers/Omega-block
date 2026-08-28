# PREREGISTRO: ENDURECIMIENTOS previos al preprint
Fecha: 2026-08-22. Escrito ANTES de correr nada. Mismo protocolo base
(boosting fijo, 5 pliegues por activo, objetivo MES futuro, panel 465).

## E1 — CONTROL SECTORIAL (el que decide si hay preprint)
Bloque base AMPLIADO con las dummies de sector GICS (11 + "Other" para
los sin mapear). Brazos: base+sector | base+sector+Omega |
base+sector+placebo(5 ruido). 96 ventanas solapadas, dR2 pareado, block
bootstrap (bloques 12).
REGLA: el bloque Omega sobrevive si su dR2 SOBRE base+sector tiene IC95
excluyendo el cero por arriba y despeja el techo del placebo. Si no
sobrevive, el resultado se reescribe como "en parte pertenencia sectorial"
y el preprint cambia de titular (se publica igual, con esa verdad).

## E2 — HACIA DELANTE ESTANDARIZADO (SEGUNDO DISPARO, declarado)
Mismo diseño forward que R2 (entrenar solo pasado, 8 ventanas de prueba)
con DOS cambios pre-registrados: objetivo = rango percentil del MES dentro
de cada ventana; cada caracteristica tambien en rangos dentro de ventana
(modelo transversal libre de escala). REGLA: Wilcoxon p<0,05 Y >=6/8
positivas -> el alcance sube a PREDICTIVO. Si falla, la via forward queda
CERRADA con dos disparos y se escribe como limitacion probada.
Multiplicidad declarada: es el 2º intento forward; su p se lee con eso.

## E3 — ROBUSTEZ DE PROTOCOLO (descriptivo, sin regla)
La ablacion principal (sin sector) sobre las 9 ventanas independientes con
tres configuraciones alternativas fijadas aqui: (a) depth 2, lr 0.1,
300 arboles; (b) depth 4, lr 0.05, 200 arboles; (c) config original con
semilla de pliegues 7. Se REPORTAN los tres dR2 medios sin elegir.
