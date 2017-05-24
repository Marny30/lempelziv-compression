Comparateur
===========
Comment fonctionne-t-il ?
--------------------------
Fonctionnement du comparateur
Le script principal comp.sh genere la base du code latex
le script comp.py utilise une expression regulière et un calcul pour donner le temps d'exécution en secondes
ce resultat est inclus dans le latex
les différents codes sont coupés avec la fonction split, puis compilés en pdf
les pdf sont assemble avec le programe pdftk
les fichier temporaires sont supprimés
Comment compiler?
-------------------------
il s'exécute avec `make` et compare le contenu du dossier 'projet'
pour le moment, la comparaison se base sur la durée d'exécution, le taux de comparaison est en cours d'implémentation
