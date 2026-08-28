# Replicas del positivo de ablacion — 22-ago-2026

## R1 — TEMPORAL (459 activos, 2012-08 a 2017-08, 39 FOMC): **REPLICA, con un matiz**
- 37 ventanas solapadas: dR2 Omega medio **+0,0207, IC95 [+0,0100, +0,0330]**
  -> excluye el cero. La clausula primaria PASA en un periodo casi disjunto
- Independientes: -0,0011 | +0,0426 | +0,0398 | -0,0055 -> 2/4 positivas.
  **MATIZ DECLARADO:** la regla escribia ">=2/3" esperando 3 ventanas y
  salieron 4; mi codigo evaluo ">=2" absoluto. Con lectura estricta de
  fraccion (3/4) la clausula de consistencia NO se alcanza; con lectura
  absoluta si. Se reporta la ambiguedad en vez de resolverla a favor.
  Las dos "negativas" son ceros casi exactos, no negativos.

## R2 — HACIA DELANTE (entrenar solo pasado): **NO PASA, y el diagnostico importa**
- 2/8 positivas, media -0,21, Wilcoxon p=0,84
- **El fallo es del MONTAJE entero, no del bloque:** el R2 BASE fuera de
  tiempo es -0,3 a -4,5 (el nivel del MES cambia de regimen a regimen y un
  modelo entrenado en niveles crudos pasados no transfiere, con o sin
  Omega). El dR2 sobre un baseline roto es ruido
- Consecuencia pre-registrada: **la reclamacion queda ATRIBUCIONAL** (quien
  cargara el estres, seccion cruzada), no predictiva temporal
- Unica continuacion legitima (NO corrida hoy, seria mover la porteria):
  version hacia delante con objetivo ESTANDARIZADO POR PERIODO (rangos o
  z-scores del MES dentro de cada ventana), con pre-registro nuevo

## R3 — MITADES (descriptivo): direccion consistente
mitad A 7/9 positivas (media +0,060) | mitad B 4/9 (media +0,024)

## LECTURA CONJUNTA (regla del pre-registro)
Pasa al menos una confirmatoria (R1 por IC) -> **el positivo queda
REPLICADO en un segundo universo y periodo casi disjunto**, con alcance
ATRIBUCIONAL fijado por R2. Frase para P1 §9 y la sintesis:
"el bloque Omega añade +2 a +4 puntos de R2 transversal sobre el bloque
estandar en dos universos y dos periodos (2012-2017 y 2016-2025), con
suelo de placebo negativo; el alcance es atribucional, y la version
predictiva temporal exige estandarizacion por periodo y queda como
pre-registro futuro".
