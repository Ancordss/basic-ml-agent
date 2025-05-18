# Agente Turistik - Sistema de Recomendación Turística

Agente Turistik es una aplicación de recomendación de lugares turísticos que utiliza aprendizaje automático para sugerir destinos basados en las preferencias del usuario.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar el repositorio** (si lo tienes en un repositorio):
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd agente-turistik
   ```

2. **Crear y activar un entorno virtual (recomendado)**:
   ```bash
   # En Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Base de Conocimiento

El sistema utiliza un archivo CSV (`base_conocimiento.csv`) que contiene información sobre diferentes tipos de lugares turísticos y sus características. Asegúrate de tener este archivo en el directorio raíz del proyecto.

## Ejecución

1. **Iniciar el servidor FastAPI**:
   ```bash
   uvicorn agente_turistik:app --reload
   ```

2. **Acceder a la documentación interactiva**:
   Abre tu navegador web y ve a:
   ```
   http://127.0.0.1:8000/docs
   ```
   Aquí podrás probar la API directamente desde la interfaz de Swagger.

## Uso de la API

### Endpoint: `POST /recomendar_combinado/`

Envía una solicitud POST con un JSON que contenga las preferencias del usuario:

```json
{
  "transporte": "auto",
  "gastronomia": "sin restricciones",
  "presupuesto": "medio",
  "acompanado": "acompanado",
  "actividad": "moderado",
  "comida": "si"
}
```

### Parámetros aceptados:

- **transporte**: ["caminando", "auto", "transporte publico", "bicicleta", "barco"]
- **gastronomia**: ["sin restricciones", "vegetariano", "vegano", "cocina local", "si", "no"]
- **presupuesto**: ["bajo", "medio", "alto"]
- **acompanado**: ["solo", "acompanado"]
- **actividad**: ["moderado", "relajado"]
- **comida**: ["si", "no"]

### Respuesta de ejemplo:

```json
{
  "recomendaciones": [
    {
      "place_type": "Parque Nacional",
      "probabilidad": 0.8
    },
    {
      "place_type": "Museo",
      "probabilidad": 0.2
    }
  ],
  "recomendacion_final": "Parque Nacional"
}
```

## Estructura del Proyecto

- `agente_turistik.py`: Aplicación principal con la lógica del servidor y el modelo de recomendación.
- `base_conocimiento.csv`: Base de datos con información de lugares turísticos y sus características.
- `requirements.txt`: Lista de dependencias de Python necesarias.

