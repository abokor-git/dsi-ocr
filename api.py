import os
# Let's pick the desired backend
# os.environ['USE_TF'] = '1'
os.environ['USE_TORCH'] = '1'

import sys

from fastapi import FastAPI

import gradio as gr
import numpy as np

import json
import re

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Instantiate a pretrained model
predictor = ocr_predictor("db_resnet50", "crnn_vgg16_bn", pretrained=True)

CUSTOM_PATH = "/gradio"

app = FastAPI()

@app.get("/")
def read_main():
    return {"Home": "Bienvenue dans notre API de reconnaissance optique de caractères (OCR). Cette API permet de détecter du texte dans des images en utilisant un modèle de machine learning entraîné pour cette tâche. Pour utiliser cette API, envoyez une requête avec une ou deux images au format PNG, JPEG ou BMP. L'API renverra le texte détecté dans chaque image sous forme d'une réponse JSON. Pour utiliser cette API, veuillez vous référer à la documentation pour obtenir des instructions détaillées sur les formats d'images pris en charge et les paramètres acceptés. N'hésitez pas à nous contacter si vous avez des questions ou des commentaires."}

def treatment(img1):
    json_export = []
    doc = [img1]
    for x in doc:
        if isinstance(x, np.ndarray):
            result = predictor([x])
            json_export.append(result.export())

            string_to_list = json_export

            list_dict = []

            for x in string_to_list:
                # Convertir le dictionnaire Python en chaîne JSON correctement formatée
                json_string = json.dumps(x, ensure_ascii=False)
                json_dict = json.loads(json_string)
                list_dict.append(json_dict)

            
            cni_pattern = [
                r'\b[Nn]om\b',
                r'\bn[éeèê](?:l|le)?\b',
                r'\b[aà]\b',
                #r'\bde\b',
                r'\bet(?:\sde|de)?\b',
                r'\b[Pp]rofession\b',
                r'\b[Dd]omicile\b',
                r'\bCNI\w*\b',
            ]

            cni_pattern_co = {
                "\\b[Nn]om\\b": "nom",
                "\\bn[éeèê](?:l|le)?\\b": "ne",
                "\\b[aà]\\b": "a",
                #"\\bde\\b": "de",
                '\\bet(?:\sde|de)?\\b': "mother",
                "\\b[Pp]rofession\\b": "profession",
                "\\b[Dd]omicile\\b": "domicile",
                "\\bCNI\w*\\b": "id_document",
            }

            cni_locate = []

            #for a in list_dict:
            for b in list_dict[0]["pages"]:
                for c in b["blocks"]:
                    for d in c["lines"]:
                        for e in d["words"]:
                            for f in cni_pattern:
                                resultats = re.findall(f, e["value"])
                                found_value = []
                                if resultats:
                                    for h in list_dict[0]["pages"]:
                                        for i in h["blocks"]:
                                            for j in i["lines"]:
                                                for k in j["words"]:
                                                    if e["geometry"][0][1]-k["geometry"][0][1] < 0.02 and e["geometry"][0][1]-k["geometry"][0][1] > 0:
                                                        found_value.append(k["value"])
                                    cni_locate.append([cni_pattern_co[f],found_value])

            for x in cni_locate:
                for y in x[1]:
                    if not y.isnumeric():
                        resultats = re.findall('[a-z]', y)
                        if resultats:
                            x[1].remove(y)

            json_resp = {
                "id_document": "",
                "prenom": "",
                "nom": "",
                "ne": "",
                "a": "",
                "father": "",
                "mother": "",
                "profession": "",
                "domicile": "",
                "type_document": "CNI",
                "date_delivrance": "",
                "date_expiration": "",
            }

            for x in cni_locate:
                som = ""
                for y in x[1]:
                    som=som+" "+y
                json_resp[x[0]]=som

    return json_resp

demo = gr.Interface(
    fn=treatment,
    inputs=["image"],
    outputs=["text"],
)

app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)

# Run this from the terminal as you would normally start a FastAPI app: `uvicorn api:app`
# and navigate to http://localhost:8000/gradio in your browser.
