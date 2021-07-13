import pandas as pd
import numpy as np
import threading
import os

lista_cadenas = ["b","c","v"]
ruta_principal = os.getcwd()

if not os.path.isdir(f"{ruta_principal}/resultados"):
    os.system(f"mkdir {ruta_principal}/resultados")

def mutation(fila):
    return fila[2:]

data_efectos = pd.read_csv(f"{ruta_principal}/data/data_efectos.csv")
data_efectos = data_efectos.drop(["Mutation_type"], axis = 1)
data_tipo_vhl = pd.read_csv(f"{ruta_principal}/data/data_vhl.csv", sep=";")
data_tipo_vhl = data_tipo_vhl.drop(["Protein_sequence"], axis = 1)
data_tipo_vhl["Mutation"] = data_tipo_vhl["Mutation"].apply(mutation)

data_efectos_drop = data_efectos.drop(["Mutation"], axis = 1)
data_tipo_vhl_drop = data_tipo_vhl.drop(["Mutation"], axis = 1)

columnas_efectos = data_efectos_drop.columns.values.tolist()
columnas_tipo_vhl = data_tipo_vhl_drop.columns.values.tolist()

cantidad_efectos = []

for i in range(len(data_efectos_drop)):
    cont = 0
    for columna in columnas_efectos:
        if data_efectos_drop[columna].iloc[i] == 1:
            cont = cont + 1
    cantidad_efectos.append(cont)

cantidad_vhl = []
for i in range(len(data_tipo_vhl_drop)):
    cont = 0
    for columna in columnas_tipo_vhl:
        if data_tipo_vhl_drop[columna].iloc[i] == 1:
            cont = cont + 1
    cantidad_vhl.append(cont)

data_efectos["Effects_amount"] = cantidad_efectos
data_tipo_vhl["VHL_amount"] = cantidad_vhl

data_efectos_vhl = data_efectos.merge(data_tipo_vhl, on = "Mutation")

def wildType(fila):
    return fila[0]

def position(fila):
    if len(fila) == 3:
        return fila[1]
    elif len(fila) == 4:
        return fila[1] + fila[2]
    elif len(fila) == 5:
        return fila[1] + fila[2] + fila[3]

def mutated(fila):
    return fila[-1]

def surface(fila):
    fila_numeric = pd.to_numeric(fila)

    if ((fila_numeric >= 154) and (fila_numeric <= 189)):
        return "A"
    elif ((fila_numeric >= 60) and (fila_numeric <= 103)):
        return "B"
    elif ((fila_numeric >= 104) and (fila_numeric <= 153)):
        return "C"
    elif ((fila_numeric >= 1) and (fila_numeric <= 59)):
        return "D"
    else:
        return ""

def main(cadena):
    if not os.path.isdir(f"{ruta_principal}/resultados/cadena_{cadena}"):
        os.system(f"mkdir {ruta_principal}/resultados/cadena_{cadena}")

    data_sdm = pd.read_csv(f"{ruta_principal}/sdm/chain_{cadena}_sdm.csv")

    data_exportar = pd.DataFrame()
    
    data_exportar.insert(0, "Mutation", data_sdm["Mutation"])
    data_exportar.insert(1, "Wild_type", data_sdm["Mutation"].apply(wildType))
    data_exportar.insert(2, "Position", data_sdm["Mutation"].apply(position))
    data_exportar.insert(3, "Mutated", data_sdm["Mutation"].apply(mutated))
    data_exportar.insert(4, "Surface", data_exportar["Position"].apply(surface))
    data_exportar.insert(5, "Predicted_ddg", data_sdm["Predicted_ddg"])

    promedio = np.mean(data_sdm["Predicted_ddg"])
    std = np.std(data_sdm["Predicted_ddg"])
    formula_mayor = promedio + 1.5*std
    formula_menor = promedio - 1.5*std
    primer_cuartil = np.quantile(data_sdm["Predicted_ddg"], 0.25)
    tercer_cuartil = np.quantile(data_sdm["Predicted_ddg"], 0.75)

    formulas = []
    cuartiles = []

    for i in range(len(data_exportar)):
        if data_exportar["Predicted_ddg"].iloc[i] >= formula_mayor:
            formulas.append("Increase")
        elif data_exportar["Predicted_ddg"].iloc[i] <= formula_menor:
            formulas.append("Reduce")
        else:
            formulas.append("Neutral")

        if data_exportar["Predicted_ddg"].iloc[i] >= tercer_cuartil:
            cuartiles.append("Increase")
        elif data_exportar["Predicted_ddg"].iloc[i] <= primer_cuartil:
            cuartiles.append("Reduce")
        else:
            cuartiles.append("Neutral")
        
    
    data_exportar.insert(6, "Formula", formulas)
    data_exportar.insert(7, "Quartile", cuartiles)

    registradas = []
    estado = False
    for i in range(len(data_exportar)):
        for j in range(len(data_efectos_vhl)):
            if data_exportar["Mutation"].iloc[i] == data_efectos_vhl["Mutation"].iloc[j]:
                registradas.append(1)
                estado = True
                break
        
        if estado == False:
            registradas.append(0)
        else:
            estado = False

    data_exportar.insert(8, "Registered", registradas)
    data_exportar_inner = data_exportar.merge(data_efectos_vhl, on="Mutation")
    data_exportar_full = data_exportar.merge(data_efectos_vhl, on="Mutation", how="outer")

    data_exportar_inner.to_csv(f"{ruta_principal}/resultados/cadena_{cadena}/cadena_{cadena}.csv", index = False, header = True)
    data_exportar_full.to_csv(f"{ruta_principal}/resultados/cadena_{cadena}/cadena_{cadena}_full.csv", index = False, header = True)

for cadena in lista_cadenas:
    t = threading.Thread(target=main, args=(cadena,))
    t.start()