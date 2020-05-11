# Intro

Ce projet gitlab va servir de point de départ pour la remise du projet de fouille de données. Il suffit depuis votre compte gitlab de créer un projet à partir de ce dépôt pour récupérer la structure de base et au fur et à mesure y ajouter les scripts de préparation des données pour obtenir matrice individus-variables qui servira pour l'analyse, et ensuite l'analyse, et enfin le rapport.


Il y a donc quelques répertoires qu'il vous faudra utiliser et compléter :

- data.preparation: il va contenir un sous-répertoire avec les scripts (R, python, bash, ...) permettant, à partir des fichiers de données fournis, d'obtenir la matrice pour l'analyse de fouille de données. Il doit contenir aussi la documentation utilisateur qui indiquera comment configurer et utiliser les scripts pour obtenir la matrice.

- analysis: ce répertoire contiendra les scripts (R, python, ...) et/ou workflows (Knime, ...) ayant servi à l'analyse de la matrice de données et l'évaluation des performances.

- rapport: ce répertoire contiendra le rapport qui sera au format Markdown. Ainsi, il sera possible de le visualiser et de l'éditer directement sur gitlab ou bien localement tout en permettant un suivi des modifications et un travail collaboratif.

- data: ce répertoire contient en théorie les fichiers CSV fournis mais **il ne faut pas** concrètement les mettre sur gitlab (ni autre média) puisque tout le monde les a déjà. En paramétrant git, cela permet de les avoir en local, avec les mêmes chemins et les mêmes noms, sans avoir à les mettre sur gitlab, et ainsi, les scripts de préparation des données devraient fonctionner plus facilement.


# Calendrier 2019-20

- **19/05/2020** Matrice de données *individus-variables* à fournir avec les scripts et la documentation utilisateur pour l'obtenir (cf. répertoire data.preparation).
- **10/06/2020** Fin du projet: Roland récupérera les dépôts de chaque projet pour évaluation (notamment les répertoires analysis et rapport).

# Première étape : compte gitlab et clonage du projet

La première étape pour vous va donc être de créer un compte gitlab si vous n'en avez pas. Et ensuite, de cloner ce projet et d'inviter l'autre membre de votre groupe pour le projet afin d'avoir un seul et même projet par groupe.

Une fois que vous aurez un compte, pour importer ce projet dans votre compte :

- Faire *New project*
- Dans l'onglet *Import project* choisir *Repo by URL*
- Mettre l'URL : https://gitlab.com/rbarriot/datamining.abc.git et renseigner le *Project name*

Gitlab va copier la totalité du projet et vous pourrez travailler sur votre propre copie.

# Remarques sur gitlab

- L'idée est de vous forcer à **utiliser git** pour, si ce n'est pas déjà le cas, vous familiariser avec le **suivi de versions** de scripts et autres. C'est particulièrement important lorsqu'on a une version qui fonctionne et que l'on cherche à modifier. Et c'est une **compétence demandée** dans le privé comme dans le public.
- En plus, cela va me permettre de suivre le niveau d'activité de votre projet et des contributions.
- Il est donc important pour chacun de vous d'utiliser git, gitlab et leurs fonctionnalités. Il ne s'agit surtout pas de cloner une fois le projet au début, puis de travailler uniquement sur votre copie, pour déposer toutes les modifications à la fin en une fois. Gitlab devrait **vous permettre de vous répartir certaines tâches** puis déposer et partager vos résultats avec l'autre membre de votre groupe. De même, pour la rédaction de la doc utilisateur et du rapport. Cela devrait vous permettre de vous répartir des parties à rédiger pour ensuite fusionner les documents produits chacun de votre côté.

# Liens

- sujet: http://silico.biotoul.fr/enseignement/m1/datamining/projet/sujet.html
- données: https://silico.biotoul.fr/enseignement/m1/datamining/projet/data/

