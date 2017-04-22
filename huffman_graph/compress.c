#include "compress.h"

#define INDEX_EOF 256

int compressMain(const char* pathinput){
  FILE *fi, *fo, *fodict;
  char* dico[256];
  occurence occ[256];
  char foPath[2048], fodictPath[2048];
  unsigned int nbChar;

  fi = fopen(pathinput, "rb");
  if (fi==NULL){
    fprintf(stderr, "Couldn't open %s.\n", pathinput);
    return 1;
  }
  strcpy(foPath, pathinput);
  strcpy(fodictPath, pathinput);
  strcat(foPath, ".huf");
  strcat(fodictPath, ".hufdict");
  fo = fopen(foPath, "wb");
  fodict = fopen(fodictPath, "w");
  if (fo==NULL || fodict==NULL){
    fprintf(stderr, "Couldn't create output file.\n");
    return 1;
  }  
  nbChar = readOccurence(&occ, fi);
  if (nbChar==0){
    fprintf(stderr, "No bytes to read.\n");
    return 1;
  }

  for(int i=0; i<256; i++){ dico[i] = NULL; }
  huffnode node[nbChar*2];
  hufftree *tree = &node[nbChar*2];
  sort(&occ);
  makeHuffmanTree(nbChar, &node, occ);
  genCode(tree, dico, "");
  compress(fi, fo, fodict, dico, nbChar);
  
  for (int i=0; i<nbChar*2-2; i++){
    free(node[i].code);
    if (dico[i]!=NULL) { free(dico[i]); }
  }
  fclose(fi);
  fclose(fo);
  fclose(fodict);
  return 0;
}

void sort(occurence (*res)[256]){
  /* Trier par occurence décroissante */
  unsigned long long min;
  unsigned long long auxllu;
  char auxchar;
  for (int i=0; i<256; i++){
    min = i;
    for (int j=i; j<256; j++){
      if ((*res)[j].probability < (*res)[min].probability
          ){
        min = j;
      }
    }
    auxllu = (*res)[i].probability;
    auxchar = (*res)[i].letter;
    (*res)[i].probability = (*res)[min].probability;
    (*res)[min].probability = auxllu;
    (*res)[i].letter = (*res)[min].letter;
    (*res)[min].letter = auxchar;
  }

}

int readOccurence(occurence (*res)[256], FILE* f){ 
  char aux;
  unsigned int nbChar = 0;
  /* init */ 
  for (int i=0; i<256; i++){
    (*res)[i].letter=i;
    (*res)[i].probability = 0;
  }
  /* parcours du fichier pour création table */
  while ((aux=fgetc(f)) != EOF){ /* 255 = EOF en unsigned */
    if (!(*res)[(unsigned char)aux].probability)
      nbChar++;
    (*res)[(unsigned char) aux].probability++;
  }
  return nbChar;
}

int getSmallestOrphanIndex(const int nbChar, hufftree (*tree)[nbChar*2], const int isOrphan[512], const int nbnode){
  int imin = 0;
  long long minproba = -1;
  for (int i=0; i<nbnode; i++){
    if (isOrphan[i]){
      if (minproba > (*tree)[i].probability){
        imin = i;
        minproba = (*tree)[i].probability;
      }
    }
  }
  return imin;
}

void makeHuffmanTree(const int nbChar, hufftree (*tree)[nbChar*2], const occurence occ[256]){
  int offsetOcc = 256-nbChar;         /* sert à parcourir occ */
  int isOrphan[512] = {0};
  int imin1, imin2;
  int nbnode = 0;
  
  /* construction des feuilles */
  for (int i=offsetOcc; i<256; i++){
    (*tree)[nbnode].letter = occ[i].letter;
    (*tree)[nbnode].probability = occ[i].probability;
    (*tree)[nbnode].left = NULL;
    (*tree)[nbnode].right = NULL;
    isOrphan[nbnode] = 1;
    nbnode++;
  }
  /* construction de l'arbre */
  while (nbnode!= nbChar*2-1){
    imin1 = getSmallestOrphanIndex(nbChar, tree, isOrphan, nbnode);
    isOrphan[imin1] = 0;
    imin2 = getSmallestOrphanIndex(nbChar, tree, isOrphan, nbnode);
    isOrphan[imin2] = 0;

    (*tree)[nbnode].letter = 0;
    (*tree)[nbnode].probability = (*tree)[imin1].probability + (*tree)[imin2].probability;
    (*tree)[nbnode].left = &(*tree)[imin1];
    (*tree)[nbnode].right = &(*tree)[imin2];
    isOrphan[nbnode] = 1;
    nbnode++;
  }
}

void genCode(huffnode *tree, char* dico[256], const char* parentCode){
  if ((*tree).left == NULL){
    /* si feuille */
    dico[(*tree).letter] = (char*) malloc(strlen(parentCode)+1);
    strcat(dico[(*tree).letter], parentCode);
  }
  else {
    (*tree).left->code = (char*) malloc(strlen(parentCode)+1);
    if ((*tree).left->code == NULL){
      fprintf(stderr,"Couldn't allocate code.\n");
      exit(1);
    }
    strcat((*tree).left->code, parentCode);
    strcat((*tree).left->code, "0");
    genCode((*tree).left, dico, (*tree).left->code);
  
    (*tree).right->code = (char*) malloc(strlen(parentCode)+1);
    if ((*tree).right->code == NULL){
      fprintf(stderr,"Couldn't allocate code.\n");
      exit(1);
    }
    strcat((*tree).right->code, parentCode);
    strcat((*tree).right->code, "1");
    genCode((*tree).right, dico, (*tree).right->code);
  }
}

void compress(FILE* fi, FILE* fo, FILE* fodict, char* dico[256], const int nbChar){
  char aux;
  /* TODO */
  /* int bits = 0; */
  /* char byte=0; */
  size_t codelength[256];
  rewind(fi);
  /* écrire dictionnaire : LAST = HUFF EOF */
  for (int i=0; i<256; i++){
    if (dico[i]!=0){
      fprintf(fodict, "%c:%s\n", i, dico[i]);
      codelength[i] = strlen(dico[i]);
      /* printf("len %c : %d\n",i, strlen(dico[i])); */
    }
    else
      codelength[i] = 0;
  }
  /* écrire contenu */
  while ((aux=fgetc(fi)) != EOF){
    for (int i=0; i < codelength[(int) aux]; i++){
      printf("%c", dico[(int) aux][i]);
    }
    fprintf(fo,"%s", dico[(int) aux]);
  }
}
