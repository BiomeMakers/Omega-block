# E6: fundamentales SimFin (subperiodo) — 23-ago-2026
Datos: SimFin bulk gratuito (balance+income trimestral US). Cobertura:
2020-2025, universo A, ~300-346/465 tickers. Universo B sin cobertura.

45 ventanas solapadas (cierre >= mar-2021), 293-313 activos con balance
REAL por ventana (sin rellenos fuera del subuniverso):
  referencia (26 col):            +0,0124 [+0,0025, +0,0179]
  CON fundamentales (31 col):     +0,0132 [+0,0007, +0,0245]  <- LA PRUEBA
  placebo (sobre 31):             -0,0058 [-0,0084, -0,0026]
Fundamentales añadidos: lev contable (L/A), lev mercado (L/(L+cap)),
log activos, book-to-market, rentabilidad TTM/activos.
VEREDICTO (regla pre-registrada, 1 disparo): SOBREVIVE. El apalancamiento
y los fundamentales NO absorben el efecto en el regimen reciente: el
punto ni baja (0,0124 -> 0,0132).
Limite declarado: subperiodo 2021-2025 y subuniverso cubierto; el
periodo completo y el universo B quedan sin control de fundamentales
(la capa gratuita de SimFin no llega).
