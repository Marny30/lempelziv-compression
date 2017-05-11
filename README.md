Introduction à Lempel Ziv
===============================
Auteurs : Guilhèm BLANCHARD, Marin JULIEN

Ce programme présente au travers d'une interface graphique le
fonctionnement des algorithmes de Lempel Ziv, qui reste la famille
d'algorithmes de compression de texte la plus efficace de nos
jours. Le projet se base sur plusieurs sous-programmes que nous avons
écrits.

Comment fonctionne le projet?
---------------------
Exécuter `main.py`. Les fichiers importants à l'utilisation du projet
sont pré-compilés mais recompilable. Le programme utilise tkinter pour
l'interface, et génère notamment des diapositives en postscript. On
renvoie aux détails sur `trie.py` plus loin dans ce fichier.

Dépendances
----------
Le projet utilise les outils système `graphviz` et `ghostscript`. Un
fichier `install-dep.sh` est fourni pour automatiser leur
installation.

Sur quels sous programmes se basent le projet?
-------------------------------------------
Nos sous programmes ont leurs propres readme respectifs pour leur
utilisation et compilation.

### arbre de huffman (C)
Se référer à `huffman/readme.md`

### Lempel ziv et trie (python)
Se référer à `lempelziv/readme.md`. Notamment, le programme lz78.py
permet notamment de compresser les fichiers (contrairement à
l'interface), avec les limites inhérentes à l'algorithme.

### Comparaison de compression (shell, python)
Se référer à `comp/readme.md`

Quels programmes externes utilisons nous?
--------------------------------
Au delà des dépendances décrites plus haut, nous utilisons pour nos
comparaisons les commandes shell `bzip2`, `xz`, `lzma`, `zip` que nous
n'avons pas codés.
