
# coding: utf-8

# We’ll start by first defining what our blocks will look like. In blockchain, each block is stored with a timestamp and, optionally, an index. In SnakeCoin, we’re going to store both. And to help ensure integrity throughout the blockchain, each block will have a self-identifying hash. Like Bitcoin, each block’s hash will be a cryptographic hash of the block’s index, timestamp, data, and the hash of the previous block’s hash. Oh, and the data can be anything you want.
# 
# 
# We’ll be using a hash function to create a ‘fingerprint’ for each of our transactions- this hash function links each of our blocks to each other. To make this easier to use, we’ll define a helper function to wrap the python hash function that we’re using.
# 
# 

# In[114]:


import hashlib, json, sys
import datetime 

def hashMe(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!
        
    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
    
    
    
    


# Awesome! We have our block structure, but we’re creating a blockchain. We need to start adding blocks to the actual chain. As I mentioned earlier, each block requires information from the previous block. But with that being said, a question arises: how does the first block in the blockchain get there? Well, the first block, or genesis block, is a special block. In many cases, it’s added manually or has unique logic allowing it to be added.
# 
# We’ll create a function that simply returns a genesis block to make things easy. This block is of index 0, and it has an arbitrary data value and an arbitrary value in the “previous hash” parameter.

# We’ll create a function that simply returns a genesis block to make things easy. This block is of index 0, and it has an arbitrary data value and an arbitrary value in the “previous hash” parameter.

# In[115]:


import random
random.seed(0)

def makeTransaction(maxValue=3):
    # This will create valid transactions in the range of (1,maxValue)
    sign      = int(random.getrandbits(1))*2 - 1   # This will randomly choose -1 or 1
    amount    = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays   = -1 * alicePays
    # By construction, this will always return transactions that respect the conservation of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    return {u'Alice':alicePays,u'Bob':bobPays}


# In[116]:


txnBuffer = [makeTransaction() for i in range(30)]


# That’s the majority of the hard work. Now, we can create our blockchain! In our case, the blockchain itself is a simple Python list. The first element of the list is the genesis block. And of course, we need to add the succeeding blocks. Because SnakeCoin is the tiniest blockchain, we’ll only add 20 new blocks. We can do this with a for loop.

# In[117]:


def updateState(txn, state):
    # Inputs: txn, state: dictionaries keyed with account names, holding numeric values for transfer amount (txn) or account balance (state)
    # Returns: Updated state, with additional users added to state if necessary
    # NOTE: This does not not validate the transaction- just updates the state!
    
    # If the transaction is valid, then update the state
    state = state.copy() # As dictionaries are mutable, let's avoid any confusion by creating a working copy of the data.
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state


# In[118]:


def isValidTxn(txn,state):
    # Assume that the transaction is a dictionary keyed by account names

    # Check that the sum of the deposits and withdrawals is 0
    if sum(txn.values()) is not 0:
        return False
    
    # Check that the transaction does not cause an overdraft
    for key in txn.keys():
        if key in state.keys(): 
            acctBalance = state[key]
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return False
    
    return True


# In[139]:


# state = {u'Alice':5,u'Bob':5}

import hashlib

def encrypt_names(name_list):
    name = input("What is your first and last name? ")
    key = hashlib.sha256(str(name).encode('utf-8')).hexdigest()
    name_list.append(key)
    return name_list
    

def poverty_level_calculator(state, persons_over_eight, income):
    poverty = False
    if state.lowercase() == 'hawaii':
        if income < 1.25 * (13960 + (persons * 4970)):
            poverty = True
    elif state.lowercase() == 'alaska':
        if income < 1.25 * (15180 + (persons * 5400)):
            poverty = True
    else:
        if income < 1.25 * (12140 + (persons * 4320)):
            poverty = True
    return poverty

#how many things you have completed
def eligible():
    eligibility = False
    q1 = input("Have you ever been convictd of a felony, three or more misdemeanors, unlawful voting, or an offense under foreign law? (y/n) " )
    q2 = input("Does the Department of Homeland Security see you as a potential terrorist? (y/n) ")
    q3 = input("Did you just move to the US in 2017 or 2018? (y/n) ")
    q4 = input("Did you live in another country in 2017 or 2018? (y/n) ")
    if (q1.startswith("n") and q2.startswith("n") and q3.startswith("n") and q4.startswith("n")):
        eligibility = True
    return eligibility


# def updateBlock():
#     #days_out_of_country
#     #consecutive_days
#     #greater_lesser_than_poverty
#     #civics_english
#     #append to the dictionary, look at the states of the variables, if they are the same, don't overwrite
    
#                #most recently filled block for that person
    
#     #hash that is a public key that is not tied to their identity
#     #
#     #make a methodd that takes the hash and has a password for clearance to 


# In[148]:


# name_list = encrypt_names(['26bbe73163064fc162b73efe23cf531cd3206683285a947d01f525dba9f0be45'])
state = {encrypt_names:True, u'Bob':False}  # Define the initial state of citizenship
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'Current Status':0, u'hash':0, u'ParentHash':0, u'Users':[name_list]  }
genesisHash = hashMe( genesisBlockContents )
genesisBlock = {u'blockhash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)
genesisBlock


# In[149]:


genesisBlock


# In[150]:


chain = [genesisBlock]
chain


# In[137]:


def makeBlock(chain):
    parentBlock = chain[-1]
    parentHash  = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    blockContents = {u'blockNumber':blockNumber, u'datetime': datetime.datetime}
    blockHash = hashMe( blockContents )
    block = {u'hash':blockHash,u'contents':blockContents}
    
    return block


chain = makeBlock(chain)
len(chain)


# In[126]:


blockSizeLimit = 5  # Arbitrary number of transactions per block- 

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    
    ## Gather a set of valid transactions for inclusion
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn,state) # This will return False if txn is invalid
        
        if validTxn:           # If we got a valid state, not 'False'
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue  # This was an invalid transaction; ignore it and move on
        
    ## Make a block
myBlock = makeBlock(txnList,chain)
chain.append(myBlock)  


# In[108]:


## Functions for the application itself! 

def validate(days_out_of_country, consecutive_days, greater_lesser_than_poverty, civics_english):
    green_card = False
    Citizenship = False
    duration_of_time = 365*3 # in days
    if days_out_of_country <= 180 and (consecutive_days < 60 or greater_lesser_than_poverty < 51000): 
    # studying English three level categorical variable.  
        green_card = True
    
    if green_card and civics_english and duration_of_time == True:
        Citizenship = True
            
    return {'Citizenship': Citizenship, 'Green Card': green_card}


    
def poverty_level_calculator(state, person_over_eight, income):
    poverty = True
    if state.lowercase() == 'hawaii':
        if income < 1.25 * (13960 + (person * 4970)):
            poverty = True

    elif state.lowercase() == 'alaska':
        if income < 1.25 * (15180 +  ( person * 5400)):
            poverty = True
    else:
        if income < 1.25 *  (12140 + (person * 4320)): 
            poverty = True
    return poverty 


# In[109]:


validate(121, 80, 61000, True)

