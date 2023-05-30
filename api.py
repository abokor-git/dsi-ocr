from doctr.models import ocr_predictor

from fastapi import FastAPI, status
import gradio as gr

import numpy as np
import pandas as pd

import re

import socket
import os
# Let's pick the desired backend
# os.environ['USE_TF'] = '1'
os.environ['USE_TORCH'] = '1'


# Instantiate a pretrained model
predictor = ocr_predictor("db_mobilenet_v3_large",
                          "crnn_vgg16_bn", pretrained=True)

CUSTOM_PATH = "/gradio"

hostname = socket.gethostname()

app = FastAPI()


@app.get("/")
def read_main():
    return {"container_id": hostname, "api_type": "ocr"}


def treatment(img):

    result = predictor([img])
    json_export = result.export()

    try:

        delta_up = 1.3
        delta_down = 0.5

        value = []
        x1_x = []
        x1_y = []
        x2_x = []
        x2_y = []

        for a in json_export["pages"]:
            for b in a["blocks"]:
                for c in b["lines"]:
                    for d in c["words"]:
                        value.append(d["value"])
                        x1_x.append(d["geometry"][0][0])
                        x1_y.append(d["geometry"][0][1])
                        x2_x.append(d["geometry"][1][0])
                        x2_y.append(d["geometry"][1][1])

        data = {
            "value": value,
            "x1_x": x1_x,
            "x1_y": x1_y,
            "x2_x": x2_x,
            "x2_y": x2_y,
        }

        # Création du DataFrame à partir du dictionnaire
        all_ocr = pd.DataFrame(data)

        all_ocr['value'] = all_ocr['value'].replace(
            '^\s*$', np.nan, regex=True)
        all_ocr_no_na = all_ocr.dropna(subset=['value'])

        type_cni = False

        if 'CARTE' in value and 'NATIONALE' in value:
            for x in list(all_ocr_no_na["value"]):
                if re.match(r'^\d{6}$', x):
                    type_cni = True

        if type_cni == False:
            print("arrêt du programe")

        value = list(all_ocr_no_na["value"])
        x1_x = list(all_ocr_no_na["x1_x"])
        x1_y = list(all_ocr_no_na["x1_y"])
        x2_x = list(all_ocr_no_na["x2_x"])
        x2_y = list(all_ocr_no_na["x2_y"])

        id_clean = 0

        for x in range(len(value)):
            if value[x] == 'Directeur' or value[x] == 'Director' or value[x] == 'Directour':

                for y in range(len(value)):
                    if value[y] == 'Domicile':

                        if x1_y[x] > x2_y[y]:
                            id_clean = x2_x[x]
                            break
                    if value[y] == 'Profession':

                        if x1_y[x] > x2_y[y]:
                            id_clean = x2_x[x]
                            break

        if id_clean != 0:
            all_ocr_filter = all_ocr_no_na.drop(
                all_ocr_no_na[all_ocr_no_na['x1_x'] > id_clean].index)
        else:
            all_ocr_filter = all_ocr_no_na

        value = list(all_ocr_filter["value"])
        x1_x = list(all_ocr_filter["x1_x"])
        x1_y = list(all_ocr_filter["x1_y"])
        x2_x = list(all_ocr_filter["x2_x"])
        x2_y = list(all_ocr_filter["x2_y"])

        # CNI
        cni = ''
        for x in value:
            if re.match(r'^\d{6}$', x):
                cni = x

        # Date Birth
        date_birth = ''
        for x in value:
            if re.match(r'\b\d{2}\.\d{2}\.\d{4}\b', x):
                date_birth = x

        # Name
        name = []

        for x in range(len(value)):
            resultats = re.findall(r'\b[Nn]om\b', value[x])
            up = x1_y[x] - ((x2_y[x]-x1_y[x])*delta_up)
            down = x2_y[x] + ((x2_y[x]-x1_y[x])*delta_down)
            if resultats:
                for y in range(len(value)):
                    if re.match(r'^[A-Z./-]*$', value[y]) and x1_y[y] > up and x2_y[y] < down:
                        name.append(value[y])

        name_str = ' '.join(name)
        name.pop(0)
        father_str = ' '.join(name)

        # City
        city = []

        for x in range(len(value)):
            resultats = re.findall(r'\b[aà]\b', value[x])
            up = x1_y[x] - ((x2_y[x]-x1_y[x])*delta_up)
            down = x2_y[x] + ((x2_y[x]-x1_y[x])*delta_down)
            if resultats:
                for y in range(len(value)):
                    if re.match(r'^[A-Z./-]*$', value[y]) and x1_y[y] > up and x2_y[y] < down:
                        city.append(value[y])

        city_str = ' '.join(city)

        # Mother
        mother = []

        for x in range(len(value)):
            resultats = re.findall(r'\bet(?:\sde|de)?\b', value[x])
            up = x1_y[x] - ((x2_y[x]-x1_y[x])*delta_up)
            down = x2_y[x] + ((x2_y[x]-x1_y[x])*delta_down)
            if resultats:
                for y in range(len(value)):
                    if re.match(r'^[A-Z./-]*$', value[y]) and x1_y[y] > up and x2_y[y] < down:
                        mother.append(value[y])

        mother_str = ' '.join(mother)

        # Profession
        profession = []

        for x in range(len(value)):
            resultats = re.findall(r'\b[Pp]rofession\b', value[x])
            up = x1_y[x] - ((x2_y[x]-x1_y[x])*delta_up)
            down = x2_y[x] + ((x2_y[x]-x1_y[x])*delta_down)
            if resultats:
                for y in range(len(value)):
                    if re.match(r'^[A-Z./-]*$', value[y]) and x1_y[y] > up and x2_y[y] < down:
                        profession.append(value[y])

        profession_str = ' '.join(profession)

        # Domicile
        home = []

        for x in range(len(value)):
            resultats = re.findall(r'\b[Dd]omicile\b', value[x])
            up = x1_y[x] - ((x2_y[x]-x1_y[x])*delta_up)
            down = x2_y[x] + ((x2_y[x]-x1_y[x])*delta_down)
            if resultats:
                for y in range(len(value)):
                    if re.match(r'^[A-Z./-]*$', value[y]) and x1_y[y] > up and x2_y[y] < down:
                        home.append(value[y])

        home_str = ' '.join(home)

        json_resp = {
            "document_id": cni,
            "first_name": "",
            "last_name": name_str,
            "date_of_birth": date_birth,
            "place_of_birth": city_str,
            "father_name": father_str,
            "mother_name": mother_str,
            "profession": profession_str,
            "address": home_str,
            "document_type": "CNI",
            "issue_date": "",
            "expiration_date": ""
        }

        code = status.HTTP_200_OK

    except:

        json_resp = {
            "document_id": "",
            "first_name": "",
            "last_name": "",
            "date_of_birth": "",
            "place_of_birth": "",
            "father_name": "",
            "mother_name": "",
            "profession": "",
            "address": "",
            "document_type": "",
            "issue_date": "",
            "expiration_date": ""
        }

        code = status.HTTP_204_NO_CONTENT

    return {"http_code": code, "ocr_text": json_resp}


demo = gr.Interface(
    fn=treatment,
    inputs=["image"],
    outputs=["json"],
)

app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)

# Run this from the terminal as you would normally start a FastAPI app: `uvicorn api:app --port 8016`
# and navigate to http://localhost:8000/gradio in your browser.
