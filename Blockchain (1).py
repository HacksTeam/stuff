
# coding: utf-8

# ### IMMIGRATION ASSISTANCE USING A BLOCKCHAIN
# 
# Code based on open source project by Emunsing 
# https://github.com/emunsing/tutorials/blob/master/BuildYourOwnBlockchain.ipynb
# 
# We’ll start by first defining what our blocks will look like. In blockchain, each block is stored with a timestamp and an index. each block’s hash will be a cryptographic hash of the block’s index, timestamp, data, and the hash of the previous block’s hash. Oh, and the data can be anything you want.
# 
# 
# We’ll be using a hash function to create a ‘fingerprint’ for each of our transactions- this hash function links each of our blocks to each other. To make this easier to use, we’ll define a helper function to wrap the python hash function that we’re using.
# 
# 

# In[176]:


import hashlib, json, sys

def hashMe(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!
        
    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        # encrypting the message/contents on the network.
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
    


# Awesome! We have our block structure, but we’re creating a blockchain. We need to start adding blocks to the actual chain. As I mentioned earlier, each block requires information from the previous block. But with that being said, a question arises: how does the first block in the blockchain get there? Well, the first block, or genesis block, is a special block. In many cases, it’s added manually or has unique logic allowing it to be added.
# 
# We’ll create a function that simply returns a genesis block to make things easy. This block is of index 0, and it has an arbitrary data value and an arbitrary value in the “previous hash” parameter.

# We’ll create a function that simply returns a genesis block to make things easy. This block is of index 0, and it has an arbitrary data value and an arbitrary value in the “previous hash” parameter.

# That’s the majority of the hard work. Now, we can create our blockchain! In our case, the blockchain itself is a simple Python list. The first element of the list is the genesis block. And of course, we need to add the succeeding blocks. Because SnakeCoin is the tiniest blockchain, we’ll only add 20 new blocks. We can do this with a for loop.

# In[160]:


def encrypt_names(name_list):
    name = input("What is your first and last name? ")
    key = hashlib.sha256(str(name).encode('utf-8')).hexdigest()
    name_list.append(key)
    return name_list
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


# In[199]:


names = []
status = validate(125, 234, 54000, True)
names_list = encrypt_names(names)
state = {u'Accounts': ['7c88a4312054f89a2b73b04989cd9b9e1ae437e1048f89fbb4e18a08479de507']}  # Define the initial state
genesisBlockTxns = [state]

genesisBlockContents = {u'blockNumber':0,u'parentHash':None, u'accounts':['7c88a4312054f89a2b73b04989cd9b9e1ae437e1048f89fbb4e18a08479de507'],  'Green_card_eligible':  [True], 'Citizenship_Eligible': status  }
genesisHash = hashMe( genesisBlockContents )
genesisBlock = {u'block_hash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)


# In[201]:


names_list
genesisBlock


# In[191]:


chain = [genesisBlock]
# Blockchain of one block
chain


# In[177]:


# def makeBlock(chain):
#     parentBlock = chain[-1]
#     parentHash  = parentBlock[u'hash']
#     blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
#     blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash}
#     blockHash = hashMe( blockContents )
#     block = {u'hash':blockHash,u'contents':blockContents}
    
#     return block


# chain = makeBlock(chain)


# In[178]:


# blockSizeLimit = 5  # Arbitrary number of transactions per block- 

# while len(txnBuffer) > 0:
#     bufferStartSize = len(txnBuffer)
    
#     ## Gather a set of valid transactions for inclusion
#     txnList = []
#     while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
#         newTxn = txnBuffer.pop()
#         validTxn = isValidTxn(newTxn,state) # This will return False if txn is invalid
        
#         if validTxn:           # If we got a valid state, not 'False'
#             txnList.append(newTxn)
#             state = updateState(newTxn,state)
#         else:
#             print("ignored transaction")
#             sys.stdout.flush()
#             continue  # This was an invalid transaction; ignore it and move on
        
#     ## Make a block
# myBlock = makeBlock(txnList,chain)
# chain.append(myBlock)  

