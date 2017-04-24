#!/usr/bin/python3
import lz78explained

HEADER = False
FOOTER = False

def readfile(path):
    global isFile
    try:
        with open(path, 'r') as f:
            content = f.read()
            return content
    except:
        sys.stderr.write("Couldn't open " + path +"\n")
        exit(1)

def draw(rawdata, code, dico, cpt=-1):
    res = 'digraph trie {rankdir="TB";'
    lowestNode = [0,0] # i, profondeur
    
    if cpt==-1:
        cpt = len(code)
        
    if HEADER:
        res += 'subgraph clusterheader{margin=0;style="invis"'
        res += 'HEADER [shape="box" label="Chaîne\n'+ rawdata +' "];'
        res += "}"
        res += "HEADER -> 0  [style=invis]"
    res += 'subgraph clusterTree{margin=0;style="invis"'
    res += str(0) + ' [label="0"];'
    for i in range(len(code)):
        if i < cpt:
            suffix = ""
        else:
            suffix = "style=invis"
        # Recherche de l'entrée la plus basse pour la lier au footer
        if len(dico[i])>lowestNode[1]:
            lowestNode = [i, len(dico[i])]

        # si ce n'est pas un couple uniquement composé d'une
        # référence
        if code[i][1]!='':
            char = code[i][1]
            if char == '"': char = "''"
            elif char == "\\": char="\\\\"
            res += '\t' +str(i+1) + ' [label="' + str(i+1) + '"' + suffix + ']\n'
            # construction aretes
            res += '\t' + str(code[i][0])  +"->"+ str(i+1) +' [label="'+char+'"'+ suffix+ '];\n'
    res += '}'
    if FOOTER:
        # codepartiel = ' '.join(str(code[:cpt]))
        # codepartiel = ""
        # for i in range(cpt):
        #     codepartiel += str(code[i])
        res += 'subgraph clusterfooter{margin=0;style="invis"'
        res += ' FOOTER [shape="box" label="Code\n'+ str(code[:cpt]) +' "];}'
        res += str(lowestNode[0]) + " -> FOOTER  [constraint=true style=invis weight=0]"
    res += "}"
    return res

def dotToPS(inputList, output):
    os.system('dot -Tps '+ ' '.join(inputList) +' >' + output)
    os.system('rm '+ ' '.join(inputList))

def StepbyStepWrapper(raw, header, footer, output):
    cpt = 0
    cpt = len(code)
    output = outputname
    for i in cpt:
        graph = draw(raw, header, footer, cpt)
        output = str(cpt) + output
        with open(output, 'w') as f:
            f.write(graph)
            
if __name__ == '__main__':
    import argparse
    import os
    # global HEADER
    # global FOOTER
    cpt = -1
    p = argparse.ArgumentParser(description="Genère des Trie de  Lempel Ziv 78 Trie depuis l'entrée choisie", prog="trie.py")
    p.add_argument('-o', metavar='output', dest='output',  type=str , help='nom de la sortie')
    p.add_argument('input', type=str, help='entrée à traiter')
    p.add_argument('-f', action='store_true', dest='isfile', help='l\'input est un chemin')

    otype=p.add_mutually_exclusive_group()
    otype.add_argument('-p', '--print', action='store_true', help='non génération du graphe, arrêt à la génération du code intermédiaire')
    otype.add_argument('-e', action='store_true', dest='isStepByStep', help='construction étape par étape')
    
    args = p.parse_args()
    # print(args)
    if args.isfile:
        raw = readfile(args.input)
    else:
        raw = args.input
        HEADER = True
        FOOTER = True
        
    if args.output:
        output = args.output
    elif args.print:
        output = args.input + '.gv'
    else:
        output = args.input
        
    code, dico = lz78explained.encode(raw)
    if args.isStepByStep:
        inputs = list()
        for i in range(len(code)):
            current_file = 'tmp_'+str(i)+'.gv'
            graph = draw(raw, code, dico, i)
            inputs.append(current_file)
            
            with open(current_file, 'w') as f:
                f.write(graph)
            
        dotToPS(inputs, output+".ps")
    else:
        graph = draw(raw, code, dico)
        if args.print:
            with open(output, 'w') as f:
                f.write(graph)
            print(graph)
        else:
            with open('tmp.gv', 'w') as f:
                f.write(graph)
            # générer le graphe
            dotToPS(['tmp.gv'], output+'.ps')
