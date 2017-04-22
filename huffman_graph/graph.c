#include "graph.h"
#include <stdlib.h>             /* itoa */

const char *printchar(char in){
  char* res = (char *) malloc(sizeof(char) * 10);
  if (in=='"')
    strcat(res,"''");
  else if (in=='\n')
    strcat(res, "\n");
  else if (in=='<')
    strcat(res, "\\<");
  else if (in=='>')
    strcat(res, "\\>");
  else if (in=='{')
    strcat(res, "\\{");
  else if (in=='}')
    strcat(res, "\\}");
  else{
    res[0]=in;
    res[1]='\0';
  }
  return res;
}

void draw(const int nbChar, const huffnode node[nbChar*2], char* dico[256]){
  printf("digraph G{\n");
  printf("\tnode [shape=record]\n");
  for (int i=0; i<nbChar*2-1; i++){
    /* déclaration des sommets */
    if ( i < nbChar){
      /* feuille */
      printf("\t%d [label=\"{%s| %s}\"];\n", i , printchar(node[i].letter), dico[node[i].letter]);
    }
    else{
      /* noeud de rattachement*/
      printf("\t%d [label=\"%llu\"][shape=oval];\n", i, node[i].probability);
      /* écriture des fils */
      printf("\t%d -> %ld [label=\"0\"];\n", i, node[i].left - &node[0]);
      printf("\t%d -> %ld [label=\"1\"];\n", i, node[i].right - &node[0]);
    }
  }
  printf("}");
}

int graph(const char* pathinput){
  FILE *fi;
  char* dico[256];
  occurence occ[256];
  unsigned int nbChar;

  fi = fopen(pathinput, "rb");
  if (fi==NULL){
    fprintf(stderr, "Couldn't open %s.\n", pathinput);
    return 1;
  }
  nbChar = readOccurence(&occ, fi);
  if (nbChar==0){
    fprintf(stderr, "No bytes to read.\n");
    return 1;
  }

  for(int i=0; i<256; i++){ dico[i] = NULL; }
  huffnode node[nbChar*2];
  hufftree *tree = &node[nbChar*2-2];
  sort(&occ);
  makeHuffmanTree(nbChar, &node, occ);
  genCode(tree, dico, "");

  draw(nbChar, node, dico);
  
  for (int i=0; i<nbChar*2-2; i++){
    free(node[i].code);
    if (dico[i]!=NULL) { free(dico[i]); }
  }
  fclose(fi);
  return 0;
}
