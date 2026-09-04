# E7 — MES CONDICIONAL ESTIMADO EN LUGAR DEL PROXY EWMA — 4-sep-2026

Cierra la unica rendija declarada de E4: la quinta caracteristica de cola era un
proxy EWMA lambda=0,94 (rho_t * sigma_i,t al cierre de la ventana), no un modelo
estimado por maxima verosimilitud. Se sustituye por el MES condicional a un dia
de Brownlees-Engle y se corre el MISMO protocolo en los dos brazos.

Codigo: `e4_dcc.py`. Un solo argumento cambia entre brazos; todo lo demas es
identico, asi que la comparacion es pareada ventana a ventana.

## Que se estima

GJR-GARCH(1,1) por maxima verosimilitud para sigma_i y sigma_m, DCC(1,1)
bivariado por activo contra el mercado con correlation targeting para rho_t, y
las dos esperanzas de cola de forma no parametrica sobre los residuos
estandarizados:

    MES_i = sigma_i,T [ rho_T E(eps_m | eps_m < c)
                        + sqrt(1-rho_T^2) E(xi_i | eps_m < c) ]

Todo dentro de la ventana de 250 dias. Sin mirada al futuro.

## Resultado

UNIVERSO A (464 activos, 2015-2025, 96 ventanas)
                                       dR2 Omega                  placebo
proxy EWMA (E4 publicado):   +0,0240 [+0,0174, +0,0310]   -0,0108 [-0,0142, -0,0071]   PASS
MES condicional GJR-DCC:     +0,0251 [+0,0192, +0,0320]   -0,0102 [-0,0131, -0,0064]   PASS
Diferencia pareada (DCC - EWMA): +0,0011, con 47 de 96 ventanas a favor.

UNIVERSO B (447 activos, 2012-2017, 37 ventanas)
                                       dR2 Omega                  placebo
proxy EWMA (E4 publicado):   +0,0177 [+0,0120, +0,0251]   -0,0077 [-0,0119, -0,0008]   PASS
MES condicional GJR-DCC:     +0,0202 [+0,0147, +0,0287]   -0,0067 [-0,0100, -0,0003]   PASS
Diferencia pareada (DCC - EWMA): +0,0026, con 21 de 37 ventanas a favor.

## Lectura

- **El bloque no dependia del proxy, y la rendija queda cerrada en los dos
  universos.** Cuatro brazos, cuatro PASS, placebo negativo en todos, y en
  ninguno se solapa el intervalo del bloque con el del placebo.
- **La diferencia entre baselines es INDISTINGUIBLE DE CERO.** En el universo A,
  47 de 96 ventanas a favor es exactamente una moneda, y la media es +0,0011. El
  universo B apuntaba lo mismo con menos ventanas. La lectura correcta NO es que
  el bloque mejore con el modelo bien estimado: es que **le da igual cual de los
  dos se use**. Eso es mas fuerte que una mejora, porque significa que el
  resultado no descansaba en la aproximacion.
- Redaccion para el articulo: "sustituir el proxy EWMA por el MES condicional
  estimado no cambia el resultado en ninguno de los dos universos, con la
  diferencia pareada indistinguible de cero". NO escribir que mejora.

## Alcance declarado del experimento

- **No lleva las 12 dummies de sector GICS**: no estan en el panel publico
  re-descargable. El nivel absoluto de dR2 NO es comparable con el E4 del
  preprint; lo valido es la comparacion pareada entre brazos.
- Entorno: python 3.9, scikit-learn 1.6.1. Los dos brazos corren en el mismo
  entorno, asi que la diferencia pareada no depende de la version, pero el nivel
  absoluto si (ver la nota de versiones del repositorio de Omega-N).

## COMO SE CITA ESTO, y no de otra forma

La arquitectura coincide con la del V-Lab, que estima una volatilidad asimetrica
GJR-GARCH y una correlacion DCC para cada empresa contra el indice de mercado y
describe el marco GJR-DCC como el suyo establecido para riesgo sistemico. Pero lo
que aqui se calcula NO es su LRMES ni su SRISK: su LRMES es a seis meses, con
umbral de caida del 40%, por simulacion con residuos remuestreados, y el SRISK
anade valor de mercado y deuda, lo que solo tiene sentido en instituciones
financieras con balance. Este panel son acciones de todos los sectores y la
ventana es de 250 dias, asi que la pieza apropiada es el MES condicional a un
dia, que es el bloque basico sobre el que se construyen aquellas medidas.

    CORRECTO:   "MES condicional de Brownlees y Engle estimado con GJR-GARCH y
                 DCC bivariado, la pieza sobre la que se construyen las medidas
                 del V-Lab"
    INCORRECTO: "el modelo del V-Lab", "hemos batido al V-Lab"

## Referencias

- Brownlees, C. y R. F. Engle. SRISK: a conditional capital shortfall measure of
  systemic risk. Review of Financial Studies 30(1):48-79, 2017.
- Engle, R. F. Dynamic conditional correlation. Journal of Business and Economic
  Statistics 20(3), 2002.
- V-Lab, NYU Stern: documentacion de Systemic Risk Analysis y de GARCH-DCC.
