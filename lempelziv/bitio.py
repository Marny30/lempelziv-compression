#!/usr/bin/python3

class BitIO():
    def __init__(self, filename, write=True):
        self.bitcount = 0
        self.currbyte = 0
        
        if write: self.mode = 'wb'
        else: self.mode = 'rb'
        
        try:
            self.file = open(filename, self.mode)
        except Exception as err:
            print('Couldn\'t open ' + filename + ":" + err)
            exit(1)
            
    def __del__(self):
        if self.mode=='wb' and self.bitcount:
            # print("EMPTYING CURRBYTE :"+ str(self.bitcount) + ": " + bin(self.currbyte)[2:])
            for i in range(8-self.bitcount):
                self.currbyte = self.currbyte << 1
            
            self._writeByte()
            self.bitcount = 0
            
    def _bufferizeBit(self, bit):
        self.currbyte = self.currbyte << 1 | bit
        self.bitcount += 1
        if self.bitcount == 8:
            self._writeByte()
            self.currbyte = 0
            self.bitcount = 0
        
    def _writeByte(self):
        # extended ascii : from 0 to 255
        byte = chr(self.currbyte).encode('latin-1')
        self.file.write(byte)
    
    def writeBin(self, number, length):
        for i in range(length-1, -1, -1): # [length; 0]
            if number >= 2**i:
                self._bufferizeBit(1)
                number -= 2**i
            else:
                self._bufferizeBit(0)

    def _getnextbit(self):
        if self.bitcount == 0:
            self.currbyte = ord(self.file.read(1))
            self.bitcount = 8
        self.bitcount -= 1
        return (self.currbyte >> self.bitcount & 1)

    def read(self, length):
        nb = 0
        try:
            for i in range(length-1,-1,-1):
                bit = self._getnextbit()
                nb = nb << 1 | bit
            return nb
        except:
            return 'EOF'

if __name__ == '__main__':
    bithandler = BitIO('workfile', write=True)    
    bithandler.writeBin(ord('î'), 8)
    bithandler.writeBin(86, 16)
    bithandler.writeBin(2, 4)
    bithandler.writeBin(3, 3)
    bithandler.writeBin(1, 1)

    bithandler = BitIO('workfile', write=False)
    d = list()
    d.append(bithandler.read(8))
    d.append(bithandler.read(16))
    d.append(bithandler.read(4))
    d.append(bithandler.read(3))
    d.append(bithandler.read(1))
    d.append(bithandler.read(1))
    print('decoded : ' + str(d))
