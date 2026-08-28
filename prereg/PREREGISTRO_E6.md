# PREREGISTRO E6: APALANCAMIENTO/FUNDAMENTALES (subperiodo SimFin)
Fecha: 2026-08-23. Escrito ANTES de correr. Datos: SimFin bulk gratuito
subido por el autor (balance e income trimestrales US + companies).

## Alcance impuesto por los datos (declarado)
Cobertura util: Publish Date 2020-2025, solo universo A, 300-346 de 465
tickers segun año. Universo B: sin cobertura, E6 no aplica alli.
E6 es por tanto una prueba de SUBPERIODO (regimen reciente) y de
SUBUNIVERSO (activos cubiertos), y asi se reportara.

## Diseño
- Ventanas elegibles: solapadas (paso 21) del universo A cuyo cierre de
  rasgos sea >= 2021-03-01 y con >= 250 activos con balance publicado
  antes del cierre.
- Universo por ventana: SOLO activos con balance publicado antes del
  cierre (Publish Date <= fin de ventana). Nada de rellenos: la prueba
  dura exige fundamentales reales.
- Cinco columnas fundamentales, del ultimo balance publicado antes del
  cierre: lev_book = Liab/Assets; lev_mkt = Liab/(Liab + acciones x
  precio al cierre); log(Assets); book-to-market = Equity/(acciones x
  precio); rentabilidad = beneficio neto TTM (4 trimestres publicados) /
  Assets. Nulos residuales dentro del subuniverso: mediana de la ventana.
- Brazos sobre el subuniverso y las mismas ventanas:
  A) baseline E5 (26 col) + Omega, como referencia del subperiodo;
  B) baseline E5 + 5 fundamentales (31 col) + Omega  <- LA PRUEBA;
  C) baseline de B + placebo (5 ruido).
- Inferencia: bootstrap por bloques (12) del dR2 pareado.

## REGLA
El bloque sobrevive E6 si en el brazo B su IC95 excluye el cero por
arriba y despeja el techo del placebo (C). Se reporta ademas cuanto
absorben los fundamentales (A vs B). Si no sobrevive, el preprint
incorpora el resultado ANTES de publicar y el titular se ajusta a la
verdad que salga. Un solo disparo.
