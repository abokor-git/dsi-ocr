# <p align="center">Direction System d'Information (DSI) - Application de reconnaissance optique de caractères (OCR) </p>

Cette application est une API qui permet de détecter du texte dans des images en utilisant un modèle de machine learning entraîné pour cette tâche. Elle est basée sur la bibliothèque DocTr, FastAPI et l'interface utilisateur Gradio pour une utilisation facile et intuitive.

# Fonctionnalités

* Reconnaissance optique des caractères (OCR) sur les cartes d'identité djiboutiennes.
* Prise en charge des cartes d'identité djiboutiennes d'avant-dernière génération.
* Interface utilisateur conviviale avec Gradio pour télécharger et afficher les résultats.

> Note : Dans un futur proche, nous prévoyons d'ajouter la prise en charge des passeports, des cartes de séjour, et d'autres types de documents.

# Utilisation

L'API accepte une image au format PNG, JPEG ou BMP. Pour utiliser l'API, envoyez une requête avec l'image et l'API renverra le texte détecté dans l'image sous forme d'une réponse JSON.

Pour exécuter l'application, vous pouvez utiliser Docker ou exécuter le script Python api.py directement sur votre machine. Si vous utilisez Docker, vous pouvez créer l'image Docker en exécutant la commande suivante à partir du répertoire racine du projet :

```
docker build -t nom-de-l-image .
```

Vous pouvez ensuite exécuter l'image Docker en utilisant la commande suivante :

```
docker run -p 8000:8000 nom-de-l-image
```

Ou directement utiliser l'image disponible sur le hub docker :

```
docker run -p 8000:8000 abokor16/dsi-ocr:3.0
```

L'application sera alors accessible à l'adresse http://localhost:8000/gradio dans votre navigateur.

# Documentation

L'API de reconnaissance optique de caractères (OCR) est accessible via l'URL http://localhost:8000/gradio. Elle accepte les requêtes HTTP POST avec les images au format PNG, JPEG ou BMP.

## Exemple de requête

```
POST /run/predict
http://localhost:8000/gradio/run/predict
```

## Payload d'entrée

Le payload d'entrée doit être un objet JSON avec une clé "data" contenant un tableau d'éléments représentant l'images d'entrée :

```
{
  "data": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==", 
  ]
}
```

Les images sont encodées en base64.

## Exemple de payload d'entrée

```
{
  "data": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==",
  ]
}
```

## Exemple de réponse

La réponse renvoie un objet JSON contenant un tableau d'élément, qui représentent le résultat de la reconnaissance de caractères pour l'image en question :

```
{
  "data": [
    {
        "id_document": "",
        "prenom": "",
        "nom": "",
        "ne": "",
        "a": "",
        "father": "",
        "mother": "",
        "profession": "",
        "domicile": "",
        "type_document": "",
        "date_delivrance": "",
        "date_expiration": "",
    }
  ],
  "duration": 2.5
}
```

La clé "duration" représente le temps de traitement en secondes.

# Utilisation de l'API

Vous pouvez tester l'API en envoyant une requête POST avec une image encodée en base64. Vous pouvez utiliser des outils comme cURL ou Postman pour tester l'API.

```
curl -X POST \
  http://localhost:8000/gradio/run/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "data": [
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==", 
    ]
}'
```

# Contact

N'hésitez pas à nous contacter si vous avez des questions ou des commentaires.

Mail : abokor.ahmed.kadar.nour@outlook.com
