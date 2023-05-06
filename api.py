import os
# Let's pick the desired backend
# os.environ['USE_TF'] = '1'
os.environ['USE_TORCH'] = '1'

import sys

from fastapi import FastAPI

import gradio as gr
import numpy as np

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Instantiate a pretrained model
predictor = ocr_predictor("db_resnet50", "crnn_vgg16_bn", pretrained=True)

CUSTOM_PATH = "/gradio"

app = FastAPI()

@app.get("/")
def read_main():
    return {"Home": "Bienvenue dans notre API de reconnaissance optique de caractères (OCR). Cette API permet de détecter du texte dans des images en utilisant un modèle de machine learning entraîné pour cette tâche. Pour utiliser cette API, envoyez une requête avec une ou deux images au format PNG, JPEG ou BMP. L'API renverra le texte détecté dans chaque image sous forme d'une réponse JSON. Pour utiliser cette API, veuillez vous référer à la documentation pour obtenir des instructions détaillées sur les formats d'images pris en charge et les paramètres acceptés. N'hésitez pas à nous contacter si vous avez des questions ou des commentaires."}

def treatment(img1,img2):
    json_export = []
    doc = [img1,img2]
    for x in doc:
        if isinstance(x, np.ndarray):
            result = predictor([x])
            json_export.append(result.export())
    return json_export

demo = gr.Interface(
    fn=treatment,
    inputs=["image","image"],
    outputs=["text"],
)

app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)

# Run this from the terminal as you would normally start a FastAPI app: `uvicorn api:app`
# and navigate to http://localhost:8000/gradio in your browser.
