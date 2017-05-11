#include "graph.h"
#include "compress.h"
#include "decompress.h"

void help(){
  printf("syntax:\n");
  printf("\thuffman OPTION PATH\n");
  printf("options:\n");
  printf("\t-c\tcompress file at PATH into PATH.huf and PATH.huf.dict\n");
  printf("\t-g\tbuild graph from file at PATH\n");
  printf("\t-d\tdecompress file at PATH\n");
}

int main(int argc, char* argv[]){
  if (argc<3){
    help();
    return 1;
  }

  if (!strcmp(argv[1],"-c")){
    compressMain(argv[2]);
    printf("ECRITURE BIT PAR BIT TODO");
  }
  else if (!strcmp(argv[1],"-g")){
    graph(argv[2]);
  }
  else if (!strcmp(argv[1],"-d")){
    printf("TODO");
  }
  else{
    help();
    return 1;
  }
  return 0;
}
