import numpy as np
from web3 import Web3 
from matplotlib import pyplot as plt

# custom package
# from ABmods.utils import WEB3 as w3
w3 = Web3(Web3.WebsocketProvider("wss://wsapi.fantom.network/"))

# current block
bn = w3.eth.get_block_number()
print('current block %i'%bn)

## API calls
def make_apicall(call):
    """ api request wrapper
    """
    import requests
    return requests.get(call).json()['result']

def get_contract(addr):
    """ 
    given address
    returns web3 contract 
    """
    call = "https://api.ftmscan.com/api?module=contract&action=getabi&"
    call += "address=%s&apikey=8QR98N45S6A5H46QP1MN39P6PHBV47QRGY"%(addr)
    abi = make_apicall(call)
    return w3.eth.contract(address=addr, abi=abi)




## data collection
""" 
@ improve time window here:
    only need to analyze data from recent 1.8 years
"""
def call_allblocks(contract_fn,delta_blocknums=10**5,min_block=27721838,current_block=None,vv=False):
    """
    calls contract_fn on all blocks 
        contract read method
    delta_blocknums: stepsize 
        backsup in time, untill error (contract init)
        (checking all blocks takes too long) 
    min_block: earliest block. 27721838 is inception of yearn btc vault
        
    """
    data = []
    bn = current_block or w3.eth.get_block_number() # current block num
    while True:
        if vv: print(bn)
        bn -= delta_blocknums
        try:
            assert bn>=min_block
            datum = contract_fn.call(block_identifier=bn)
            data.append(datum)
        except:
            break
    data.reverse()
    return data


# analysis tools

def ma(X,w):
    'moving avg'
    X = np.array(X)
    Z = np.zeros(len(X)-w)
    for idx in range(len(X)-w):
        Z[idx] = X[idx:idx+w].mean()
    return Z

# useful vars

yearnVaults = {
    # fantom addresses
    "btc":"0xd817A100AB8A29fE3DBd925c2EB489D67F758DA9",
    "eth":"0xCe2Fc0bDc18BD6a4d9A725791A3DEe33F3a23BB7",
    'wftm':"0x0DEC85e74A92c52b7F708c4B10207D9560CEFaf0",
    "usdc":"0xEF0210eB96c7EB36AF8ed1c20306462764935607",
    "usdt":"0x148c05caf1Bb09B5670f00D511718f733C54bC4c",
    "mim":"0x0A0b23D9786963DE69CB2447dC125c49929419d8",
    "dai":"0x637eC617c86D24E421328e6CAEa1d92114892439",
    "yfi":"0x2C850cceD00ce2b14AA9D658b7Cad5dF659493Db",    

    "boo":"0x0fBbf9848D969776a5Eb842EdAfAf29ef4467698",
    "frax":"0x357ca46da26E1EefC195287ce9D838A6D5023ef3",
    "geist":"0xF137D22d7B23eeB1950B3e19d1f578c053ed9715",
    "crv":"0x0446acaB3e0242fCf33Aa526f1c95a88068d5042",    
    "spell":"0xD3c19eB022CAC706c898D60d756bf1535d605e1d",
    "dola":"0x1b48641D8251c3E84ecbe3f2bD76B3701401906D",
    "link":"0xf2d323621785A066E64282d2B407eAc79cC04966",
    
    "tripool":"0xCbCaF8cB8cbeAFA927ECEE0c5C56560F83E9B7D9"
}