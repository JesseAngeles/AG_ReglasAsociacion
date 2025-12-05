import pandas as pd

df = pd.read_csv("./data/diabetes_dataset.csv")

# Convertir columnas numéricas 
numeric_cols = ["age", "bmi", "hbA1c_level", "blood_glucose_level"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# ====== NUEVO: Convertir one-hot de raza a una columna única ======
race_cols = [
    "race:AfricanAmerican",
    "race:Asian",
    "race:Caucasian",
    "race:Hispanic",
    "race:Other"
]

# Obtener la raza correspondiente al 1 en cada fila
df["race"] = df[race_cols].idxmax(axis=1).str.replace("race:", "")

# Eliminar las columnas one-hot
df = df.drop(columns=race_cols)
# ================================================================

# Filtrar solo 2019
df = df[df["year"] == 2019].drop(columns=["year"])

# RANGOS
ranges_age = [
    ("niño", 0, 9),
    ("adolescente", 10, 19),
    ("joven", 20, 59),
    ("adulto mayor", 60, 100),
]

ranges_bmi = [
    ("bajo peso", 0, 18.4),
    ("peso normal", 18.5, 24.9),
    ("sobrepeso", 25, 29.9),
    ("obesidad", 30, 100),
]

ranges_hba1c = [
    ("normal", 0, 5.6),
    ("limite", 5.7, 6.4),
    ("sobre", 6.5, 20)
]

ranges_glucose = [
    ("hipoglucemia", 0, 79),
    ("normal", 80, 159),
    ("elevado", 160, 199),
    ("critico", 200, 1000)
]

# Función de discretización genérica
def discretize(df, col, ranges, new_name):
    df[new_name] = None
    for label, low, high in ranges:
        mask = df[col].between(low, high, inclusive="both")
        df.loc[mask, new_name] = label

# Aplicar discretizaciones
discretize(df, "age", ranges_age, "age_cat")
discretize(df, "bmi", ranges_bmi, "bmi_cat")
discretize(df, "hbA1c_level", ranges_hba1c, "hba1c_cat")
discretize(df, "blood_glucose_level", ranges_glucose, "glucose_cat")

# Eliminar columnas originales numéricas
df = df.drop(columns=numeric_cols)

# Renombrar
df = df.rename(columns={
    "age_cat": "age",
    "bmi_cat": "bmi",
    "hba1c_cat": "hbA1c_level",
    "glucose_cat": "blood_glucose_level",
})

df.to_csv("./data/diabetes_clean_dataset.csv", index=False)