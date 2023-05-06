# <p align="center">Direction System d'Information (DSI) - Application de reconnaissance optique de caractères (OCR) </p>

Cette application est une API qui permet de détecter du texte dans des images en utilisant un modèle de machine learning entraîné pour cette tâche. Elle est basée sur la bibliothèque DocTr, FastAPI et l'interface utilisateur Gradio pour une utilisation facile et intuitive.

# Utilisation

L'API accepte une ou deux images au format PNG, JPEG ou BMP. Pour utiliser l'API, envoyez une requête avec les images et l'API renverra le texte détecté dans chaque image sous forme d'une réponse JSON.

Pour exécuter l'application, vous pouvez utiliser Docker ou exécuter le script Python api.py directement sur votre machine. Si vous utilisez Docker, vous pouvez créer l'image Docker en exécutant la commande suivante à partir du répertoire racine du projet :

```
docker build -t nom-de-l-image .
```

Vous pouvez ensuite exécuter l'image Docker en utilisant la commande suivante :

arduino
Copy code
docker run -p 8000:8000 nom-de-l-image
L'application sera alors accessible à l'adresse http://localhost:8000/gradio dans votre navigateur.

# Documentation

Pour plus d'informations sur les formats d'images pris en charge et les paramètres acceptés, veuillez vous référer à la documentation de l'API qui se trouve à l'adresse http://localhost:8000/docs.

# Contact

N'hésitez pas à nous contacter si vous avez des questions ou des commentaires.
