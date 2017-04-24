#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

class TrieApp():
    def __init__(self):
        self.root = Tk()
        self.root.title("Génération de Trie de Lempel Ziv")
        # self.root.resizable(0,0)
        self.frame = ttk.Frame(self.root, padding="10 5 10 5")
        self.frame.grid(column=3, row=3, sticky=(N, W, E, S))
        self.path = StringVar(self.root)
        Label(self.frame, text="Chaîne : ").grid(row=0, sticky=W)
        Label(self.frame, text="ou fichier : ").grid(row=1, sticky=W)
        self.e1 = Entry(self.frame)
        self.e2 = Entry(self.frame, textvariable=self.path)
        self.e1.grid(row=0, column=1, columnspan=2, sticky="nsew")
        self.e2.grid(row=1, column=1)
        ttk.Button(self.frame, text="Parcourir", command=self.parcourir).grid(column=2, row=1, pady=10)
        ttk.Button(self.frame, text="Ok", command=self.draw).grid(column=1, row=2, pady=10)
        
    def parcourir(self):
        import tkinter.filedialog
        self.path.set(tkinter.filedialog.askopenfilename())
    
    def draw(self):
        import trie as trie
        import lempelziv.lz78explained as lz78explained
        import tkinter.messagebox
        import os
        text = self.e1.get()
        path = self.e2.get()
        trie.NBLETTER = 0
        if text:
            print(text)
            isFile = False
            trie.HEADER, trie.FOOTER = True, True
        elif path:
            try:
                text = trie.readfile(path)
                isFile = True
            except:
                tkinter.messagebox.showwarning("Erreur", path + " n'a pas pu être lu")
                return
        else:
            return

        code, dico = lz78explained.encode(text)
        trie.stepbyStepWrapper(text, 'lz78graph')
        os.system('exo-open lz78graph.ps')
        
    def show(self):
        self.frame.destroy()
        
class App():
    def __init__(self, master):
        self.master = master
        master.title("Compression de texte")
        # master.minsize(width=300, height=400)
        self.accueil()

    def sousmenu(self, retour='self.accueil'):
        ttk.Button(self.frame, text="Quitter", command=quit).grid(row=4, column=1, padx=10, pady=10)
        if retour:
            ttk.Button(self.frame, text="Retour", command=eval(retour)).grid(row=4, column=0, padx=10, pady=10)
        
    def accueil(self):
        try:
            self.frame.destroy()
        except:
            pass
        self.frame = ttk.Frame(self.master, padding="40 5 40 5")
        self.frame.rowconfigure( 0, weight = 1 )
        self.frame.columnconfigure( 0, weight = 1 )
        self.frame.grid(column=3, row=3, sticky=(N, W, E, S))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        ttk.Button(self.frame, text="Huffman", command=self.huffman).grid(row=0, column=0, columnspan=2, pady=10, sticky="nswe")
        ttk.Button(self.frame, text="Lempel Ziv", command=self.lempelziv).grid(row=1, column=0, columnspan=2, pady=10, sticky="NSEW")
        ttk.Button(self.frame, text="Comparaisons", command=self.comp).grid(row=2, column=0, columnspan=3,pady=10)
        
        self.sousmenu(retour=False)
        
    def huffman(self):
        pass
    
    def lempelziv(self):
        self.frame.destroy()
        self.frame = ttk.Frame(self.master, padding="10 5 10 5")
        self.frame.grid(column=3, row=3, sticky=(N, W, E, S))
        ttk.Button(self.frame, text="Galaxie Lempel Ziv", command=self.lempelziv).grid(column=0, columnspan=2, row=0, pady=10)
        ttk.Button(self.frame, text="LZ77", command=self.lempelziv).grid(column=0, columnspan=2, row=1, pady=10)
        ttk.Button(self.frame, text="LZ78 : codage pas à pas", command=self.lempelzivTrie).grid(column=0, columnspan=2,  row=3, pady=10)
        ttk.Button(self.frame, text="LZ78 plus en détail", command=self.lempelziv).grid(column=0, columnspan=2,  row=2, pady=10)
        self.sousmenu()

    def lempelzivTrie(self):
        t = TrieApp()
        # self.frame.destroy()
        # self.frame = ttk.Frame(self.master, padding="10 5 10 5")
        # self.frame.grid(column=3, row=3, sticky=(N, W, E, S))



        # self.sousmenu(retour='self.lempelziv')
             
    def comp(self):
        pass
    
def main():
    root = Tk()
    root.resizable(0,0)
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'lempelziv'))
    app = App(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
