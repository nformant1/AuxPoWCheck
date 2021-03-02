import subprocess
import json
import sys
from datetime import datetime

# how many tries
i = 6

binaryPath = 'C:\Program Files\Dogecoin\daemon\\'
cli = binaryPath + 'dogecoin-cli.exe'

currentBlock = 0
currentHash = ""
nonce = 0
time = 0


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

# extract the time for the blockhash
def getTime(bh):
    bh = str(bh)
    b = subprocess.Popen([cli, "getblock", bh],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True,
                         bufsize=0)
    b.stdin.close()
    data = json.load(b.stdout)

    return data['time']

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

# extract the transactions for the blockhash
def printTXs(bh):
    bh = str(bh)
    b = subprocess.Popen([cli, "getblock", bh],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True,
                         bufsize=0)
    b.stdin.close()
    data = json.load(b.stdout)

    for t in data['tx']:
        print ("    ** TX : " + t)
        b2 = subprocess.Popen([cli, "getrawtransaction", t],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True,
                             bufsize=0)
        b2.stdin.close()

        for line in b2.stdout:
            rawTx = line.strip()
            b3 = subprocess.Popen([cli, "decoderawtransaction", rawTx],
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  universal_newlines=True,
                                  bufsize=0)
            b3.stdin.close()
            rtxj = json.load(b3.stdout)
            #print (rtxj)
            #print (rtxj['vin'])
            #print(rtxj['vin'][0])
            for k in rtxj['vin']:
                if "coinbase" in k:
                    print ("    from : fee") # +k['coinbase'])
                if "txid" in k:
                    # get the vouts of the vin...
                    #print ("    < tx in: " +k['txid'] + " (" +str(k['vout'])+ ")")
                    b22 = subprocess.Popen([cli, "getrawtransaction", str(k['txid'])],
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          universal_newlines=True,
                                          bufsize=0)
                    b22.stdin.close()

                    for line in b22.stdout:
                        rawTxin = line.strip()

                        try:
                            b33 = subprocess.Popen([cli, "decoderawtransaction", rawTxin],
                                                  stdin=subprocess.PIPE,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  universal_newlines=True,
                                                  bufsize=0)
                            b33.stdin.close()
                            rtxjin = json.load(b33.stdout)

                            for kk in rtxjin['vout']:
                                if kk['n'] == k['vout']:
                                    v = kk['value']
                                    for w in kk['scriptPubKey']['addresses']:
                                        print("    from  : " + w)
                                    print("    amount: " + str(v))
                        except:
                            print(" E R R O R: ", sys.exc_info()[0])
                            print(" E R R O R: ", sys.exc_info()[1])
                            #print (" E R R O R: transaction maybe too big?")
                            print (" E R R O R: "+rawTxin[:35]+"...")



            for k in rtxj['vout']:
                v = k['value']
                for w in k['scriptPubKey']['addresses']:
                    print ("          > to: " +w)
                print ("          > value: "+str(v))
            print ("")



print(" ____   ___   ____ _____ ____ ___ ___ _   _")
print("|  _ \ / _ \ / ___| ____/ ___/ _ \_ _| \ | |")
print("| | | | | | | |  _|  _|| |  | | | | ||  \| |")
print("| |_| | |_| | |_| | |__| |__| |_| | || |\  |")
print('|____/ \___/ \____|_____\____\___/___|_| \_|')
print("")
print("Find block to date, by _nformant")
print("")


if len(sys.argv) == 2:
    if sys.argv[1] == "-h":
        print('No start time defined, stopping...')
        print("add and argument like this: ")
        print("getBlockOfTime.py \"2021-03-02 20:08:00\"")
        sys.exit()

if len(sys.argv) == 1:
   print('No start time defined, stopping...')
   print("add and argument like this: ")
   print("getBlockOfTime.py \"2021-03-02 20:08:00\"")

   sys.exit()


if len(sys.argv) == 2:
    checkDate = sys.argv[1]
    #print ("checkdate: "+str(checkDate))

currentBlock = getStartBlock()

"""
if len(sys.argv) == 1:
   print('No start block defined, fetching best...')
   currentBlock = getStartBlock()

if len(sys.argv) == 2:
    currentBlock = sys.argv[1]
"""

#print("Starting with block: " + currentBlock)
l = 0
score = 9999999999
bestBlock = currentBlock

first_time = datetime.strptime(checkDate, '%Y-%m-%d %H:%M:%S')
print("Goal: " +str(first_time))
while l < i:
    currentHash = getBlockHash(currentBlock)
    nonce = getNonce(currentHash)
    time = getTime(currentHash)
    type = "(non AuxPoW) "
    # nonce is always 0 for AuxPoW blocks
    if nonce == 0:
        type = "(AuxPoW) "
    #print("BLOCK " + type + str(currentBlock) + ": " + currentHash)


    #print(time)

    later_time = datetime.utcfromtimestamp(time)



    difference = later_time - first_time
    seconds_in_day = 24 * 60 * 60
    calc = divmod(difference.days * seconds_in_day + difference.seconds, 60)
    #minutes (=blocks)
    #print (calc[0])
    #seconds
    #print(calc[1])
    if abs((calc[0]*60)+calc[1]) < score:
        score = abs((calc[0]*60)+calc[1])
        bestBlock = currentBlock
        print("BLOCK : " + str(currentBlock))
        print("HASH  : " + currentHash)
        print("TIME  : " + str(datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')))
        print("SCORE : " + str(score))
        print("")


    #print(divmod(difference.days * seconds_in_day + difference.seconds, 60))
    r = calc[0]
    # 9 = accuracy when to stop (diff in sec.)
    if calc[1] > 9:
        r = r+1

    currentBlock = int(currentBlock) - r
    l = l + 1

print ("###############################")
print (" B E S T  B L O C K:  "+str(bestBlock))
print ("###############################")
