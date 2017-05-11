lz78.py
================

Implémentation de l'algorithme de compression LZ78.

Comment l'utiliser?
-----------------------
Faire `lz78.py -h` pour informations

trie.py
=========
Génère une représentation en trie du dictionnaire généré par le codage
de lz78. Envoi la sortie dans un fichier tmp.gv. On s'est basé sur le
fait que le code de Lempel Ziv était similaire à un *Trie*

Comment l'utiliser?
-----------------------
Faire `trie.py -h` pour informations

Fonctionnement
-----------------
1. Génération du code (sous forme de couples) de l'entrée
2. Lecture progressive de ce dernier et écriture des noeuds et arêtes
   en code **dot**
3. Interprétation de ce code par les outils standards *graphviz* pour
   traduction en **postscript** par la commande suivante :
```shell
dot -Tps FILE.gv > FILE2.ps
```
4. (si graphe "étape par étape") fusionnement des divers fichiers postscript
   par par l'outil *ghostscript*
5. suppression des fichiers auxiliaires
