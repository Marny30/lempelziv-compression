#!/usr/bin/python3

from tkinter import *
from tkinter import ttk


class SaisieApp():
    def __init__(self, title="Saisie"):
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(0,0)
        self.frame = ttk.Frame(self.root, padding="10 5 10 5")
        
        self.frame.grid(column=3, row=3, sticky=(N, W, E, S))
        self.frame.pack(fill=BOTH, expand=YES)

        self.path = StringVar(self.root)
        
        Label(self.frame, text="Chaîne : ").grid(row=0, sticky=W)
        Label(self.frame, text="ou fichier : ").grid(row=1, sticky=W)
        
        self.e1 = Entry(self.frame)
        self.e2 = Entry(self.frame, textvariable=self.path)
        self.e1.grid(row=0, column=1, columnspan=2, sticky="nsew")
        self.e2.grid(row=1, column=1, sticky="ew")
        
        Button(self.frame, text="Parcourir", command=self.parcourir).grid(column=2, row=1, pady=10)
        Button(self.frame, text="Ok", command=self.draw).grid(column=1, row=10, pady=10)
        
    def parcourir(self):
        import tkinter.filedialog
        self.path.set(tkinter.filedialog.askopenfilename())
        
    def draw(self):
        pass

class HuffApp(SaisieApp):
    def draw(self):
        pass

class TrieApp(SaisieApp):
    def __init__(self):
        super().__init__(title="Génération de Trie de Lempel Ziv")
        self.step = BooleanVar(self.root)
        Checkbutton(self.frame, text="Étape par étape", variable=self.step).grid(row=2, sticky=W)
        
    def draw(self):
        import lempelziv.trie as trie
        import lempelziv.lz78 as lz78
        import tkinter.messagebox
        import os
        
        text = self.e1.get()
        path = self.e2.get()
        filename='lz78graph.ps'
        trie.NBLETTER = 0
        
        if text:
            data = text
            trie.HEADER, trie.FOOTER = True, True
        elif path:
            try:
                data = trie.readfile(path)
                trie.HEADER = False
                trie.FOOTER = False
            except:
                tkinter.messagebox.showwarning("Erreur", path + " n'a pas pu être lu")
                return
        else:
            return

        code, dico = lz78.encode(data)
        if self.step.get():
            trie.stepbyStepWrapper(data, code, dico, filename)
        else:
            graph=trie.draw(data, code, dico)
            with open('tmp.dot', 'w') as f:
                f.write(graph)
            trie.dotToPS(['tmp.dot'], filename)
        os.system('exo-open '+ filename)


class CompressionApp(SaisieApp):
    def __init__(self):
        super().__init__(title="Compression LZ78")
        
        self.isize = StringVar(self.root)
        self.osize = StringVar(self.root)

        self.isize.set('poids input:\t0\tbits')
        self.osize.set('poids compressé:\t0\tbits')
        
        self.t1 = Text(self.frame, height=2, width=30, font=(None, 13))
        self.t1.grid(row=2, column=0, columnspan=3, sticky="ew")
        
        
        self.t2 = Text(self.frame, height=2, width=30, font=(None, 13))
        self.t2.grid(row=3, column=0, columnspan=3, sticky="ew")
        Label(self.frame, textvariable= self.isize).grid(row=4, sticky=W,columnspan=3)
        Label(self.frame, textvariable = self.osize).grid(row=5, sticky=W,columnspan=3)
        
    def draw(self):
        import lempelziv.lz78 as lz78
        import tkinter.messagebox
        
        self.t1.delete(1.0, END)
        self.t2.delete(1.0, END)
        text = self.e1.get()
        path = self.e2.get()
        
        if text:
            data = text
        elif path:
            try:
                data = lz78.readfile(path)
            except:
                tkinter.messagebox.showwarning("Erreur", path + " n'a pas pu être lu")
                return
        else:
            return

        size = len(data)*8
        zivcode, dico = lz78.encode(data)
        compressed, csize = lz78.codeToBinString(zivcode)

        cpt=0
        l1, l2 = 0, 0
        isBlue = False
        for i in range(len(zivcode)):
            l1_end = l1 + len(str(zivcode[i][0])) + len(zivcode[i][1]) +1
            l2_end = l2 + len(compressed[i][0]) + len(compressed[i][1]) +1
            self.t1.insert(INSERT, zivcode[i][0])
            self.t1.insert(INSERT, zivcode[i][1])

            self.t1.insert(INSERT, ' ')
            self.t2.insert(INSERT, compressed[i][0])
            self.t2.insert(INSERT, compressed[i][1])
            self.t2.insert(INSERT, ' ')
            
            self.t1.tag_add(str(cpt), "1."+str(l1), "1."+str(l1_end))
            self.t2.tag_add(str(cpt), "1."+str(l2), "1."+str(l2_end))
            if isBlue:                
                self.t1.tag_config(str(cpt), foreground="blue")
                self.t2.tag_config(str(cpt), foreground="blue")
            else:
                self.t1.tag_config(str(cpt), foreground="red")
                self.t2.tag_config(str(cpt), foreground="red")
            l1= l1_end
            l2 = l2_end
            cpt+=1
            isBlue = not isBlue
        self.isize.set('poids input:\t'+ str(size) +'\tbits')
        self.osize.set('poids compressé:\t'+ str(csize) +'\tbits')
