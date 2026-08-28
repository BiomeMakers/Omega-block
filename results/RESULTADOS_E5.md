# E5: tamaño/liquidez y estabilidad de placebos — 23-ago-2026

## E5a — baseline MAX + log dolar-volumen + Amihud (26 col): SOBREVIVE
                     dR2 Omega                  placebo
465, 2016-2025:  +0,0128 [+0,0082, +0,0178]   -0,0120 [-0,0183, -0,0066]
459, 2012-2017:  +0,0128 [+0,0056, +0,0205]   -0,0049 [-0,0085, +0,0012]
Punto identico en ambos universos. Tamaño/liquidez absorbe ~12% y ya.
El riesgo "patron TIM" (rival barato fuera del baseline) queda cerrado
para todos los rivales computables del panel.

## E5b — estabilidad del sorteo de placebos: INESTABLE a 1x, ARREGLADO a 5x
Pool = nº eventos:      Spearman mediano entre semillas 0,517 (min 0,164)
Pool = 5x eventos:      Spearman mediano 0,882 (min 0,491)
dR2 por semilla (5x):   0,0387 / 0,0398 / 0,0382 (estable siempre)
DECISION (regla pre-registrada): Q4 se define con pool 5x en el preprint.
Fichero de señal regenerado con la definicion nueva; hash actualizado en
PILOT_TERMS Annex B.
