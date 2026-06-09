# Projet d'admin Google Workspace

## Avant propos

### Contexte

Ce projet a été initié par la demande de mon service de créer plusieurs structures google drive complexes (drives partagés avec nomenclature normalisée) dans le cadre de mon travail.

J'ai d'abord reagardé ce qui existait au niveau des APIs en python, mais j'ai constaté que l'api était pensée pour que l'on fasse presque exclusivement des requêtes aux serveurs de Google, ce qui peut parfois prendre beaucoup de temps selon les données auxquels on souhaite accéder.

### Objectif

L'idée du projet était donc de structurer les différents objets retournés par les appels des api en classes Python pour les rendre plus exploitables, et enregistrer une partie des données en cache pour gagner en temps d'exécution pour certains type recherche.

### Historique du projet

Les commits ne sont malheureusement pas disponibles publiquement car le projet était au départ privé et contenait des données propres à un domaine que je ne pouvais pas rendre publiques.


### Prérequis

- Avoir un compte et un domaine Google Cloud
- Avoir créé un projet
- Avoir activé dessus les APIs:
    - SDK (for gmail)
    - Drive
    - Python 3.12
    - Bibliothèque pickle
    - Bibliothèque google api client
- Avoir choisi par compte de service
- VSCode avec l'extension Pylance

Sinon, se référer à [la documentation de Google](https://developers.google.com/workspace/guides/create-project?hl=fr)



### Installation

--Sur votre envoronnement virtuel--

    git clone https://github.com/OlivierLesenfans/admin-google-public
    pip install --upgrade google-api-python-client

#### Paramétrage des clés:

1: Mettre le fichier json d'authentification dans le dossier **"cle"**, et le nommer **"key.json"**

2: Ajouter un fichier **"compte.py"** dans lequel vous définirez les variables suivantes

    COMPTE_PERSO = "mon-compte@unmail.com"
    COMPTE_ADMIN = "admin@unmail.com"

Une fois ces étapes réalisées, je vous conseille de créer un **.vscode/sttings.json** à la racine contenant:

    {
        "python.languageServer": "Pylance",
        "python.analysis.typeCheckingMode": "basic",
        "python.analysis.extraPaths": [
            "Drives",
            "fonctions_dates"
        ]
    }

### Utilisation

Pour utiliser la librairie et scripter des actions, vous n'aurez qu'à créer un fichier main à la racine, puis à lui donner l'en-tête suivant:

    from classes import *

Il faudra pour chaque classe commencer par la fonction maj, qui récupère les,données du Cloud et en fait un fichier structuré pickle, qu'elle stocke localement.


La **classe Service(s:str)** permet de définir des instances qui ouvrent une session avec les scopes correspondants aux opérations permises par le paramètre s:
- Pour des drives -> Service("d")
- Pour des groupes -> Service("g")
- Pour des utilisateurs -> Service("u")

Voici un exemple d'un script permettant d'afficher les Drives Par de votre domaine:

    #main.py


    from classes import *




    def main():

        su = Service("d")

        listeDrives = ListeDrivePartages(su) 

        listeDrives.load() #Attention, nécessite que vous ayez appelé la fonction maj au moins une fois
        

        print(listeDrives)
        
        return 0

    main()

### idées futures

-Mettre en place une mise à jour intelligente de la base pour charger que ce qui a été modifié, et pas l'entièreté de la base à chaque fois

-Un système de logs avec des dossier qui traçent l'exécution de scripts

-Appliquer le même système que l'on a utilisé jusque là mais pour les dossiers, et voir dans quelle mesure cela serait pertienent

-Mettre un algo en place de suggestion des valeurs recherchées à partir du début d'un mot (ce qui pourrait aider pour la recherche).
