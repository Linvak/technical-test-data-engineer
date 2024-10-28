# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

_Inscrire la documentation technique_
Le code est réparti en 4 : 
API
Va gérer les appels APIs (pour l'instant simple sans headers) pour récupérer les données. 
db
Gère l'intéraction avec la database. Cette partie m'a posé plus de problèmes que souhaité du fait de la volonté d'ajouter un système de metadata (permettant d'enregistrer les dernières valeurs d'éxecution du script), un système de valid_until pour garder les modifications éventuelles et permettre de récupérer des données dans le temps, et un champ d'ingestion, champs pénibles à simuler avec une base de données csv / pandas dataframe.
etl
Orchestre la récupération des données, le filtre par rapport aux données déjà récupérées, et une validation sommaire du schéma lors de la récupération pour éviter l'ajout de données corrompues en base.
main
Le fichier comprend l'itération sur les 3 apis/tables finales de destination
## Questions (étapes 4 à 7)

### Étape 4

Je ne suis pas sûr de comprendre la question, mais une base de données SQL peut très bien fonctionner pour ce cas. Surtout si le ML va avoir besoin de features applaties, travailler avec le SQL facilitera les prétraitements. De plus, nous pourrons éclater le champ items a l'aide de la clé étrangère présent dans les items qui correspond aux tracks, et ajouter les features qui nous serons demandées à l'aide d'une jointure.
Le schema pourrait donc ressembler à :

user_id,user.favorite_genres, user.gender, track.name, track.artist, track.genres, track.albim, track.songwriters, track.duration,created_at,updated_at,ingested_at,valid_until


### Étape 5
5. Le client exprime le besoin de suivre la santé du pipeline de données dans son exécution quotidienne. Expliquez votre méthode de surveillance à ce sujet et les métriques clés.

Je ne suis pas allé au bout du logging dans mon code, mais il sera important de surveiller les warnings lors de l'éxecution quotidienne du script. Si possible, nous ajouterons également de l'alerting sur les erreurs remontées par le logging.
La mise en place des metadata permettra rapidement de vérifier la bonne exécution du script car celles-ci sauvegarderont les dates d'éxecution des scripts
Nous pourrons également vérifier le temps d'éxecution du script. La mise en place de filtres sera importante si le volume de donnée augmente. De la même manière, la gestion simpliste de la base avec le chargement en mémoire pour modifier les dataframes pandas devra être revu si le volume de données devient par trop important

   Félicitations, à ce stade les données sont ingérées quotidiennement grâce à votre pipeline de données! Les scientifiques de données sollicitent votre collaboration pour la mise en place de l’architecture du système de recommandation. Votre expertise est sollicitée pour automatiser le calcul des recommandations et pour automatiser le réentrainement du modèle.





### Étape 6
6. Dessinez et/ou expliquez comment vous procèderiez pour automatiser le calcul des recommandations.

Une fois le modèle entraîné en place, il faudra mettre en place l'inférence. Nous pourrons déployer ce modèle sur un endpoint. Il s'agira alors de créer une transformation de données rapide pour permettre l'appel API vers notre modèle à l'aide des donnes d'un seul utilisateur. Le volume de donnée pour un utilisateur de vrai permettre d'envoyer toutes les données sans problèmes pour l'inférence. Si nous avons un utilisateur avec un trop grand nombre d'écoute, il sera possible de garder que les X derniers mois / derniers points. L'inférence renvoyée pourra être utilisée directement pour les chansons en suggestion aléatoire, ou sous la forme de playlists stockées en base pour des playlists suggérées à l'utilisateur.

### Étape 7
7. Dessinez et/ou expliquez comment vous procèderiez pour automatiser le réentrainement du modèle de recommandation.

Une fois que les features engineering et les résultats du modèle sont satisfaisants, afin de permettre le réentrainement du modèle, il est important de continuer d'extraire les données. Des données récentes (nouvelles chansons, nouvelles habitudes) permettront d'améliorer le modèle.

Il sera alors important de créer une pipeline pour entrainer périodiquement le modèle (1 semaine/ 1 mois), et d'automatiser le process de déploiement de l'endpoint d'inférence. Cependant, une étape critique est de vérifier les résultats du modèle avant tout redéploiement, car un changement dans la structure de la donnée pourrait impacter négativement celui-ci.
Cette vérification de performance peut également être automatisé à l'aide du développement de pipeliens de déploiement (Cloud / MLFlow).


