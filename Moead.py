import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import itertools
from mpl_toolkits.mplot3d import Axes3D
import random

# ------------------------------------------------
# La función MOEA/D recibe los siguientes parámetros:
# ------------------------------------------------
# m: the number of objectives
# H: the decomposition parameter
# N: the number of weight vectors and solutions
# T: the neighborhood size T
# ------------------------------------------------
# Tiene la siguiente salida:
# ------------------------------------------------
# nonDominatedSet: the nondominated set of solutions
# ------------------------------------------------

# ------------------------------------------------------
# PASO 1: Inicialización: calcular los vectores de peso:
# ------------------------------------------------------

# Función para calcular la N, a partir de una combinatoria, usando m y H
def obtenerNumberOfWeightVectors(numberOfObjectives, decompositionParameter):
    r = numberOfObjectives - 1
    n = decompositionParameter + numberOfObjectives - 1
    N = math.comb(n + r - 1, r)
    print(f"\nNumero de vectores de peso: {N}")
    return N

# Funcion para calcular los de vectores de peso para cualquier m
def generar_vectores_pesos(M, H):
    vectores = []

    # Elegimos M−1 posiciones de corte entre H+M−1 posibles
    for cortes in itertools.combinations(range(H + M - 1), M - 1):
        # Añadimos los extremos
        indices = (-1,) + cortes + (H + M - 1,)
        # Calculamos los k_i mediante diferencias
        ks = [indices[i+1] - indices[i] - 1 for i in range(M)]
        # Convertimos k_i en lambda_i = k_i / H
        vectores.append([k / H for k in ks])
    return vectores


# Funcion que dibuja un vector de peso 2D desde el origen con su etiqueta (k1/H, k2/H).
def graficar_vectores(vectores, M, H):
    """
    Grafica vectores de peso en 2D (M=2) o en 3D (M=3).

    Parámetros:
        vectores: lista de listas, cada vector es [λ1, λ2] o [λ1, λ2, λ3]
        M: número de objetivos (2 o 3)
    """

    # ------------------------------------------------------
    # CASO M = 2  (Gráfica estilo Das & Dennis)
    # ------------------------------------------------------
    if M == 2:
        plt.figure(figsize=(8,8))

        # GRID azul
        plt.grid(True, linestyle=":", linewidth=0.8, color="deepskyblue")

        # Ejes negros gruesos
        plt.axhline(0, color="black", linewidth=2)
        plt.axvline(0, color="black", linewidth=2)

        # Línea diagonal del simplex
        plt.plot([0,1], [1,0], linestyle="--", color="gray")

        # Ticks especiales 0, 1/H, 2/H, ... 1
        ticks = [i/H for i in range(H+1)]
        plt.xticks(ticks)
        plt.yticks(ticks)

        # Estilo de marcas y etiquetas fraccionarias
        for t in ticks:
            plt.plot([t, t], [0, -0.02], color="deepskyblue", linewidth=2)
            plt.plot([-0.02, 0], [t, t], color="deepskyblue", linewidth=2)

            plt.text(t, -0.05,
                    f"$\\frac{{{int(t*H)}}}{{H={H}}}$",
                    ha='center', va='top', fontsize=8, color="deepskyblue")

            plt.text(-0.05, t,
                    f"$\\frac{{{int(t*H)}}}{{H={H}}}$",
                    ha='right', va='center', fontsize=8, color="deepskyblue")

        # ---- Flechas + puntos + etiquetas ----
        for i, v in enumerate(vectores):
            x, y = v

            plt.arrow(
                0, 0, x, y,
                head_width=0.025,
                head_length=0.025,
                length_includes_head=True,
                fc="black",
                ec="black"
            )

            plt.scatter([x], [y], color="black")

            k1 = int(round(x * H))
            k2 = int(round(y * H))

            plt.text(
                x + 0.03, y + 0.03,
                f"$\\lambda^{i+1} = (\\frac{{{k1}}}{{{H}}}, \\frac{{{k2}}}{{{H}}})$",
                fontsize=9, color="deepskyblue"
            )

        plt.xlim(-0.1, 1.1)
        plt.ylim(-0.1, 1.1)
        plt.xlabel("$\\lambda_1$", fontsize=14)
        plt.ylabel("$\\lambda_2$", fontsize=14)
        plt.title("Vectores de peso (M = 2) — Das & Dennis", fontsize=16)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        return

    # ------------------------------------------------------
    # CASO M = 3  (Gráfica 3D con flechas y triángulo del simplex)
    # ------------------------------------------------------
    if M == 3:
        fig = plt.figure(figsize=(9,9))
        ax = fig.add_subplot(111, projection='3d')

        xs = [v[0] for v in vectores]
        ys = [v[1] for v in vectores]
        zs = [v[2] for v in vectores]

        # puntos
        ax.scatter(xs, ys, zs, color="deepskyblue")

        # flechas desde el origen
        for v in vectores:
            x, y, z = v
            ax.quiver(0,0,0,  x,y,z, color="black", arrow_length_ratio=0.1)

        # simplex triangular
        tri = np.array([
            [1,0,0],
            [0,1,0],
            [0,0,1],
            [1,0,0]
        ])
        ax.plot(tri[:,0], tri[:,1], tri[:,2], "--", color="deepskyblue")

        ax.set_xlabel("$\\lambda_1$")
        ax.set_ylabel("$\\lambda_2$")
        ax.set_zlabel("$\\lambda_3$")

        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_zlim(0,1)

        ax.set_title("Vectores de peso (M = 3)", fontsize=16)
        plt.show()
        return

    # ------------------------------------------------------
    # CASO INVALIDO
    # ------------------------------------------------------
    else: ("\nSolo se puede graficar para M = 2 o M = 3.")


# ------------------------------------------------------
# PASO 2: Determinación de los k vecinos de cada vector de peso
# ------------------------------------------------------

def vecinos_mas_cercanos(vectores, k):
    vectores = np.array(vectores)
    N = len(vectores)
    # Matriz NxN de distancias euclidianas
    distancias = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            distancias[i, j] = np.linalg.norm(vectores[i] - vectores[j])
    # Arreglo donde guardamos los vecinos
    vecinos = []
    print("\n")
    for i in range(N):
        # Ordenar por distancia
        orden = np.argsort(distancias[i])
        # Tomar los k más cercanos
        k_vecinos = orden[:k]
        vecinos.append(k_vecinos)
        # Imprimir 
        print(f"lambda {i+1}: B{i+1} = {k_vecinos + 1}")
    return vecinos



# ------------------------------------------------------
# PASO 3: Generar una población aleatoriamente
# ------------------------------------------------------

def generar_individuo(dominios):
    # Obtener lista de variables
    variables = list(dominios.keys())
    n = len(variables)
        
    azul = [0] * n
    verde = [0] * n
        
    
    return azul, verde

# Generar la población
def generarPoblacion(numeroIndividuos):
    
    poblacion = []
    
    df = pd.read_csv("./data/diabetes_dataset.csv")
    
    def get_domains(df):
        domains = {}
        for col in df.columns:
            domains[col] = sorted(df[col].dropna().unique().tolist())
        return domains

    dominios = get_domains(df)
    print(dominios)
    """
    dominios = {
    "gender": ["Male", "Female"],
    "location": ["Alabama", ],
    "hypertension",
    "heart_disease",
    "smoking_history",
    "diabetes",
    "race",
    "age",
    "bmi",
    "hbA1c_level",
    "blood_glucose_level"
    }
    """
    
    for i in range(numeroIndividuos):
        poblacion.append(generar_individuo(dominios))
    
    print(poblacion)
    
    return poblacion


# ------------------------------------------------------
# Función que implementa el algoritmo MOEA/D
# ------------------------------------------------------

def moeadAlgorithm(numberOfObjectives, decompositionParameter, numberOfWeightVectors, neighborhoodSize, numeroIndividuos):
    
    # ------------------------------------------------------
    # PASO 1: Inicialización: calcular los vectores de peso:
    # ------------------------------------------------------

    # Para la inicialización de los vectores de peso (dirección) usamos el método de Das and Dennis
    print(f"\nSe van a generar {numberOfWeightVectors} vectores de peso")
    
    # Arreglo para almacenar los vectores de peso
    vectores_l = generar_vectores_pesos(numberOfObjectives, decompositionParameter)
    print(f"\nVectores de peso: {vectores_l}")
    graficar_vectores(vectores_l, numberOfObjectives, decompositionParameter)
    
    
    # ------------------------------------------------------
    # PASO 2: Determinación de los k vecinos de cada vector 
    # ------------------------------------------------------
    
    vecinos = vecinos_mas_cercanos(vectores_l, k=neighborhoodSize)
    
    # ------------------------------------------------------
    # PASO 3: Generar una población aleatoriamente
    # ------------------------------------------------------
    
    generarPoblacion(numeroIndividuos)



# Función principal del programa
def main():
    # Parámetros de prueba:
    # m
    numberOfObjectives = 2
    # H
    decompositionParameter = 8
    # N
    numberOfWeightVectors = obtenerNumberOfWeightVectors(numberOfObjectives, decompositionParameter)
    # T
    neighborhoodSize = 3
    # Tamaño de la población
    numeroIndividuos = 100
    
    # Llamar a la función MOEA/D
    moeadAlgorithm(numberOfObjectives, decompositionParameter, numberOfWeightVectors, neighborhoodSize, numeroIndividuos)

# Llamar a la función principal:
main()