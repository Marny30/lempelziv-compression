#!/usr/bin/python3

# Methodologie
# 1. Raw -> Codage Ziv
# 2. Codage Ziv -> Codage Binaire pour stockage
# 3. Codage Bin -> Décodage


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
    
def dictToBin(compressed, dict, pretty=False, toByte=False):
    ''' Generation d'un format compréssé pour le code de Lempel Ziv'''
    from math import log
    aux = list()
    res = ""
    size = 0
    for i in range(len(compressed)):
        binIndex = iToBin(i, compressed[i][0])
        aux.append((binIndex, compressed[i][1]))
        size += len(binIndex) + 8*int(i>0)

    # génération de la sortie
    for i in range(len(aux)):
        if pretty:
            res+= aux[i][0] + "," + aux[i][1]
            if i < len(aux)-1: res += "|"
        else:
            res += aux[i][0] + aux[i][1]
            
    # TODO: ajout du préfixe rendant le code multiple d'octets
    prefix=""
    if toByte:
        print("size:" + str(size))
        bitToAdd = 8-(size % 8)
        print("to add:" + str(bitToAdd))
        for i in range(bitToAdd, 0, -1):
            if i==1:
                prefix += "1"
            else:
                prefix += "0"
    return prefix+res


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

    rawString = "AABABBBABAABABBBABBABB"

    zivcode, dict = encode(rawString)
            
    prettycode = dictToBin(zivcode, dict, True)
    code = dictToBin(zivcode, dict)

    print("input:")
    print("\t" + rawString)

    # print dictionnaire
    print("Dictionnaire")
    print("------------")
    for i in range(len(dict)):
        print(str(i).rjust(3) + " | " + dict[i])

    print("format compressé:\n\t", end="")
    print(*zivcode)

    print("code compressé (découpage):")
    print("\t" + prettycode)
    print("code compressé (brut):")
    print("\t" + code)
    print("\nlength input  (bits) : " + str(len(rawString)*8))

    #calcul poids : 1 par bit, et un byte par char.
    # TODO : Gestion des char unicodes.
    weight=0
    for i in range(len(zivcode)):
        weight+= len(iToBin(i,zivcode[i][0])) + 8*int(i>0)
    print("length output (bits) : " + str(weight))

    res = decode(code)
    print("decoded = " +res)
    print("Encodage/Décodage correct : " + str(res == rawString))
