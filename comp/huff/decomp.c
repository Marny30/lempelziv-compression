#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//void extraireDico()
/*for(int i=0;i<cpt;i++)
{
    

}
*/
void decale(char*buffer,int col)
{
  int i=0;
  int indFren;
  for (i;i<512;i++)
  {
    if ((buffer[i+col]!='\0')&&(i+col<512))
    {
     buffer[i]=buffer[i+col];
    }
   
    else if(buffer[i+col]=='\0')
    { indFren=i+col;
     for(i;i<=indFren;i++)
     {
        buffer[i]='\0';
     }
     break;
    }
    else if(i+col==512)
    {
     indFren=512;
     for(i;i<indFren;i++)
     {
       buffer[i]='\0';
     }
     break;
    }

  }
}



int compare(char* buffer, char** TabCar,char *fichierOriginal, unsigned long long int* CarE)
{
 int col=0;
 int lig=0;
 int trouve=0;
 int preLettreTrouv=0;
 /*printf("j'affiche Tab");
 for(int i=0;i<3;i++)
  printf("%c",buffer[i]);*/
  
 // printf("\n");
 while((trouve==0)&&(lig<512))
  {
   if(buffer[col]==TabCar[lig][col])
   { 
     col++;
     preLettreTrouv=1;
       // printf("%i et %i diff", buffer[col],TabCar[lig][col]);
    }

   else if(((col==511)||(TabCar[lig][col]=='\0'))&&(preLettreTrouv==1))
    {
      /////printf("Ok ");
      /////printf("lettre trouvée=%c lig=%i col=%i\n",lig,lig,col);
     preLettreTrouv=0;
     trouve=1;
     
       //écrire le caractère dans le fichier décompressé
     char* NomFichierDecomp=malloc(sizeof(char));
     strcpy(NomFichierDecomp,fichierOriginal);
     strcat(NomFichierDecomp,".decomp");
     //printf("On décompresse %s dans %s\n\n",fichierOriginal,NomFichierDecomp);
     FILE* fichierDecomp;
     if((fichierDecomp=fopen(NomFichierDecomp,"ab"))!=NULL)
      {
       //on peut écrire
       /////printf("J écris %i dans le fichier comme %c\n",lig,lig);
       /////printf("buffer dans compare : %s\n",buffer);
       fwrite(&lig,1,1,fichierDecomp);
       printf("%c",lig);
       (*CarE)++;

       //on ferme le fichier
       fclose(fichierDecomp);
      }
      else
      {
       //le fichier n'a pas pu etre ouvert
       printf("Impossible d'écrire le fichier décompressé");
       exit(3);
      }
    }
    
   else
    {
     //printf("%i et %i diff", buffer[col],TabCar[lig][col]);
     lig++;
     col=0;
     preLettreTrouv=0;
     }

     
      
      }
 /////printf("-->%s<-- \n",buffer);
 /////printf("ligFinal=%i colFinal=%i\n",lig,col);
 //if(lig==512&&col==0) return 8;
 return col;
}

void decodeOctet(unsigned char Octet, char* Tab)
{
 
 // Octet%=256;
  
  //printf("DEc  %i ",Octet);
  //printf("Hex  %#02x  ",Octet);
  for(int i=0;i<8;i++)
    {
      Tab[7-i]=(Octet%2)+48;
      Octet/=2;
    }
  /////printf("L'octet vaut donc %i",Octet);
    
  
  /* for(int i=0;i<8;i++)
     printf(" %i ",Tab[i]);*/
}


void afficheTabCar(char **TableCar)
{
  int j=0;
  for(int i=0;i<512;i++)
    {  
      if(TableCar[i][j]!='\0')
	{
	  /////printf("%i ",i);
	  while((TableCar[i][j]!='\0')&&(j<512))
	    {
	      /////printf("%c",TableCar[i][j]);
	      j++;
	    }
		
	  /////printf("\n");
	  j=0;
	}
    }
}

void recuperDico(char **TableCar,FILE* fichierComp,unsigned long long int cpt)
{
 int j=0;
 int pass;
 unsigned char c='\0';
 unsigned char preCharInt;
 /////printf("voici la suite c=");
 fread(&c,1,1,fichierComp); 
 for(int i=0;i<cpt;i++)
    {               //ON EXTRAIT LE PREMIER CARACTERE DE LA CHAINE QUI CORRESPOND AU CARATERE ASCI DU DICO
     preCharInt=c; //ON LE CONVERTIT EN ENTIER POUR STOCKER A L'INDICE C LA SUITE BINAIRE CORRESPONDANT AU CARACTERE
    
     pass=0; 
     while((c!=':')|(pass==0))
       {
	 pass++;
	 /////printf("%c",c);
	 fread(&c,1,1,fichierComp);
	 if(c!=':')
	   {
	     
	     TableCar[preCharInt][j]=c;
	   }
	 j++;
       } 
     /////printf("%c",c);//ON SAUTE LES ':' car ici c = ':'
     fread(&c,1,1,fichierComp);     
     
     j=0;  
    }
 /////printf("%c",c);printf(" <----dernier caractere");
 /////printf("\n");
} //LE CURSEUR SE SITUE DANS LA CARACTERE APRES LE DERNIER':'

void recuperSuite(FILE* fichierComp,unsigned long long int fTaille,char **TableCar,char *fichier, unsigned long long int* occurence, unsigned long long int* CarE)
{
  char *buffer=malloc(512*sizeof(char));
  memset(buffer,'\0',512);
  unsigned long long int posC;
  posC=ftell(fichierComp);
  int i=0;
  char* TabCode=malloc(8*sizeof(char));
  unsigned char c;
  unsigned int nbDecale=0;
  fseek(fichierComp,-2,SEEK_CUR);
  fread(&c,1,1,fichierComp);
  
  
  /////printf("j'affiche le premier caractère de fichierComp %c\n",c);
  /////printf("CarE=%Lu\n",*CarE);
  /////printf("occurence=%Lu\n",*occurence);
  while((*CarE)<(*occurence))
  { 
    /////printf("je boucle\n");
    
    if((512-i>=8)&&(posC<=fTaille)) //Cas où on remplit au maximum le buffer
    { 
      /////printf("1\n");
      fread(&c,1,1,fichierComp);  
      /////printf("c=%c\n",c);
      posC=ftell(fichierComp);        
      
      /////printf("je suis à la positionCurseur = %Lu\n",posC);
      /////printf("position total=%Lu\n",fTaille);
      
      decodeOctet(c,TabCode); //CONVERTIT LE CARACTERE EN UN TAB DE SUITE BINAIRE 
      /////printf("TabCode :%s\n",TabCode);
       
       
      strcat(buffer,TabCode);
      /////printf("buffer dans Recuper Suite%s\n =",buffer);
      i+=8;
      if(posC==fTaille)
        {posC++;}
    } 
      
    else if(i==512||512-i<8||posC>fTaille) //Cas où le buffer n'a pas de place ou cas où la place disponible modulo 8 != 0
      {     //printf("2\n");                 //ou la lecture du fichier est finie et que le buffer n'est ni rempli 
	     nbDecale=compare(buffer,TableCar,fichier,CarE);              //ni vide
       decale(buffer,nbDecale);           
       i-=nbDecale;
       //printf(" nbDecale=%i ",nbDecale);
       //printf("i=%i ",i);
       //printf("CarE=%Lu\n",*CarE);

      // compare (char* buffer, char** TabCar,char *fichierOriginal, unsigned long long int* CarE)
      }
    



    else 
    {
      printf("erreur\n");
      exit(1);
    }
  }
  //printf("je suis à la positionCurseur = %Lu\n",posC);
}

int main(int argc, char** argv)
{ //DECLARATION DU TABLEAU TABLECAR OU ON STOCKERA LE DICO EXTRAIT DU FICHIER

 

	unsigned long long int fTaille;
  
  char **TableCar=malloc(512*sizeof(char*));
  for(int i=0;i<512;i++)
  	{TableCar[i]=malloc(512*sizeof(char));}

  for(int i=0;i<512;i++)
    {
      for(int j=0;j<512;j++)
      {
        TableCar[i][j]='\0';
      }
    }

  FILE* fichierComp;
  unsigned long long int* cpt=malloc(sizeof(unsigned long long int));
  fichierComp=fopen(argv[1],"r");
  
  fseek(fichierComp,0L,SEEK_END); //on regarde la taille du fichier
 
  fTaille=ftell(fichierComp);
  fseek(fichierComp,0L,SEEK_SET);
  /////printf("la taille du fichier = %Li\n",fTaille);
     if(fichierComp!=NULL)
    {
     char* c=malloc(sizeof(char));
     
     fread(c,1,10,fichierComp);
     /////printf("La chaine est %s",c);
 
     if(strcmp(c,"%HUF-1.0.%"))
       {
	       printf("Usage : Passer en paramètre un fichier compressé par huf\n");
	       exit(1);
       }
     else
       {
	 /////printf("Fichier correct, début de la décompression\n");
    
	 unsigned long long int* occurence=malloc(sizeof(unsigned long long int));
	
	 fread(occurence,sizeof(unsigned long long int),1,fichierComp);
	    
	 /////printf("Le nombre de caractères est %Lu \n",*occurence);

	     
	
	 fread(cpt,sizeof(unsigned long long int),1,fichierComp);
		
	 /////printf("Le nombre de caractères différent est %Lu\n",*cpt);

	 unsigned long long int CarE=0;
	 recuperDico(TableCar,fichierComp,*cpt);
   
   

	 /////printf("j'affiche tableCar\n");
	    
	 /////afficheTabCar(TableCar);

  
	 

	 recuperSuite(fichierComp,fTaille,TableCar,argv[1],occurence,&CarE);
 	       
 
		 
       }
    }
 
     else
       {
	 printf("Erreur d'ouverture");
	 exit(2);
       }

     fclose(fichierComp);

 

 
     printf("\n");
     return 0;

}

