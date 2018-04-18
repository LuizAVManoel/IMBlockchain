'''
Blockchain teste
Autor: Luiz Augusto VM
2018.1
'''

import hashlib, json, sys
import random

random.seed(0)

def hashMe(msg=""):
	if type(msg)!=str:
		msg = json.dumps(msg,sort_keys=true)

	if sys.version_info.major == 2:
		return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
	else:
		return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

# Create valid transactions in the range of (1,maxValue)
def makeTransaction(maxvalue=3): 

	sign = int(random.getrandbits(1))*2 -1 #sign = {-1,1}

	amount = random.randint(1,maxvalue)
	alicePays = sign * amount
	bobPays = -1 * alicePays

	return {u'Alice':alicePays,u'Bob':bobPays}

txnBuffer = [makeTransaction(7) for i in range(30)]
print(txnBuffer)

def updateState(txn,state): 
# Inputs: txn, state: dictionaries keyed with account names, holding numeric values for transfer amount (txn) or account balance (state)
# Returns: Updated state, with additional users added to state if necessary
# NOTE: This does not not validate the transaction- just updates the state!

	state = state.copy() # As dictionaries are mutable, let's avoid any confusion by creating a working copy of the data.
	for key in txn:
		if key in state.keys():
			state[key] += txn[key]
		else:
			state[key] = txn[key]
	return state

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

#Genesis block
state = {u'Alice':50, u'Bob':50}  # Define the initial state
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
genesisHash = hashMe( genesisBlockContents )
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

chain = [genesisBlock]

def makeBlock(txns,chain):
    
    parentBlock = chain[-1] #Last element
    parentHash  = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    txnCount    = len(txns)
    blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,
                     u'txnCount':len(txns),'txns':txns}
    blockHash = hashMe( blockContents )
    block = {u'hash':blockHash,u'contents':blockContents}
    
    return block