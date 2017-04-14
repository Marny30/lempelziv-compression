#!/usr/bin/python3

# Méthodologie
# 1. Tokénisation
# 2. Génération table "Search Buffer-Look Ahead"
# 3. Encodage binaire de cette dernière


def encode(input):
    w = ""
    dictionnary= list()
    res= list()
    dictionnary.append("")            # mot vide
    for i in range(len(input)):
        letter = input[i]
        if w+letter in dictionnary:
            w += letter
        else:
            res.append((dictionnary.index(w), letter))
            dictionnary.append(w+letter) 
            w =""
    # Récupération dernier mot
    if w != '':
        res.append((dictionnary.index(w), ''))
    return res, dictionnary


def iToBin(pos, nb):
    '''entier vers binaire, avec un nombre de 0 devant dépendant de pos'''
    from math import log
    if pos>0:
        nbzfill = int(log(pos, 2)) +1
        return bin(nb)[2:].zfill(nbzfill)
    else:
        return ''
    
def dictToBin(compressed, dict, pretty=False):
    ''' Generation d'un format compréssé pour le code de Lempel Ziv'''
    from math import log
    aux = list()
    res = ""
    for i in range(len(compressed)):
        binIndex = iToBin(i, compressed[i][0])
        aux.append((binIndex, compressed[i][1]))
    # génération de la sortie
    for i in range(len(aux)):
        if pretty:
            res+= aux[i][0] + "," + aux[i][1]
            if i < len(aux)-1: res += "|"
        else:
            res += aux[i][0] + aux[i][1]
    return res


def decode(code):
    from math import log
    dico = ['']
    nbCarLus = 0
    i = 0                       # curseur dans mot
    index=1                     # index dans dictionnaire
    
    # lecture premier caractère
    letter = code[i]
    nbCarLus = 1; i=1
    dico.append(letter)
    res = letter
    
    while i in range(len(code)):
        # lecture de l'index
        toRead = int(log(nbCarLus ,2)) +1
        # print("now reading " +str(toRead) + " chars")
        # print("from " + code[i:])
        index = code[i:i+toRead] # index binaire
        index = int(index, 2)
        i += toRead

        # build prefix
        if (index==0):
            string = ""
        else:
            string = dico[index]

        # Si on est sur le dernier atome, et qu'il n'est constitué que
        # d'une référence (pas de lettre derrière)
        if i>=len(code):
            res+=string
            break;
        # read a char
        letter = code[i]
        nbCarLus += 1
        i+=1
        
        dico.append(string + letter)
        res+= string+letter
    return res

if __name__ == '__main__':
    import random
    length = 30
    rawString = ''.join(random.choice('ACGT') for _ in range(length))
    # rawString = "0010111010010111011011"
    rawString = "AABABBBABAABABBBABBABB"

    compressed, dict = encode(rawString)
            
    prettycode = dictToBin(compressed, dict, True)
    code = dictToBin(compressed, dict)

    print("input:")
    print("\t" + rawString)

    # print dictionnaire
    print("Dictionnaire")
    print("------------")
    for i in range(len(dict)):
        print(str(i).rjust(3) + " | " + dict[i])

    print("format compressé:\n\t", end="")
    print(*compressed)

    print("code compressé (découpage):")
    print("\t" + prettycode)
    print("code compressé (brut):")
    print("\t" + code)
    print("\nlength input  (bits) : " + str(len(rawString)*8))

    #calcul poids : 1 par bit, et un byte par char.
    # TODO : Gestion des char unicodes.
    weight=0
    for i in range(len(compressed)):
        weight+= len(iToBin(i,compressed[i][0])) + 8*int(i>0)
    print("length output (bits) : " + str(weight))

    res = decode(code)
    print("decoded = " +res)
    print("Encodage/Décodage correct : " + str(res == rawString))
