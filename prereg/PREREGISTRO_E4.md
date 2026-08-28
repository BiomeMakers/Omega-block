# PREREGISTRO E4: BASELINE MAXIMO PUBLICO DE COLA
Fecha: 2026-08-22. Escrito ANTES de correr. La pregunta del autor: ¿batimos
lo mejor publico? Respuesta pendiente de esta prueba; el titulo del
preprint depende de su desenlace y se acepta el que salga.

## Baseline MAX (todo computable de precios, todo publico)
Los 7 estandar + 12 dummies de sector + CINCO caracteristicas de cola:
1. beta bajista: cov/var condicionadas a dias de mercado negativo (250d)
2. cosimetria: E[(ri-mi)(rm-mm)^2] / (si*sm^2)
3. cocurtosis:  E[(ri-mi)(rm-mm)^3] / (si*sm^3)
4. semidesviacion bajista del propio activo (dias ri<0)
5. pronostico MES condicional tipo V-Lab (proxy EWMA lambda=0.94:
   rho_t * sigma_i,t al cierre de la ventana)
Total baseline MAX: 24 columnas.

## Prueba (misma maquinaria que E1)
96 ventanas solapadas del panel de 465, dR2 pareado del bloque Omega y del
placebo (5 ruido) SOBRE el baseline MAX, block bootstrap (bloques 12).
REGLA: el titulo puede reclamar "sobre el mejor baseline publico" solo si
el IC95 del bloque Omega excluye el cero por arriba Y despeja el techo del
placebo. Si no, el titulo se queda en "bloque estandar con sector" y la
tabla E4 se publica igual como limite medido.
Secundaria (reportada): lo mismo en el universo B (459, 2012-17).
