#pragma once
#include "common.h"
#include "compress.h"

#include <stdio.h>
#include <string.h>             /* strcat */

int graph(const char* pathinput);
void draw(const int nbChar, const huffnode node[nbChar*2], char* dico[256]);
const char *printchar(char in);
