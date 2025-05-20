from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

CSV_PATH = "base_conocimiento.csv"

questions = [
    ("transporte", ["caminando","auto","transporte publico","bicicleta","barco"]),
    ("gastronomia", ["sin restricciones","vegetariano","vegano","cocina local","si","no"]),
    ("presupuesto", ["bajo","medio","alto"]),
    ("acompanado", ["solo","acompanado"]),
    ("actividad", ["moderado","relajado"]),
    ("comida", ["si","no"])
]

class UserAnswers(BaseModel):
    transporte: str = "caminando"
    gastronomia: str = "sin restricciones"
    presupuesto: str = "bajo"
    acompanado: str = "acompanado"
    actividad: str = "relajado"
    comida: str = "si"

def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path)
    categorias = [
        ["caminando","auto","transporte publico","bicicleta","barco"],
        ["sin restricciones","vegetariano","vegano","cocina local","si","no"],
        ["bajo","medio","alto"],
        ["solo","acompanado"],
        ["moderado","relajado"],
        ["si","no"]
    ]
    place_types = df["place_type"].unique()
    rows = []
    for place in place_types:
        row = {"place_type": place}
        df_place = df[df["place_type"]==place]
        for i, cat in enumerate(categorias):
            found = df_place[df_place["user_answer"].isin(cat)]
            val = found["user_answer"].iloc[0] if not found.empty else None
            row[f"cat_{i}"] = val
        rows.append(row)
    df_ml = pd.DataFrame(rows)
    df_ml = df_ml.dropna()
    return df_ml

df_ml = load_and_prepare_data(CSV_PATH)

app = FastAPI()

@app.post("/recomendar_combinado/")
def recomendar_combinado(respuestas: UserAnswers):
    # Create a default instance to get default values
    defaults = UserAnswers()
    
    # Use default values if field is empty string or undefined
    user_answers = [
        respuestas.transporte if respuestas.transporte and respuestas.transporte.strip() else defaults.transporte,
        respuestas.gastronomia if respuestas.gastronomia and respuestas.gastronomia.strip() else defaults.gastronomia,
        respuestas.presupuesto if respuestas.presupuesto and respuestas.presupuesto.strip() else defaults.presupuesto,
        respuestas.acompanado if respuestas.acompanado and respuestas.acompanado.strip() else defaults.acompanado,
        respuestas.actividad if respuestas.actividad and respuestas.actividad.strip() else defaults.actividad,
        respuestas.comida if respuestas.comida and respuestas.comida.strip() else defaults.comida
    ]
    print("User answers with defaults applied:", user_answers)

    # Configura aquí los pesos para cada categoría (ajusta según importancia)
    pesos = [1, 1, 3, 3, 1, 1]

    # Umbral minimo para filtrar lugares (suma ponderada)
    umbral_minimo = 5  # por ejemplo, ajustar a tu conveniencia

    # Calcular puntajes ponderados para todos los lugares
    scores = []
    for _, row in df_ml.iterrows():
        score = sum((row[f"cat_{i}"] == user_answers[i]) * pesos[i] for i in range(6))
        scores.append((row['place_type'], score))

    # Filtrar lugares que cumplen con el umbral minimo
    lugares_filtrados = [p for p, s in scores if s >= umbral_minimo]

    if not lugares_filtrados:
        raise HTTPException(status_code=404, detail="No se encontraron lugares con suficiente coincidencia.")

    # Si solo uno, devolver directo
    if len(lugares_filtrados) == 1:
        elegido = lugares_filtrados[0]
        return {
            "recomendaciones": [{"place_type": elegido, "probabilidad": 1.0}],
            "recomendacion_final": elegido
        }

    # Si hay varios, usar modelo ML para ordenar esos lugares
    df_filtrado = df_ml[df_ml["place_type"].isin(lugares_filtrados)]
    X = df_filtrado.drop(columns=["place_type"])
    y = df_filtrado["place_type"]
    enc = OneHotEncoder(handle_unknown="ignore")
    X_enc = enc.fit_transform(X)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_enc, y)

    X_user = pd.DataFrame([user_answers], columns=[f"cat_{i}" for i in range(6)])
    X_user_enc = enc.transform(X_user)

    probs = clf.predict_proba(X_user_enc)[0]
    classes = clf.classes_
    sorted_places = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:10]

    total_prob = sum(prob for _, prob in sorted_places)
    resultados = [{"place_type": p, "probabilidad": float(prob / total_prob)} for p, prob in sorted_places]

    elegido = sorted_places[0][0]

    return {
        "recomendaciones": resultados,
        "recomendacion_final": elegido
    }
