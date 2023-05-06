# <p align="center">Direction System d'Information (DSI) - Application de reconnaissance optique de caractères (OCR) </p>

Cette application est une API qui permet de détecter du texte dans des images en utilisant un modèle de machine learning entraîné pour cette tâche. Elle est basée sur la bibliothèque DocTr, FastAPI et l'interface utilisateur Gradio pour une utilisation facile et intuitive.

# Utilisation

L'API accepte une ou deux images au format PNG, JPEG ou BMP. Pour utiliser l'API, envoyez une requête avec les images et l'API renverra le texte détecté dans chaque image sous forme d'une réponse JSON.

Pour exécuter l'application, vous pouvez utiliser Docker ou exécuter le script Python api.py directement sur votre machine. Si vous utilisez Docker, vous pouvez créer l'image Docker en exécutant la commande suivante à partir du répertoire racine du projet :

```
docker build -t nom-de-l-image .
```

Vous pouvez ensuite exécuter l'image Docker en utilisant la commande suivante :

```
docker run -p 8000:8000 nom-de-l-image
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

Le payload d'entrée doit être un objet JSON avec une clé "data" contenant un tableau de deux éléments représentant les images d'entrée :

```
{
  "data": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==", 
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
  ]
}
```

La première image correspond à la première page d'un document et la deuxième image correspond à la deuxième page du même document. Les images sont encodées en base64.

## Exemple de payload d'entrée

```
{
  "data": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==", 
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
  ]
}
```

## Exemple de réponse

La réponse renvoie un objet JSON contenant un tableau de deux éléments, qui représentent les résultats de la reconnaissance de caractères pour chaque image :

```
{
  "data": [
    "Hello, world!", 
    "This is the second page."
  ],
  "duration": 2.5
}
```

La clé "duration" représente le temps de traitement en secondes.

# Utilisation de l'API

Vous pouvez tester l'API en envoyant une requête POST avec des images encodées en base64. Vous pouvez utiliser des outils comme cURL ou Postman pour tester l'API.

```
curl -X POST \
  http://localhost:8000/gradio/run/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "data": [
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==", 
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
    ]
}'
```

# Contact

N'hésitez pas à nous contacter si vous avez des questions ou des commentaires.

Mail : abokor.ahmed.kadar.nour@outlook.com
