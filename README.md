Los resultados estan divididos por cadena (cada una con su carpeta), donde cada una presenta dos archivos: cadena_b.csv y cadena_b_full.csv, cadena_c.csv y cadena_c_full.csv y cadena_v.csv y cadena_v_full.csv. La diferencia es que los "full" contempla las mutaciones tanto de la base de datos como del landscape, mientras que los archivos que no contemplan el "full", solo las mutaciones que se encuentran en la base de datos.

# Con respecto a las columnas

* Mutation
* Wild_type
* Position
* Mutated
* Surface: Presenta 5 salidas, las cuales estan determinadas por la posición (Position) de la mutación:
    * A: Entre las posiciones 154 y 189.
    * B: Entre las posiciones 60 y 103.
    * C: Entre las posiciones 104 y 153.
    * D: Entre las posiciones 1 y 59.
    * Las mutaciones que no esten en ninguno de esos rangos, tienen nulo este valor.
* Predicted_ddg: DDG determinado por SDM.
* Formula: Se definen tres salidas:
    > Increase: Las mutaciones que presentan un DDG por sobre o igual el mean + 1.5*std.
    > Reduce: Las mutaciones que presentan un DDG por debajo o igual del mean - 1.5*std.
    > Neutral: Las mutaciones que presentan un DDG entre medio de los casos anteriores.
* Quartile: Se definen tres salidas:
    > Increase: Las mutaciones que presentan un DDG por sobre o igual del tercer cuartil (0.75).
    > Reduce: Las mutaciones que presentan un DDG por debajo o igual al primer cuartil (0.25).
    > Neutral: Las mutaciones que presentan un DDG entre el primer y tercer cuartil.
* Registered: Indica si la mutación esta registrada o no en la base de datos:
    > 1: Esta registrada.
    > 0: No esta registrada.
* Se detallan los 38 efectos:
    > 1: Presenta el efecto.
    > 0: No presenta el efecto.
* Effects_amount: Cantidad total de efectos que presenta cada mutación, que puede ir desde 0 a 38.
* Se detallan los 5 tipos de VHL:
    > 1: Presenta el tipo de VHL.
    > 0: No presenta el tipo de VHL.
* VHL_amount: Cantidad total de tipos de vhl que presenta cada mutación, que puede ir desde 0 a 5.
