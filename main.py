import Crypto
import DES
import csv
from Crypto.Hash import SHA
from datetime import datetime as dt
from random import randint, sample
from Crypto.Util.Padding import pad

#Initializing ZKP values
p=11                                  
g=2                                  
r =0          
b =0 
y=0


open_transactions=[] #stores current open transactions
success_transactions=[] #stores succesful transactions

from Crypto.Cipher import DES
#Here we create the block class
class Block:

    def __init__(self, index, time, transaction, previousHash, proof_of_work):
        self.index=index                     
        self.time=time                        
        self.transaction=transaction         
        self.previousHash=previousHash                
        self.proof_of_work=proof_of_work                      
        self.currentHash=self.hashCalculationBlock()  

    def hashCalculationBlock(self):
        data=str(self.index)+str(self.time)+str(self.transaction)+str(self.previousHash)+str(self.proof_of_work)
        hashed=SHA.new(data.encode('utf-8'))
        hashed=str(hashed).split(" ")[-1]
        hashed=hashed.rstrip(hashed[-1])
        hashed=hashed.encode()
        # print(hashed)
        #DES
        anskey=b"\x13\x34\x57\x79\x9B\xBC\xDF\xF1"
        des=DES.new(anskey, DES.MODE_ECB)
        encryptedtext=des.encrypt(pad(hashed, 64))
        # print("Encrypted Text: ",encryptedtext)
        return encryptedtext

        

class Blockchain: 

    def __init__(self, diff):
        # self.transactions=[]  
        self.blockchain=[]        
        self.diff=diff          

    #creating genesis block, which acts as a header block in the code
    def genesisBlock(self):
        time=dt.now()
        trans=[]
        self.createBlock(0,time,trans,"0",0)

    def createBlock(self, index, time, transaction, previousHash, proof_of_work): #creates a new block
        block=Block(index, time, transaction, previousHash, proof_of_work)
        self.blockchain.append(block)

    def proof_of_work_calculation(self,block): #proof_of_work caculator
        prev=block
        proof_of_work=0
        
        testHash=SHA.new()
        testHash.update((str(proof_of_work)+str(prev.index)+str(prev.time)+ str(prev.transaction)+str(prev.previousHash)+str(prev.proof_of_work)).encode('utf-8'))
        
        while(testHash.hexdigest()[:self.diff]=='0'*self.diff):
            proof_of_work += 1
            testHash.update((str(proof_of_work)+str(prev.index)+str(prev.time)+ str(prev.transaction)+str(prev.previousHash)+str(prev.proof_of_work)).encode('utf-8'))
            # testHash.update((str(prev.previousHash)+str(prev.proof_of_work)).encode('utf-8'))
        print("test: ",testHash)
        return proof_of_work

    def mineBlock(self,mineArr): #mine the block
        prevBlock=self.blockchain[-1]
        proof_of_work=self.proof_of_work_calculation(prevBlock)

        self.createBlock((prevBlock.index+1), dt.now(), open_transactions, prevBlock.currentHash, proof_of_work)
        print("block ban gaya")

blockchain=Blockchain(2)
blockchain.genesisBlock()

def verifyTransaction():
    mineArr=[]
    print("In verifyTransaction: ",open_transactions)

    for i in range(len(open_transactions)):
        r=randint(0,p-1)         
        b=randint(0,1)
        amount=int(open_transactions[i]['amount'])
        y=pow(g,amount)%p
        # print(type(amount))

        s=(r+b*amount) % (p-1)
        h=pow(g,r)%p
        if (pow(g, s)%p) == (h * (pow(y, b)%p)):
            mineArr.append(open_transactions[i])
        else:
            print("The transaction ",open_transactions[i]," is invalid")

    if len(mineArr)>0:
        save(mineArr) #creates the CSV
        blockchain.mineBlock(mineArr)
        print("Valid Transactions mined")
    else:
        print("No transaction to mine")


def viewUser():
    inputUser=input("Input user's name: ")
    data=[]
    for block in blockchain.blockchain:
        for x in block.transaction:
            if x['sender'] == inputUser:
                data.append(x)
    
    print(data)

def get_transaction():
    sender=input("Input sender's name: ")
    recipient=input("Input recipient's name: ")
    amount=input("Enter the transaction amount: ")

    transaction={'sender': sender,
                    'recipient': recipient,
                    'amount': amount}
    return transaction,sender

def printFullBlockchain():
    for i in range(len(blockchain.blockchain)):
        print("Details of block ",i," are:")
        print("\tTime=",blockchain.blockchain[i].time)
        print("\tTransactions=",blockchain.blockchain[i].transaction)
        # print("\tPrevious block Hash=",blockchain.blockchain[i].previousHash)
        # print("\tCurrent block Hash=",blockchain.blockchain[i].currentHash)
        print("\tproof_of_work=",blockchain.blockchain[i].proof_of_work)


def save(mineArr): #creates the csv file
    csv_columns=['sender','recipient','amount']
    csv_file="save.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer=csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in mineArr:
                writer.writerow(data)
    except IOError:
        print("I/O error")

if __name__ == '__main__':
    while(True): #takes user input
        print("Enter your choice:")
        print("0: Do a transaction")
        print("1: Verify transaction and then mine block")
        print("2: View user")
        print("3: Print full blockchain")
        print("4: Exit")

        st=input()
        if st=='0':
            transaction,sender=get_transaction()
            open_transactions.append(transaction)
            print(open_transactions)
        elif st=='1':
            verifyTransaction()
            open_transactions=[]
            r=0
            b=0
            y=0
        elif st=='2':
            viewUser()
        elif st=='3':
            printFullBlockchain()
        elif st=='4':
            break
        else:
            print("Please choose from the following")
        
        
    print("Ho gaya.. GG")