#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
from interface import *

class App():
    def __init__(self, master):
        self.master = master
        master.title("Compression de texte")
        self.accueil()

    def sousmenu(self, retour='self.accueil'):
        Button(self.frame, text="Quitter", command=quit).grid(row=4, column=1, padx=10, pady=20)
        if retour:
            Button(self.frame, text="Retour", command=eval(retour)).grid(row=4, column=0, padx=10, pady=20)
        
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
        ttk.Button(self.frame, text="Comparaisons", command=self.comparaison).grid(row=2, column=0, columnspan=3,pady=10)
        
        self.sousmenu(retour=False)
        
    def huffman(self):
        h = HuffApp()
        print("TODO: HUFF APP")
    
    def lempelziv(self):
        self.frame.destroy()
        self.frame = ttk.Frame(self.master, padding="10 5 10 5")
        self.frame.grid(column=3, row=3, sticky=(N, W, E, S))
        Button(self.frame, text="LZ78 : codage pas à pas", command=self.lempelzivTrie).grid(column=0, columnspan=2,  row=0, pady=5)
        Button(self.frame, text="LZ78 : compression", command=self.compression).grid(column=0, columnspan=2,  row=1, pady=5)
        Button(self.frame, text="LZ77", command=self.lz77).grid(column=0, columnspan=2, row=2, pady=5)
        Button(self.frame, text="Famille Lempel Ziv", command=self.famille).grid(column=0, columnspan=2, row=3, pady=5)
        self.sousmenu()

    def lempelzivTrie(self):
        t = TrieApp()
    
    def compression(self):
        c = CompressionApp()

    def lz77(self):
        print("TODO: lz77")
        pass

    def famille(self):
        import os
        os.system('exo-open lempelziv/famille/famille.png')
    
    def comparaison(self):
        print("TODO: Comparison")
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
