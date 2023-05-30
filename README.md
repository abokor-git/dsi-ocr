# <p align="center">Direction System d'Information (DSI) - Application de reconnaissance optique de caractères (OCR) </p>

Cette application est une API qui permet de détecter du texte dans des images en utilisant un modèle de machine learning entraîné pour cette tâche. Elle est basée sur la bibliothèque FastAPI et l'interface utilisateur Gradio pour une utilisation facile et intuitive.

# Fonctionnalités

* Reconnaissance optique des caractères (OCR) sur les cartes d'identité djiboutiennes.
* Prise en charge des cartes d'identité djiboutiennes d'avant-dernière génération.
* Interface utilisateur conviviale avec Gradio pour télécharger et afficher les résultats.

> Note : Dans un futur proche, nous prévoyons d'ajouter la prise en charge des passeports, des cartes de séjour, et d'autres types de documents.

# Installation

1. Clonez ce dépôt sur votre machine locale :

```
git clone https://github.com/abokor-git/dsi-ocr.git
```

2. Accédez au répertoire du projet :

```
cd dsi-ocr
```

3. Installez les dépendances nécessaires :

```
pip install -r requirements.txt
```

# Utilisation

1. Démarrez l'application FastAPI :

```
uvicorn api:app --port 8016
```

2. Accédez à l'interface utilisateur en ouvrant votre navigateur et en vous rendant à l'adresse suivante :

```
http://localhost:8016/gradio
```

3. Unploader une image de carte d'identité djiboutienne d'avant-dernière génération.

4. Cliquez sur le bouton "Soumettre" pour lancer le processus OCR.

5. Les résultats OCR seront affichés sur la page.

# Déploiement avec Docker

Vous avez deux options pour déployer l'application à l'aide de Docker : construire l'image localement à partir du Dockerfile ou télécharger l'image préconstruite depuis DockerHub.

## Option 1 : Construire l'image localement

Assurez-vous d'avoir Docker installé sur votre machine avant de suivre ces étapes :

1. Assurez-vous d'être dans le répertoire principal du projet où se trouve le fichier Dockerfile.

2. Construisez l'image Docker en exécutant la commande suivante :

```
docker build -t nom_de_votre_image .
```

3. Une fois que la construction de l'image est terminée, exécutez un conteneur à partir de l'image :

```
docker run -p 8016:8016 nom_de_votre_image
```

4. Accédez à l'interface utilisateur en ouvrant votre navigateur et en vous rendant à l'adresse suivante :

```
http://localhost:8016/gradio
```

5. Vous pouvez maintenant unploader une image de carte d'identité djiboutienne d'avant-dernière génération et effectuer l'OCR en utilisant l'application.

## Option 2 : Télécharger l'image depuis DockerHub

1. Exécutez la commande suivante pour télécharger l'image préconstruite depuis DockerHub :

```
docker pull dsi-ocr:latest
```

2. Une fois le téléchargement terminé, exécutez un conteneur à partir de l'image :

```
docker run -p 8016:8016 dsi-ocr:latest
```

3. Accédez à l'interface utilisateur en ouvrant votre navigateur et en vous rendant à l'adresse suivante :

```
http://localhost:8016/gradio
```

4. Vous pouvez maintenant télécharger une image de carte d'identité djiboutienne d'avant-dernière génération et effectuer l'OCR en utilisant l'application.

N'hésitez pas à choisir l'option qui convient le mieux à vos besoins. Assurez-vous d'avoir des connaissances de base sur Docker pour une utilisation appropriée.

# Utilisation de l'API Gradio

En plus de l'interface utilisateur, l'application FastAPI avec OCR pour les cartes d'identité djiboutiennes offre également une API basée sur Gradio. Vous pouvez envoyer des requêtes POST à l'API en incluant une image encodée en base64, et elle renverra une réponse avec les résultats OCR.

## Envoi d'une requête POST

Effectuez une requête POST à l'endpoint /gradio/run/predict avec le payload suivant :

```
{
  "data": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
  ]
}
```

Assurez-vous de remplacer "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==" par la représentation en base64 de votre image.

Exemple d'utilisation avec cURL :

```
curl -X POST -H "Content-Type: application/json" -d '{"data": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="]}' http://localhost:9000/gradio/run/predict
```

## Réponse de l'API

L'API renverra une réponse JSON avec les informations suivantes :

```
{
  "http_code": 200|204,
  "ocr_text": {
    "document_id": "DOCUMENT_ID",
    "first_name": "FIRST_NAME",
    "last_name": "LAST_NAME",
    "date_of_birth": "DATE_OF_BIRTH",
    "place_of_birth": "PLACE_OF_BIRTH",
    "father_name": "FATHER_NAME",
    "mother_name": "MOTHER_NAME",
    "profession": "PROFESSION",
    "address": "ADDRESS",
    "document_type": "DOCUMENT_TYPE",
    "issue_date": "ISSUE_DATE",
    "expiration_date": "EXPIRATION_DATE"
  }
}
```

La réponse contient les champs suivants :

* data (tableau) : Un tableau contenant un objet représentant les résultats de l'OCR. Les champs de cet objet comprennent :
  * http_code (entier) : Le code HTTP indiquant le statut de la requête. Une valeur de 200 indique une requête réussie, tandis que 204 indique que le document scanné n'est pas une carte d'identité valide ou qu'il est illisible.
  * ocr_text (objet) : Un objet contenant les informations extraites du processus OCR. Les champs de cet objet comprennent :
    * document_id (chaîne de caractères) : L'identifiant du document.
    * first_name (chaîne de caractères) : Le prénom du titulaire du document.
    * last_name (chaîne de caractères) : Le nom de famille du titulaire du document.
    * date_of_birth (chaîne de caractères) : La date de naissance du titulaire du document.
    * place_of_birth (chaîne de caractères) : Le lieu de naissance du titulaire du document.
    * father_name (chaîne de caractères) : Le nom du père du titulaire du document.
    * mother_name (chaîne de caractères) : Le nom de la mère du titulaire du document.
    * profession (chaîne de caractères) : La profession ou l'occupation du titulaire du document.
    * address (chaîne de caractères) : L'adresse du titulaire du document.
    * document_type (chaîne de caractères) : Le type du document (par exemple, CNI, passeport, carte de résidence, etc.).
    * issue_date (chaîne de caractères) : La date de délivrance du document.
    * expiration_date (chaîne de caractères) : La date d'expiration du document.

Veuillez noter que si le code_http est 204, ce qui indique une requête non réussie, les valeurs de l'objet texte_ocr seront vides.


Voici un exemple de réponse JSON avec un code HTTP 200 :

# Contact

N'hésitez pas à nous contacter si vous avez des questions ou des commentaires.

Mail : abokor.ahmed.kadar.nour@outlook.com
