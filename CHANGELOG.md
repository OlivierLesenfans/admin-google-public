## Mai 2026

Changement du projet en vue de la publication, donc adaptation pour enlever les appels à des données confidentielles


## Grande maj de Février

### Nouvel objectif

Après une demande d'un acteur ne faisant pas partie de l'orgnaisation d'être retiré de toutes les listes de diffusion, je me suis rendu compte que ce cas qui peut arriver assez souvent dans une organiastion est complexe à résoudre.

**En effet** la ressource <kbd>Member</kbd> de l'API ne dispose d'aucun lien entre le membre du groupe, et le groupe dont il est membre.

Ainsi, pour traiter ce simple cas, il faut d'abord parcourir tous les groupes du domaine, puis requêter les serveurs pour chacun d'eux. Dans notre cas, la requête prend 17 minutes. C'est bien entendu très long.

#### Résolution

J'ai pensé à mettre une partie du code en cache, afin de pouvoir faire des requêtes d'observation et d'audit sans attendre des années entre chaque exécution.

Le but du code est donc de stocker une partie des données localement avec <kbd>Pickle</kbd>.

Dans notre cas, on aura les Groupes du domaine, avec un champs Utilisateurs qui pointera vers les classes utilisateur stockées elles aussi en pickle.

En stockant le tout dans des fichiers pickle, on peut mettra à jour la base une fois, puis le chargement se fait en moins d'une seconde.

### 28 septembre

    Restructuration plus cohérente du projet.
    Tests de plusieurs manières de procéder pour avoir le code le plus lisible possible
    Supression de plusieurs classes inutiles (ex manageGroup...)

    **Reste à faire:**

    -Tests des créations de Dossiers
    -Migration si c'est possible des créations d'utilisateurs dans leur classe dédiée

    Et surtout: Restructuration des différentes requêtes que l'on fait sur la base, et qui ne renvoient que des .json imbriqués

### 24 novembre

    Pas mal avancé, mais reste à faire une requête pour les comptes à supprimer, puis
    faire la fonction de déploiement qui doit dorénavant couvrir le niveau 2...

### 30 novembre

    factorisation et optimisation du programme, pour qu'il ne calcule pas tous les services à chaque
    exécution.

    Il restera tout de même à demander l'ajout du scope pour les ressources

    Ajout du de la création des sous dossiers. A NOTER qu'il ne faut pas oublier que le fichier texte
    qui sert pour les titres doit comporter un saut de ligne à la fin pour bien réaliser les splits.

### 22 décembre

    ne pas oublier de mettre l'option useDomainAdminAccess pour faire des opérations sur l'esemble des drives

    Reste à optimiser le service en paramètre de chaque fonction, il pourrait être accéléré

### 18 Janvier

    Volonté de refondre le projet pour le rendre plus utile et lisible
    Plus de user_maker, tout est dans le constructeur de Cloud qui est désormais Service
    Moins de désordre dans les dossiers