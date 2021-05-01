---
title: "Rapport de Projet"
author: "Sophia Toffoli & Victoria Fathi"
output:
  html_document:
    code_folding: show
    toc: TRUE
    toc_float: TRUE
    toc_depth: 4
    theme: paper
    highlight: tango
editor_options: 
  chunk_output_type: console
---

# Contexte

Dans le cadre de l'UE Fouille de données, un jeu de données comportant des annotations sur des génomes Eucaryotes, Procaryotes et d'Archées nous a été fourni. Ce jeu de données appartient au de CBI de Toulouse et n'est donc pas disponible sur ce gitlab. 

L'objectif de ce projet est de mettre au point une méthode de classification des gènes impliqués dans les systèmes de transport ABC. 

![Transporteur ABC](transporteurs.png)

# Analyse

**Précisions sur les objectifs à atteindre et comment y arriver.**

  Pour répondre à cet objectif il faut tout d'abord réaliser la matrice d'individus-variables à partir de laquelle le classificateur sera entraîné. Par la suite, le classificateur sera testé et différentes mesures de la qualité de ce classificateur seront réalisées. A l'issu de la création de ce classificateur un certain nombres d'individus de classe inconnues pourront être classifié. 
  

- évaluer la qualité de la méthode: forêt aléatoire  <br>
- analyser l’arbre pour essayer d’en déduire les variables discriminantes  <br>
- utiliser l’arbre pour prédire les gènes annotés dont l’Identification_status = ‘pending’ ou null.  <br>


**Analyse préliminaire des données pour les appréhender ainsi que les méthodes disponibles pour atteindre les objectifs.**  <br>

*Un script d'intégration des données a été fourni par l'équipe CBI et a permis la création de la base de données suivante.*

![Schéma de la Base Données fourni par le CBI](database_schema.png)


<br>

  La méthode de classification repose sur le type de données en possession. Il est possible de se demander si les données sont qualitatives ou quantitatives, si elles sont comparables d'un individu à un autre ou encore si elles sont complètes.
  
  Ici les individus sont les gènes appartenant à l'ensemble des génomes présents dans la base. A chacun est associé un certain nombre de variables qualitatives et quantitatives. Puisque nous n'avons aucun a priori sur les données, la méthode doit pouvoir sélectionner les variables pertinentes pour la classification. Le choix se porte donc entre un arbre de décision ou une forêt aléatoire. 
  
-> finalement certaines sont tables sont à exclure soit parce qu'elles ne sont pas vraiment des variables (tax id etc) ou soit parce qu'elle comporte trop de catégories (à discuter)

# Conception

Fort de l'analyse précédente, présenter l'approche choisie et pourquoi. Quelle méthodologie allez-vous mettre en oeuvre pour les différentes étapes du projet avec quelles méthodes (par exemple : obtention de la matrice pour l'analyse, puis quelle méthode de classification et comment se fera l'évaluation). 

#### Quels individus choisir ?

Pour sélectionner les individus, nous nous sommes penchées sur la fiabilité des données puisque la qualité de la méthode de classification en dépend. Tout d'abord, les gènes non présents dans la table Protein n'appartiennent pas à un système ABC. Ensuite au sein des gènes de la table Protein, ils peuvent être identifiés comme appartenant à un système ABC avec l'attribut type. Enfin au sein de ces gènes de type 'ABC', l'attribut Identification_Status annoté l'état de l'attribution de la fonction. Celle-ci peut être "Pending", "Confirmed" ou "Rejected". <br> <br> 
Dans le cadre de la construction de la matrice d'individus-variables, seuls les gènes ayant un type 'ABC' 'Confirmed' ont recu la classe "ABC". Les gènes dont le statut est "pending" ou "null" sont mis "null" pour l'attribution de la classe et constitueront le jeu de données sur lequel sera utilisé le classificateur. Enfin, le reste des gènes sont classés 'non ABC'.


-> peut être petit tableau récapitulatif 


#### Quelles variables choisir ?

*Toutes les variables ne sont pas exploitables ou même pertinentes et peuvent donc être évincer sans que cela constitue un a priori sur les données.* revoir formulation



Pour chaque gène, nous récupérons ses domaines fonctionnels. 
Sur ces domaines conservés (jointure avec Conserved_Domain), nous récupérons le domaine fonctionnel auquel il correspond (jointure avec Functional_Domain), à partir duquel on extrait la famille de domaine correspondant à la première lettre du Family_Link.

Pour chaque gène, Pour chaque famille de domaine fonctionnel (MSD, NBS, SBP)  les domaines sont résumés par:

- le nombre de domaines fonctionnels de cette famille sur ce gène
- la e-value minimale
- la e-value maximale. 


Si cette famille est absente sur ce gène, la e_value est fixée à 10 000 (??) et le nombre de domaine à 0 pour la famille de domaine correspondante.


Notons qu’ici les e-values sont comparables puisque les résultats issus  de rps-blast utilise plusieurs bases de données concaténées pour sa recherche. L’espace de recherche est de même taille pour l’ensemble des requêtes. 


À cela s'ajoute une variable pour la taille du gène. Sa valeur est récupéré dans la table Gene à partir des attributs end et start.

Enfin une dernière variable correspondant à la e-value de l'alignement entre la séquence du gène et le gène auquel il a été identifié.

La matrice individu variable est résumé dans le tableau suivant: 


-> tableau de la matrice individus variables
le gene_size = | Gene.End - Gene.Start  + 1 | a mettre dans le tableau ?

#### Quelle méthode utilisée ?
Le choix s'est porté sur une forêt aléatoire puisque blabla




#### Quels outils ?

- mysql <br>
- python <br>
- mysql connector <br>
- scikit learn  <br>


# Réalisation

Mise en œuvre de ce qui a été conçu. Il s'agit là de préciser les paramètres et tous les détails concernant la réalisation concrète de l'analyse. Puis de décrire les résultats obtenus.

# Discussion

Analyse et discussion sur les résultats obtenus. 

Conclusion sur la qualité de la ou des méthodes mises en oeuvre.

# Bilan et perspectives

Qu'est-ce qui fonctionne ou pas. Piste d'amélioration. Recul sur l'ensemble du projet. Si c'était à refaire...

# Gestion du projet

Comment s’est organisé le groupe. Comment se sont déroulées les discussions, les prises de décisions. Comment se sont réparties les tâches. Quels ont été les rôles et les contributions de chacun·e. Diagramme de Gantt avec le calendrier et les tâches.
