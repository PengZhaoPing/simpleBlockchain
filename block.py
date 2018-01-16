#coding:utf-8
import time 
import random
import hashlib
import threading
import MerkleTrees
import mysql.connector
def __mining(recvTx):
    try:
        block=Block()
        block.getTransaction(recvTx)
        Chain.addBlock(block.newBlock["blockhash"] ,block.newBlock)
        block.ExchangeBlock()
        return Chain.getBlockFromHeight(Chain.getHeight())
    except Exception as e :
        print e

class Block:
    def __init__(self):
        self.txs=[]
        self.time=""
        pass
    def getTransaction(self,recvTx):
        #while True:
        try :
            self.create()
            self.newBlock["txs"].extend(recvTx)
            # hashTarget=self.SerializeToString(self.newBlock)
            ground_truth_Tree = MerkleTrees.Jae_MerkTree()
            txHashList = []
            for i in range(len(recvTx)):
                txHashList.append(recvTx[i]["txhash"])
            ground_truth_transaction = txHashList
            ground_truth_Tree.listoftransaction = ground_truth_transaction
            ground_truth_Tree.create_tree()
            ground_truth_past_transaction = ground_truth_Tree.Get_past_transacion()
            ground_truth_root = ground_truth_Tree.Get_Root_leaf()
            self.newBlock["merkleRoot"] = ground_truth_root
            hashTarget=str(self.newBlock["previoushash"])+str(self.newBlock["unixtime"])+str(self.newBlock["difficulty"])+str(self.newBlock["version"])+str(self.newBlock["merkleRoot"])
            blockhash=hashlib.sha256(hashTarget).hexdigest()
            nonce = 0
            while True:
                if(blockhash > Chain().getDifficulty()):
                    nonce+=1
                    blockhash = hashlib.sha256(hashTarget*nonce).hexdigest()
                else:
                    break
            self.newBlock["nonce"] = nonce
            self.newBlock["blockhash"] = blockhash
        except Exception as e:
            print (e)


        print ("mining Block: %d" % self.newBlock["height"])
        
        
        
    def firstblock(self):
        # 創世區塊
        blockhash="00002a3157a4c26c8f3f8f7785bc632602a4903125251f466c99e61afe92d976"
        newBlock = {"height":0, "unixtime":str(1497414820) , "previoushash":"This is first block", 
        "blockhash":blockhash, "merkleRoot":'', "txs":[], "difficulty":Chain().getDifficulty(), "nonce":str(1234), "version":1}


        self.newBlock = newBlock

        Chain.addBlock(blockhash,self.newBlock)
        return self.newBlock
        
        
    def create(self):
        # 建立區塊
        try:
            currentlyHeight = Chain.getHeight()
            previousblock = Chain.getBlockFromHeight(currentlyHeight)
            newBlock = {"height":Chain.getHeight()+1, "unixtime":str(time.time()) , "previoushash":previousblock["blockhash"], 
            "blockhash":"", "merkleRoot":"", "txs":[], "difficulty":Chain().getDifficulty(), "nonce":"", "version":1}
            self.newBlock = newBlock
            return self
        except Exception as e:
            print (e)

    def SerializeToString(self, data):
        targetString = ""+str(data)+""
        return targetString
        
    @staticmethod
    def ExchangeBlock():
        box=Chain.getBlockFromHeight(Chain.getHeight())
        print "-"*60+"Block:"+str(box["height"])+"-"*60
        print "{" 
        print ""
        print "height:", box["height"]
        print "unixtime:", box["unixtime"]
        print "previoushash:", box["previoushash"]
        print "blockhash:", box["blockhash"]
        print "merkleRoot:", box["merkleRoot"]
        print "difficulty:", box["difficulty"]
        print "nonce:", box["nonce"]
        print "version:", box["version"]
        print "txs:"
        for i in range(len(box["txs"])):
            print box["txs"][i]
        print ""
        print "}"
        print "-"*110

            
            

        
class Chain:
    #這些東西之後都要改成從DB裡面撈出來
    _blockFromHeight = {}
    _blockFromHash = {}
    _Height=0
    @staticmethod
    def getHeight():
        return Chain._Height


    @staticmethod
    def getBlockFromHeight(height):
        try:
            resultBlock = Chain._blockFromHeight[height]
            return resultBlock
        except Exception as e:
            time.sleep(1)
            # Block.From(height)
            raise Exception("not found height: %d block" % height)


    @staticmethod
    def getBlockFromHash(hashvalue):
        try:
            resultBlock = Chain._blockFromHash[hashvalue]
            return resultBlock
        except Exception as e:
            time.sleep(1)
            # Block.From(height)
            raise Exception("not found blockhash: %d block" % hashvalue)
    
    @staticmethod
    def getDifficulty():
        return "002fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

    @staticmethod
    def addBlock(key,block):
        Chain._Height=block["height"]
        Chain._blockFromHeight[block["height"]]=block
        Chain._blockFromHash[key] = block
        return "ADD_BLOCK"
                   


_firstblock = Block().firstblock()
print "----------------------------------------Block:0(this is first block)----------------------------------------"
print "{"
print ""
print "height:", _firstblock["height"]
print "unixtime:", _firstblock["unixtime"]
print "previoushash:", _firstblock["previoushash"]
print "blockhash:", _firstblock["blockhash"]
print "merkleRoot:", _firstblock["merkleRoot"]
print "difficulty:", _firstblock["difficulty"]
print "nonce:", _firstblock["nonce"]
print "version:", _firstblock["version"]
print "txs:", _firstblock["txs"]
print ""
print "}"
print "------------------------------------------------------------------------------------------------------------"

if __name__ == "__main__":
    print("Send test1 transaction")
    txsPool =[]
    tx1 = {'body': 'u1,u2,780$', 'unixtime': '1510822461.15', 'txhash': '091bda1b5f50980b2b68511f14c35c42b61761898e7008f3b3125ca39610bc2b'}
    tx2 = {'body': 'u3,u4,935$', 'unixtime': '1510822461.15', 'txhash': 'bb4683653913498a8d01cef3fd0990a233d52055764a431c113fb27a84b1e667'}
    print("")
    print(tx1)
    print(tx2)
    print("")
    txsPool.append(tx1)
    txsPool.append(tx2)
    __mining(txsPool)
    print("Send test2 transaction")
    txsPool =[]
    tx3 = {'body': 'u5,u6,500$', 'unixtime': '1510822461.34', 'txhash': '84a861c9241f86dd4071da3931ea720dcf967465e7a3cb979c2f4a4177bf6a59'}
    tx4 = {'body': 'u7,u8,843$', 'unixtime': '1510822461.34', 'txhash': 'b71298d3161cfe0a1308fedde4c13ae7a1fbd2ba4b438f8f4fc3c80c9729d96a'}
    print("")
    print(tx3)
    print(tx4)
    print("")
    txsPool.append(tx3)
    txsPool.append(tx4)
    __mining(txsPool)
