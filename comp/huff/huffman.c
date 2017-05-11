#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct noeud{
  unsigned long long int o;
  int pere,fg,fd;
}NOEUD;


unsigned long long int GetFileSize(char* fichier){
  unsigned long long int fTaille=0;
  FILE* fd;
  fd=fopen(fichier,"r");
  fseek(fd,0L,SEEK_END);
  fTaille=ftell(fd);
  fseek(fd,0L,SEEK_SET);
  fclose(fd);
  return fTaille;
}

void afficheTab(NOEUD *arbre)
{ 
  //printf("lettres\n");
  for(int i=0;i<=255;i++)
    {
      if(arbre[i].o!=0) printf("%i %c %Lu %i %i %i\n",i,i, arbre[i].o,arbre[i].pere,arbre[i].fg,arbre[i].fd);

    }

  //printf("noeud\n");
  for(int i=256;i<=511;i++)
    {
      if(arbre[i].o!=0)
	printf("%i %Lu %i %i %i\n",i,arbre[i].o,arbre[i].pere,arbre[i].fg,arbre[i].fd);
     
    }

  
}

unsigned long long int* calculOccurences (char* fichier,unsigned long long int *nbCar)
{
  unsigned long long int* occurence=malloc(256*sizeof(unsigned long long int)); //création d'un tableau de 256 float, pour chaque caractère ASCII
  int i=0;
  //unsigned long long int nbCar=0; //compteur de caractères totaux
 
  unsigned long long int occurenTot = 0;
  for(i=0;i<256;i++)
    occurence[i]=0; //initialisation de chaque case du tableau a 0

  FILE* fd;
  if((fd=fopen(fichier,"r"))!=NULL)
    {
      unsigned char c;
      /*
	lecture caractère par caractère, incrémentation de la case qui correspond et du nb total
      */

      unsigned long long int posC;
      posC=ftell(fd);
      unsigned long long int fTaille=GetFileSize(fichier);
      while(posC<fTaille)
	{
	  fread(&c,1,1,fd);
	  posC=ftell(fd);
	  occurence[c]++;
	  nbCar[0]++;
	  // printf("%c \n", c);
	}

      printf("effectif total=%Li\n",*nbCar);
      for(i=0;i<256;i++)
	if(occurence[i]!=0)
	  {occurenTot+=occurence[i];
	    //printf("%i %f",i)
	    // printf("")
	  }

      
      printf ("occurrences totales dans calculOccurrences=%Li\n",occurenTot);
   
      fclose(fd);    
      return occurence;
    }
  else{printf("Erreur d'ouverture\n");
    exit(1);}
}



void rechercheMins(int *ind,NOEUD* arbre,unsigned int racine,unsigned long long int* Mins,unsigned long long int *nbCar)
{
  //int *ind=malloc(2*sizeof(int));
  ind[0]=0;
  ind[1]=1;
  Mins[0]=nbCar[0];
  Mins[1]=nbCar[0];
  int i;
  for(i=0;i<512;i++)
    {
      if((arbre[i].o!=0)&&(arbre[i].o<=Mins[0])&&(arbre[i].pere==-1))
	{
	  Mins[1]=Mins[0];
	  Mins[0]=arbre[i].o;
	  ind[1]=ind[0];
	  ind[0]=i;
	  // printf("a l'indice i : %i",i );
	  // printf(" la fréquence est :%f\n",arbre[i].f);
	}
    
      else if((arbre[i].o!=0)&&(arbre[i].o>Mins[0])&&(arbre[i].o<=Mins[1])&&(arbre[i].pere==-1))
	{ 
	  Mins[1]=arbre[i].o;
	  ind[1]=i;
	}
    }
 

  //return ind;
}


int constArbre(unsigned long long int * tab,unsigned long long int *nbCar,NOEUD* arbre)
{
  /*
    Calcul du nombre de caractères différents
  
   */
  
  int nbCarDiff=0;
  for(int k=0;k<256;k++)
    {
      if(tab[k]!=0)
	{
	  nbCarDiff++;
	}
    }
  
 
  
  int *ind=malloc(2*sizeof(int));
  unsigned long long int *Tabmin=malloc(2*sizeof(unsigned long long int));
  Tabmin[0]=0;
  Tabmin[1]=0;
  unsigned long long int Mins[2];
  unsigned int i;
  unsigned int racine=256;

  for(i=0;i<256;i++)
    {
      arbre[i].o=tab[i];
      arbre[i].fg=-1;
      arbre[i].fd=-1;
      arbre[i].pere=-1;
    }
  
  for(i=256;i<512;i++)
    {
      printf("acce a a ligne %i  ",i );
      arbre[i].o=0;
      arbre[i].fd=-1;
      arbre[i].fg=-1;
      arbre[i].pere=-1;
    }
  
  if(nbCarDiff==1)
    {
      int indRech=0;
      while(arbre[indRech].o==0)
	{
	  indRech++;
	}
      racine=indRech+1;
      printf("Et la racine est %i ",racine);
    }
  else{
  
  while((arbre[ind[0]].o+arbre[ind[1]].o)<nbCar[0])
    {
      
      rechercheMins(ind,arbre,racine,Mins,nbCar);
      
      /*for (int i=0;i<2;i++)
	{
	Tabmin[i]=ind[i];
	}
	//printf("Tabmin= %i %i\n",Tabmin[0],Tabmin[1]);
	*/

      arbre[racine].fd=ind[0];
      arbre[racine].fg=ind[1];
      arbre[racine].o=arbre[ind[0]].o+arbre[ind[1]].o;
      arbre[ind[0]].pere=racine;
      arbre[ind[1]].pere=racine; 
      racine++;
     
     
      //printf("racine : %i\n",racine );
      //printf("%i %i\n",Tabmin[0],Tabmin[1]);

    }

  }
    
  free(Tabmin);
  free(ind);
  return racine;

}



void ConstruireSuiteBin(NOEUD *arbre,int num_noeud,char* suite,char** TableCar)
{  
  char suiteD[256];
  char suiteG[256];
  for(int i=0;i<256;i++){
    suiteG[i]=suiteD[i]=suite[i];
    
  }
  if(arbre[num_noeud].fg==-1)
    { 
      strcat(TableCar[num_noeud],suite);

    }
  
  else{
    ConstruireSuiteBin(arbre,arbre[num_noeud].fd,strcat(suiteD,"1"),TableCar);
    ConstruireSuiteBin(arbre,arbre[num_noeud].fg,strcat(suiteG,"0"),TableCar);
    
    
  }
}




void afficheCodeBin(char** TableCar, unsigned int ni)
{
  int i=0;
  while(TableCar[ni][i]!='\0')
    {
      printf("%c",TableCar[ni][i]);
      i++;
    }
}

char* retourneCodeBin(char** TableCar, unsigned int ni, char* retour)
{
  retour[0]='a';
  int nbCh=1;
  int i=0;

  //printf("ni = %i\n",ni);
  unsigned char ini=ni;
  //printf("ini =  %i\n",ini);
  while(TableCar[ini][i]!='\0')
    {
      retour[i]=TableCar[ini][i];
      retour=realloc(retour,nbCh*sizeof(char));
      i++;
      nbCh++;
      retour[i-1]=TableCar[ini][i-1];
      retour[i]='\0';
    }
  if(retour[0]=='a')
    retour[0]='\0';
  //printf("J'ai le code binaire de %c c est %s\n",ni,retour);
  return retour;
}

void EcrireEnTete(unsigned long long int* occurenTot, unsigned long long int compteur,  char* fichier, char* NomFiComp){
    
  char* EnTete=malloc(10*sizeof(char));
  
  for(int i=0;i<10;i++){
    EnTete[i]='\0';
  }
  EnTete=strcat(EnTete,"%HUF-1.0.%");
  
  unsigned long long int* EnTeteSuite=malloc(2*sizeof(unsigned long long int));
  EnTeteSuite[0]=occurenTot[0];
  EnTeteSuite[1]=compteur;
  

  
  FILE* fichierComp;  
  fichierComp=fopen(NomFiComp,"wb");
  fwrite(EnTete,10,1,fichierComp);
  fwrite(&EnTeteSuite[0],sizeof(unsigned long long int),1,fichierComp);
  fwrite(&EnTeteSuite[1],sizeof(unsigned long long int),1,fichierComp);
 
  free(EnTete); 
  free(EnTeteSuite);
  fclose(fichierComp);  
}


void inserDico(char **TableCar,char *fichier, char* NomFiComp)
{char deuxP=':';
 int j=0;
 FILE* fichierComp;
 fichierComp=fopen(NomFiComp,"a+b");
 
 for(int i=0;i<512;i++)
 {
  if(TableCar[i][0]!='\0')
  {
    fwrite (&i,1,1,fichierComp);
    while((TableCar[i][j]!='\0')&&(j<512))
    {
      fwrite(&TableCar[i][j],1,1,fichierComp);
      j++;
    }
    j=0;
    fwrite(&deuxP,1,1,fichierComp);
  }
 
 } 
 fclose(fichierComp);
 

}


void ecrireFichierComp(char* fichier,char**TableCar,char* NomFiComp)
{  
  char* buffer=malloc(264*sizeof(char));
  for(int i=0;i<264;i++)
    {
      buffer[i]='\0';
    }
 
  int nbBitBuffer=0;
  int car;
  int i;
  FILE* fichier_or;
  fichier_or=fopen(fichier,"r");
  FILE* fichierCompData;
  
    
  fichierCompData=fopen(NomFiComp,"a+b");
  char* retour1=malloc(sizeof(char));
  char* retour2=malloc(sizeof(char));
  char lettre;


  unsigned char c;
  unsigned long long int posC;
  posC=ftell(fichier_or);
  unsigned long long int fTaille=GetFileSize(fichier);
  while(posC<fTaille)
    {
      fread(&c,1,1,fichier_or);
      posC=ftell(fichier_or);
      
      strcpy(retour2,retourneCodeBin(TableCar,c,retour1));
      // strcpy(retour1,retour2);
      strcat(buffer,retour2);
      i=0;
      while(retour2[i]!='\0')
	{
	  i++;
	  nbBitBuffer++;
	}
      //c=fgetc(fichier_or);
      if(nbBitBuffer>7)
	{
            
	  car=0;
	  for(int i=0;i<8;i++)
	    {
	      car*=2;
	      car+=(buffer[i]-48);//equivalent atoi
	      //printf("--> %c",car);
	
	    }
	  //printf("Le caractère obtenu est donc %i \n",car);
      
	  lettre=car;
	  fwrite(&lettre,1,1,fichierCompData);
	  i=0;
     
       
	  while(buffer[i+8]!='\0')
	    {
	      buffer[i]=buffer[i+8];
	      i++;
	    }
	  nbBitBuffer-=8;
	  for(int j=0;j<8;j++)
	    {
	      buffer[i]='\0';
	      i++;
	    }
      
	}
    
     
     
    }
  
  if((posC==fTaille)&&(nbBitBuffer<8))
    {
      //printf("Ecriture de la dernière lettre");
      //int diff;
      //diff=8-nbBitBuffer;
      for(int i=0;i<8;i++)
	{
	  if(buffer[i]=='\0')
	    buffer[i]='0';
	    }


    
      car=0;
      for(int i=0;i<8;i++)
	{
	  car*=2;
	  car+=(buffer[i]-48);//equivalent atoi
	  //printf("--> %c",car);
      
	}
      lettre=car;
      fwrite(&lettre,1,1,fichierCompData);

   
      }

  fclose(fichierCompData);
  free(retour2);
  free(retour1);

}

unsigned long long int stats(NOEUD* arbre)
{unsigned long long int cpt=0;
  unsigned long long int occTot=0;
  for(int j=0;j<512;j++)
    {
    
   
      if(j<256)
	{ if(arbre[j].o!=0)
	    {cpt++;}

	  printf("%c ",j);
	}
      else if(j>256)
	{printf(" ");}
  
  printf(" %i %Lu %i %i %i \n",j,arbre[j].o,arbre[j].fg,arbre[j].fd,arbre[j].pere);
}



  for(int j=0;j<256;j++)
    {occTot+=arbre[j].o;}
  
  printf("occurence total =%Lu\n",occTot);
  printf("cpt : %Lu \n",cpt);

  return cpt;
}



int main(int argc, char** argv)
{ unsigned long long int *nbCar=malloc(1*sizeof(unsigned long long int));

  unsigned long long int* occu=calculOccurences(argv[1],nbCar);
  NOEUD arbre[512];
  int racine=constArbre(occu,nbCar,arbre);

  racine --;
  
  //afficheTab(arbre);
  //printf("La racine est %d\n",racine);
  unsigned long long int NbCarDiff=stats(arbre);
  if(NbCarDiff!=1){
  
    char** TableCar=malloc(512*sizeof(char*));
    for (int i=0;i<512;i++)
      {TableCar[i]=malloc(512*sizeof(char));}
  
    for(int i=0;i<512;i++)
      {
      
     
	for(int j=0;j<512;j++)
	  {
	    TableCar[i][j]='\0';
	  }
      }
  
    char* suite=malloc(512*sizeof(char));
    for(int i=0;i<512;i++)
      {
	suite[i]='\0';
      }

     
    ConstruireSuiteBin(arbre,racine,suite,TableCar);
	 
    EcrireEnTete(nbCar,stats(arbre),argv[1],argv[2]);
    
    inserDico(TableCar,argv[1],argv[2]);
    
    ecrireFichierComp(argv[1],TableCar,argv[2]);
    
  
    printf("La racine est %i\n",racine);
  }
  else
    {

      char LaLettre;
      int i=1;
      while(arbre[i].o==0)
	i++;
      LaLettre=i;
      EcrireEnTete(nbCar,stats(arbre),argv[1],argv[2]);
      printf("La lettre unique est %c\n", LaLettre);
      FILE* fichierComp;
      fichierComp=fopen(argv[2],"a");
      char* dico=malloc(3*sizeof(char));
      dico[0]=LaLettre;
      dico[1]='0';
      dico[2]=':';
      printf("Le dico est %s",dico);
      fwrite(dico,3,1,fichierComp);
      char FF=0;
      unsigned long long int nbOctet=*nbCar/8;
      for(int i=0;i<nbOctet+1;i++)
	fwrite(&FF,1,1,fichierComp);
    }


  return 0;
}
