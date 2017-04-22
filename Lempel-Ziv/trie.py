#!/usr/bin/python3
import lz78explained

def readfile(path):
    global isFile
    try:
        with open(path, 'r') as f:
            content = f.read()
            return content
    except:
        sys.stderr.write("Couldn't open " + path +"\n")
        exit(1)

def draw(rawdata, header=False, footer=False):
    code, dico = lz78explained.encode(rawdata)
    res = 'digraph trie {rankdir="TB";'
    lowestNode = [0,0] # i, profondeur
    if header:
        res += 'subgraph clusterheader{margin=0;style="invis"'
        res += 'HEADER [shape="box" label="Chaîne\n'+ rawdata +' "];'
        res += "}"
        res += "HEADER -> 0  [style=invis]"
    res += 'subgraph clusterTree{margin=0;style="invis"'
    res += str(0) + ' [label="0"];'
    for i in range(len(code)):
        # Recherche de l'entrée la plus basse pour la lier au footer
        if len(dico[i])>lowestNode[1]:
            lowestNode = [i, len(dico[i])]

        # si ce n'est pas un couple uniquement composé d'une
        # référence
        if code[i][1]!='':
            char = code[i][1]
            if char == '"': char = "''"
            elif char == "\\": char="\\\\"
            res += '\t' +str(i+1) + ' [label="' + str(i+1) +'"]\n'
            # construction aretes
            res += '\t' + str(code[i][0])  +"->"+ str(i+1) +' [label="'+char+'"];\n'
    res += '}'
    if footer:
        res += 'subgraph clusterfooter{margin=0;style="invis"'
        res += ' FOOTER [shape="box" label="Code\n'+ str(code) +' "];}'
        res += str(lowestNode[0]) + " -> FOOTER  [constraint=true style=invis weight=0]"
    res += "}"
    return res

def dotToPS(input_path, output):
    os.system('dot -Tps '+ input_path +' >' + output)
    
if __name__ == '__main__':
    import argparse
    import os
    p = argparse.ArgumentParser(description="Genère des Trie de  Lempel Ziv 78 Trie depuis l'entrée choisie", prog="trie.py")
    p.add_argument('-p', '--print', action='store_true', help='non génération du graphe, arrêt à la génération du code intermédiaire')
    p.add_argument('-f', action='store_true', dest='isfile', help='l\'input est un chemin')
    p.add_argument('-o', metavar='output', dest='output',  type=str , help='nom de la sortie')
    
    p.add_argument('input', type=str, help='chemin de l\'entrée')
    args = p.parse_args()
    # print(args)
    if args.isfile:
        raw = readfile(args.input)
    else:
        raw = args.input
    
    if args.output:
        output = args.output
    elif args.print:
        output = args.input + '.gv'
    else:
        output = args.input + '.ps'

    graph = draw(raw, header=(not args.isfile), footer=(not args.isfile))
    
    if args.print:
        with open(output, 'w') as f:
            f.write(graph)
        print(graph)
    else:
        with open('tmp.gv', 'w') as f:
            f.write(graph)
        # générer le graphe
        dotToPS('tmp.gv', output)
