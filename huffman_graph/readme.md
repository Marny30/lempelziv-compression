Huffman graph
======
Génération d'arbre de huffman pour un fichier donné.

Comment compiler?
-------------
Par usage du makefile, la commande est la suivante:  `make`

Comment l'utiliser?
------------
Faire `huffman -h`

Comment il fonctionne?
---------------
Génération d'un arbre DOTFILE correspondant à l'arbre de huffman du fichier
entré. Le dotfile est renvoyé dans la sortie standard. Il s'agit
ensuite de le transformer en graph avec l'outil `graphviz`.
