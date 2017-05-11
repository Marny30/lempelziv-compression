#pragma once

typedef struct occurence{
  unsigned char letter;
  unsigned long long probability;
} occurence;

typedef struct huffnode{
  unsigned char letter;
  unsigned long long probability;
  char* code;
  struct huffnode* left;               /* 0 */
  struct huffnode* right;              /* 1 */
} huffnode;

typedef huffnode hufftree;

