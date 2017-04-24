lz78explained.py
================
Implémentation de LZ78. Étapes de compression pas à pas.

Fonctionnement
----------------
1. Données brutes -> Codage de Lempel Ziv (couple *référence, lettre*)
2. Codage LZ -> Codage Binaire pour stockage avec *taille variable*
   inférieure à l'octet des référence pour gain d'espace
3. Codage Binaire -> Décodage

trie.py
=========
Génère une représentation en trie du dictionnaire généré par le codage
de lz78.  Envoi la sortie dans le fichier tmp.gv. On s'est basé sur le
fait que le code de Lempel Ziv était similaire à un *Trie*

Comment l'utiliser?
-----------------------
Faire `trie.py -h`

Fonctionnement
-----------------
1. Génération du code (sous forme de couples) d'un texte
2. Lecture progressive de ce dernier et écriture des noeuds et arêtes
   en code *dot*
3. Interprétation de ce code par les outils standards *graphviz* pour
   traduction en postscript par la commande suivante :
```shell
dot -Tps FILE.gv > FILE2.ps
```
