# Ablacion no lineal — PRIMER PASE de la campaña (22-ago-2026, 14º falsador)

Pregunta (suya): ¿aporta Omega como COMPONENTE de una arquitectura mayor,
no como arquitectura? Protocolo GKX-style: boosting (hiperparametros fijos),
bloque BASE de 7 caracteristicas estandar (beta, vol21, vol250, momento,
reversion, MES pasado, fuerza), objetivo = MES futuro (250d), 5 pliegues
por activo, panel de 465 (2016-2025).

## PRIMARIA (pre-registrada): dR2 del bloque Omega (5 columnas)
- 9 ventanas independientes: positivo en 8/9, media +0,0408
- 96 solapadas: media +0,0340, IC95 block bootstrap [+0,0271, +0,0421]
  -> EXCLUYE EL CERO POR ARRIBA
- Control placebo (5 columnas de ruido, mismo protocolo): -0,0157
  [-0,0201, -0,0124] -> añadir columnas SIN señal EMPEORA; la ganancia de
  Omega no es artefacto de dimension. Distancia al suelo: ~+0,05
- REGLA: IC>0 y >=6/9 -> **PASA (8/9)**

## Descomposicion (POST-HOC declarada) y robustez sin covid
| bloque añadido a BASE            | dR2     | IC95              | sin covid |
| completo (5)                     | +0,0340 | [+0,027, +0,043]  | +0,0322 [+0,026, +0,039] |
| solo ESTATICO (tri, tri_exc)     | +0,0297 | [+0,024, +0,034]  | +0,0292 [+0,024, +0,033] |
| solo DOS-TIEMPOS (resp,bas,omr)  | +0,0092 | [+0,003, +0,018]  | +0,0069 [+0,002, +0,013] |

**La señal la lleva sobre todo tri_exc/diag(A^3) usados NO linealmente**
(el mismo objeto de P1 §9), y la respuesta al FOMC añade un incremento
menor pero significativo. Aproximadamente aditivos.

## Alcance (decir siempre)
- Es EXPLICACION TRANSVERSAL del reparto futuro de estres sistemico
  (QUIEN lo cargara), no una señal de trading temporal: los pliegues son
  por activo y ambos brazos comparten periodo; el estadistico pareado es
  justo, la reclamacion es atribucional, la misma familia que P1 §9
- Un solo universo. REPLICACION PENDIENTE en el panel de 42 (no esta en
  el contenedor) antes de escribir nada fuerte
- Nada de retorno

## Lectura de campaña
Los 13 cierres median a Omega COMO INDICE (solo, lineal, o actuador).
El 14º mide a Omega COMO CARACTERISTICA dentro del paradigma ganador, y
pasa con suelo de placebo negativo. La conclusion de toda la campaña queda:
"como arquitectura, no; como componente no lineal de la arquitectura
canonica, si, con +3-4 puntos de R2 transversal sobre el bloque estandar".
Esto REESCRIBE la seccion 9 de P1 y el articulo de sintesis.
