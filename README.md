# Intro

Ce projet gitlab va servir de point de départ pour la remise du projet de fouille de données. Il suffit de le **cloner** sur votre compte gitlab (en tant que projet privé auquel il faudra inviter Roland pour qu'il puisse y accéder) pour récupérer la structure de base et au fur et à mesure y ajouter les scripts de préparation des données pour obtenir matrice individus-variables qui servira pour l'analyse, et ensuite l'analyse, et enfin le rapport.


Il y a donc quelques répertoires qu'il vous faudra utiliser et compléter :

- data.preparation: il va contenir un sous-répertoire avec les scripts (R, python, bash, ...) permettant, à partir des fichiers de données fournis, d'obtenir la matrice pour l'analyse de fouille de données. Il doit contenir aussi la documentation utilisateur qui indiquera comment configurer et utiliser les scripts pour obtenir la matrice.

- analysis: ce répertoire contiendra les scripts (R, python, ...) et/ou workflows (Knime, ...) ayant servi à l'analyse de la matrice de données et l'évaluation des performances.

- rapport: ce répertoire contiendra le rapport qui sera au format Markdown. Ainsi, il sera possible de le visualiser et de l'éditer directement sur gitlab ou bien localement tout en permettant un suivi des modifications et un travail collaboratif.

- data: ce répertoire contient en théorie les fichiers CSV fournis mais **il ne faut pas** concrètement les mettre sur gitlab (ni autre média) puisque tout le monde les a déjà. En paramétrant git, cela permet de les avoir en local, avec les mêmes chemins et les mêmes noms, sans avoir à les mettre sur gitlab, et ainsi, les scripts de préparation des données devraient fonctionner plus facilement.


# Calendrier 2019-20

- **19/05/2020** Matrice de données *individus-variables* à fournir avec les scripts et la documentation utilisateur pour l'obtenir (cf. répertoire data.preparation).
- **10/06/2020** Fin du projet: Roland récupérera les dépôts de chaque projet pour évaluation (notamment les répertoires analysis et rapport).
