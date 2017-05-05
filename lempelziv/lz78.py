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
    dico = list('')
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
    size = 8
    for i in range(len(code)):
        binIndex = _iToBin(i, code[i][0])
        res.append((binIndex, code[i][1]))
        size += len(binIndex) + 8*int(i>0)
    return res, size

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
        dico.append(string + letter)
        res+= string+letter
    return res

# Écrire
def writecompressed(zivcode, path):
    from math import log
    bithandler = bitio.BitIO(path, write=True)    
    
    if len(zivcode)>=1:
        bithandler.writeBin(ord(zivcode[0][1]), 8) # lettre

    for i in range(1, len(zivcode)):
        length = int(log(i, 2)) +1
        
        bithandler.writeBin(zivcode[i][0], length)
        if zivcode[i][1]!='':
            bithandler.writeBin(ord(zivcode[i][1]), 8) # lettre
    del bithandler

def readcompressed(path):
    ''' lis un fichier compressé depuis path et retourne le code de lempelziv '''
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
        res.append((ref, char))        
        length = int(log(i, 2)) +1
        ref = bithandler.read(length)
        char = bithandler.read(8) # lettre
        i+=1
    # Si il y a encore à écrire (référence existante, mais pas char)
    if ref!='EOF' and ref!=0 and char=='EOF':
        res.append((ref,''))
    return res

def readfile(path):
    import sys

    try:
        bithandler = bitio.BitIO(path, write=False)
        char = bithandler.read(8)
        res = ''
        while char!='EOF':
            # print('read: ' + str(char))
            char = chr(char)
            res += char
            char = bithandler.read(8)
        return res
    except Exception as e:
        sys.stderr.write("Couldn't open " + path +": "+ str(e) +"\n")
        exit(1)        

if __name__ == '__main__':
    import argparse
    
    p = argparse.ArgumentParser(description="Compression de lempel ziv78", prog="lz78.py")
    action=p.add_mutually_exclusive_group(required = True)
    action.add_argument('-c', action='store_true', dest='code', help='compression de données brutes')
    action.add_argument('-d', action='store_true', dest='decode', help='décompression de fichier compressé')
    p.add_argument('input', type=str, help='entrée à traiter')
    p.add_argument('-s', action='store_true', dest='isString',
                   help='l\'input est une chaîne et non un chemin')
    p.add_argument('-p', '--print', action='store_true',
                   dest='printing', help='affichage des étapes de transformation dans le terminal. exclut l\'écriture dans fichier.')
    p.add_argument('-o', metavar='output', dest='output',  type=str , help='nom de la sortie')
    
    args = p.parse_args()
    if args.code: suffix = ".lz78"
    else: suffix = ""

    if args.output:
        output = args.output
    elif args.isString:
        output="out" +suffix
    elif args.decode and args.input[-5:]=='.lz78':
        output = args.input[:-5]
        
    if args.isString:
        rawdata = args.input
    elif args.code:
        print("reading input file..")
        rawdata = readfile(args.input)

    if args.code:
        print("encoding..")
        zivcode, dict = encode(rawdata)
    else:
        print("reading compressed file..")
        zivcode = readcompressed(args.input)
    
    if not (args.printing):
        if args.code:
            print("writing compressed file..")
            writecompressed(zivcode, output)
            print("ok")
        else:
            res = decode(zivcode)
            bithandler = bitio.BitIO(output, write=True)
            for i in res:
                bithandler.writeBin(ord(i), 8)
            print("decoded: " + res)
    else:
        res = codeToBinString(zivcode)
        print("input:")
        print("\t" + args.input)
        # print dictionnaire
        print("Dictionnaire")
        print(" --------------")
        for i in range(len(dict)):
            print(str(i).rjust(3) + " | " + dict[i])
        print("Code de lempel-ziv:  (ref, lettre)\n\t", end="")
        print(*zivcode)
        print("format compressé:\n\t", end="")
        print(*res[0])
