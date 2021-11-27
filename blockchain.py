import hashlib

"""
pour faire un hash, il faut encoder l objet avant de faire le hash
* si on par d une chaine de bytes, c ok
    a = b"hello"    
    b = sha256(a)       --> on fait le hash
    c = b.hexdigest()   --> convertir en une chaine de caractere
* si on par d une chaine ou chaque car est code sur 4 octets ...pb
    d = "hello"
    e = sha256(d)   --> TypeError: Unicode-objects must be encoded before hashing
donc
    e = sha256(d.encode('utf-8'))
    f = e.hexdigest()

str.encode() renvoie une representation bytes de la chaine unicode
bytes.decode() renvoye une representation str ...
"""

class Block:
    # Define Block Structure
    def __init__(self, no, nonce, data, hashcode, prev):
        self.no = no                # Block number
        self.nonce = nonce          # number to calculate the proof of work
        self.data = data            # transaction / ledger
        self.hashcode = hashcode    # block hash
        self.prev = prev            # previous block hash

    def getStringVal(self):
        return self.no, self.nonce, self.data, self.hashcode, self.prev


class Blockchain:
    # Define simple blockchain structure, add new block and chain them together
    def __init__(self):
        self.chain = []             # la chaine
        self.prefix = "0000"        # proof of work

    def addNewBlock(self, data):
        no = len(self.chain)
        nonce = 0

        if len(self.chain) == 0:    # 1er block
            prev = "0"
        else:
            prev = self.chain[-1].hashcode

        """
        data
        str(data)   --> str
        str(data).encode('utf-8')   --> renvoie une representation bytes de la chaine unicode
        sha256(str(data).encode('utf-8'))   --> le sha
        .hexgigest()    --> converti en une chaine
        """
        myHash = hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        block = Block(no, nonce, data, myHash, prev)
        self.chain.append(block)

    def printBlockChain(self):
        chainDict = {}
        for no in range(len(self.chain)):
            chainDict[no] = self.chain[no].getStringVal()
        print(chainDict)

    def mineChain(self):
        ### check wether the chain is broken
        brokenLink = self.checkIfBroken()

        if (brokenLink == None):
            pass
        else:
            for block in self.chain[brokenLink.no:]:
                print("Mining Block:", block.getStringVal())
                self.mineBlock(block)

        ## if it is boken

        ## else start mining the block from the broken block to the end block


    """
    miner c trouver le bon hash
    """
    def mineBlock(self, block):
        nonce = 0
        myHash = hashlib.sha256(str(str(nonce) + str(block.data)).encode('utf-8')).hexdigest()
        while myHash[0:4] != self.prefix:
            myHash = hashlib.sha256(str(str(nonce) + str(block.data)).encode('utf-8')).hexdigest()
            nonce += 1
        else:
            print("nonce   ", nonce)
            print("new hash", myHash)
            self.chain[block.no].hashcode = myHash
            self.chain[block.no].nonce = nonce
            if(block.no < len(self.chain) - 1):
                self.chain[block.no + 1].prev = myHash

    def checkIfBroken(self):
        for no in range(len(self.chain)):
            if ( self.chain[no].hashcode[0:4] == self.prefix ):
                pass
            else:
                return self.chain[no]
        return None

    def changeData(self, no, data):
        self.chain[no].data = data
        self.chain[no].hashcode = hashlib.sha256(str(str(self.chain[no].nonce)+str(self.chain[no].data)).encode('utf-8')).hexdigest() 

"""
PERSO\Blockhain>python

>>> from blockchain import *
>>> b = Blockchain()
>>> b.addNewBlock("My Data")
>>> b.printBlockChain()

>>> b.addNewBlock("Hello")
>>> b.printBlockChain()

>>> b.addNewBlock("World")
>>> b.printBlockChain()

>>> b.mineChain()

>>> b.printBlockChain()

>>> b.changeData(1, "My Hello")
>>> b.printBlockChain()

>>> b.mineChain()
>>> b.printBlockChain()
"""