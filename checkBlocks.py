import subprocess
import json

# how many blocks you want to go back...
i = 100

binaryPath = 'C:\Program Files\Dogecoin\daemon\\'
cli = binaryPath + 'dogecoin-cli.exe'

currentBlock = 0
currentHash = ""
nonce = 0

# check current block number and go i blocks back
def getStartBlock():
    b = subprocess.Popen([cli, "getblockcount"],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
    b.stdin.close()
    
    for line in b.stdout:
        currentBlock = line.strip()
    return currentBlock

# get the current block hash
def getBlockHash(cb):
    cb = str(cb)
    b = subprocess.Popen([cli, "getblockhash", cb],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
    b.stdin.close()
    
    for line in b.stdout:
        currentHash = line.strip()
    return currentHash

# extract the nonce for the blockhash
def getNonce(bh):
    bh = str(bh)
    b = subprocess.Popen([cli, "getblock", bh],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
    b.stdin.close()
    data = json.load(b.stdout)

    return data['nonce']
    
    
    
currentBlock = getStartBlock()
print ("Starting with block: " + currentBlock)
l = 0
while l < i:
    currentHash = getBlockHash(currentBlock)
    nonce = getNonce(currentHash)
    type = "(non AuxPoW) "
    # nonce is always 0 for AuxPoW blocks
    if nonce == 0:
        type = "   (AuxPoW) "
    print ("Block "+type+str(currentBlock)+": " + currentHash)
    currentBlock = int(currentBlock) -1
    l = l+1
