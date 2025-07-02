import io
import json

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LOAD SPECIES INFO ---
with open("species_info.json") as f:
    species_info = json.load(f)

# --- LOAD CLASS-INDICES & INVERT ---
with open("models/class_indices.json") as f:
    cls2idx = json.load(f)
# cls2idx: { "shrimp": 0, "trout": 1, ... }
idx2cls = {int(v): k for k, v in cls2idx.items()}

# --- LOAD MODEL ---
model = load_model("models/fish_classifier.keras")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1) Validate image
    if file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=400, detail="File is not an image.")
    data = await file.read()
    try:
        img = Image.open(io.BytesIO(data)).convert("RGB").resize((224, 224))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    # 2) Preprocess & Predict
    x = np.array(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)             # e.g. [[0.01, 0.05, 0.9, ...]]
    idx = int(np.argmax(preds, axis=1)[0])
    species = idx2cls[idx]
    confidence = float(np.max(preds))

    # 3) Lookup extra info
    info = species_info.get(species, {})

    return {
        "species":   species,
        "confidence": round(confidence, 2),
        "info":       info
    }
