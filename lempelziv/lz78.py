#!/usr/bin/python3

# Methodologie
# 1. Raw -> Codage Ziv
# 2. Codage Ziv -> Codage Binaire pour stockage
# 3. Codage Bin -> Décodage

import bitio

dico = list('')

def encode(input):
    global dico
    w = ""
    res= list()
    dico.append('')
    for i in range(len(input)):
        letter = input[i]
        if w+letter in dico:
            w += letter
        else:
            res.append((dico.index(w), letter))
            dico.append(w+letter) 
            w =""
    # Récupération dernier mot
    if w != '':
        res.append((dico.index(w), ''))
    return res, dico

def _iToBin(pos, nb):
    '''entier vers binaire, avec un nombre de 0 devant dépendant de pos
    Utile seulement pour print'''
    from math import log
    if pos>0:
        length = int(log(pos, 2)) +1
        return bin(nb)[2:].zfill(length)
    else:
        return ''

def codeToBinString(code):
    ''' Écriture en string du code ziv. pour print '''
    res = list()
    size = 0
    for i in range(len(code)):
        binIndex = _iToBin(i, code[i][0])
        res.append((binIndex, code[i][1]))
        size += len(binIndex) + 8*int(i>0)
    return res, size

def dictToBin(code, dict, pretty=False, toByte=False):
    ''' Generation d'un format compréssé pour le code de Lempel Ziv'''
    from math import log
    aux = list()
    res = ""
    size = 0
    for i in range(len(code)):
        binIndex = iToBin(i, code[i][0])
        aux.append((binIndex, code[i][1]))
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

def decode(zivcode):
    from math import log
    dico = ['']
    nbCarLus = 0
    i = 0                       # curseur dans mot
    # lecture premier caractère
    res = ''
    for i in range(len(zivcode)):        
        # build prefix
        ref = zivcode[i][0]
        letter = zivcode[i][1]
        # print("reading" + str(zivcode[i]))
        if ref==0:
            string = ""
        else:
            string = dico[ref]
        # Si on est sur le dernier atome, et qu'il n'est constitué que
        # d'une référence (pas de lettre derrière)
        if ref == '':
            res+=string
            break;
        # read a char
        # print("new entry:" + string+ "+"+letter)
        dico.append(string + letter)
        res+= string+letter
    # print(dico)
    return res

# Écrire
def writecompressed(zivcode, path):
    from math import log
    bithandler = bitio.BitIO(path, write=True)
    
    if len(zivcode)>=1:
        bithandler.writeBin(ord(zivcode[0][1]), 8) # lettre
        print('write : ' + str(ord(zivcode[0][1])))

    for i in range(1, len(zivcode)):
        length = int(log(i, 2)) +1
        bithandler.writeBin(zivcode[i][0], length)
        print('write : ' + str(zivcode[i][0]) + ', len=' + str(length))
        print(str(zivcode[i]) + ":" + str(length))

        if zivcode[i][1]!='':
            bithandler.writeBin(ord(zivcode[i][1]), 8) # lettre
            print('write : ' + str(ord(zivcode[i][1])))
    del bithandler


# lis un fichier compressé depuis path et retourne le code de lempelziv
def readcompressed(path):
    from math import log
    bithandler = bitio.BitIO(path, write=False)    
    i=1
    ref = 0
    res = []
    char = bithandler.read(8) # lettre
    while char!='EOF' and ref!='EOF':
        if char=='EOF':
            break
        else:
            char = chr(char)
            # print('read {' + str(ref) + "," + str(char) + "} updating dict.")
        res.append((ref, char))        
        length = int(log(i, 2)) +1
        ref = bithandler.read(length)
        char = bithandler.read(8) # lettre
        i+=1
    # Si il y a encore à écrire (référence existante, mais pas char)
    if ref!='EOF' and ref!=0 and char=='EOF':
        # print('reading last byte')
        # print('read {' + str(ref) + ", ''} updating dict.")
        res.append((ref,''))
    return res

def readfile(path):
    global isFile
    try:
        with open(path, 'r') as f:
            content = f.read()
            return content
    except:
        sys.stderr.write("Couldn't open " + path +"\n")
        exit(1)        

if __name__ == '__main__':
    import argparse
    
    p = argparse.ArgumentParser(description="Compression de lempel ziv78", prog="lz78.py")
    action=p.add_mutually_exclusive_group(required = True)
    action.add_argument('-c', action='store_true', dest='code', help='codage de données brutes')
    action.add_argument('-d', action='store_true', dest='decode', help='décompression de fichier compressé')
    p.add_argument('-o', metavar='output', dest='output',  type=str , help='nom de la sortie')
    p.add_argument('input', type=str, help='entrée à traiter')
    p.add_argument('-f', action='store_true', dest='isfile', help='l\'input est un chemin')
    p.add_argument('--nobin', action='store_true', dest='nobinary', help='utiliser un codage numérique. implique -p.')
    p.add_argument('-p', '--print', action='store_true', dest='printing', help='affchage dans terminal. exclut l\'écriture dans fichier.')
    
    args = p.parse_args()
    if args.code: suffix = ".lz"
    else: suffix = ".txt"
    
    if args.isfile:
        if args.output:
            output = args.output
        else:
            output = args.input + suffix
        if args.code:
            rawdata = readfile(args.input)
    else:
        output="out" +suffix
        rawdata = args.input

    if args.code:
        zivcode, dict = encode(rawdata)
    else:
        zivcode = readcompressed(args.input)

    if args.nobinary:
        res = zivcode
    else:
        res = codeToBinString(zivcode)

    if not (args.printing or args.nobinary):
        if args.code:
            writecompressed(zivcode, output)
        else:
            res = decode(zivcode)
            print("decoded: " + str(res))
            
    else:
        print("input:")
        print("\t" + args.input)
        # print dictionnaire
        print("Dictionnaire")
        print(" --------------")
        for i in range(len(dict)):
            print(str(i).rjust(3) + " | " + dict[i])
        print("Code de lempel-ziv:\n\t", end="")
        print(*zivcode)
        print("format compressé:\n\t", end="")
        print(*res[0])
