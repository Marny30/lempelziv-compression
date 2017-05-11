#pragma once
#include "common.h"
#include <stdio.h>
#include <string.h>             /* strcat */
#include <stdlib.h>             /* exit, realloc, malloc */

int compressMain(const char*);
int readOccurence(occurence (*occ)[256], FILE* file); /* returns number
                                                        of char */
void codeToDict(const int nbChar, huffnode (*tree)[nbChar*2-1],
                occurence*);
void sort(occurence (*res)[256]);
void makeHuffmanTree(const int nbChar, huffnode (*tree)[nbChar*2-1],
                     const occurence occ[256]);
void compress(FILE*, FILE*,
              FILE*, char *dico[256], const int nbChar);
void genCode(huffnode*, char* dico[256], const char* parentCode);
