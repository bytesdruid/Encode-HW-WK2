# Previously funded account is used to fund new account
# My address: BSTDOSCCPYN3AZNRGBX3VO4XBEAH2TKCGKYZPMYIIRNYAFHJZGNASJMOEI
# My private key: cYGCLpViChb078xonSF43x/IUQvdFlI0jPeD30DZCwIMpjdIQn4bsGWxMG+6u5cJAH1NQjKxl7MIRFuAFOnJmg==
# My passphrase: comfort anxiety nuclear citizen below airport leisure smooth public major rose worth mother stamp tribe bitter medal cotton wink wealth like wagon aware abandon witness

from algosdk import *
from algosdk.future.transaction import *
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
import json
import base64

pk_1 = "cYGCLpViChb078xonSF43x/IUQvdFlI0jPeD30DZCwIMpjdIQn4bsGWxMG+6u5cJAH1NQjKxl7MIRFuAFOnJmg=="
sk_1 = mnemonic.to_private_key("comfort anxiety nuclear citizen below airport leisure smooth public major rose worth mother stamp tribe bitter medal cotton wink wealth like wagon aware abandon witness")

#### ACCOUNT GENERATION ####

# creates an account and prints info
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    new_my_address = format(address)
    new_my_private_key = format(private_key)
    new_my_passphrase = format(mnemonic.from_private_key(private_key))
    return[new_my_address, new_my_private_key, new_my_passphrase]

# funds new account
def fund_new_acct(private_key, my_address, new_acct_addr):
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    receiver = new_acct_addr
    note = "Hello World".encode()
    amount = 1000000
    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    #submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# CALLING THE FUNCTIONS #
### This function creates a new account
new_my_address, pk_2, new_my_passphrase = generate_algorand_keypair()
### This function funds the new account with a previously funded testnet account
fund_new_acct("cYGCLpViChb078xonSF43x/IUQvdFlI0jPeD30DZCwIMpjdIQn4bsGWxMG+6u5cJAH1NQjKxl7MIRFuAFOnJmg==", "BSTDOSCCPYN3AZNRGBX3VO4XBEAH2TKCGKYZPMYIIRNYAFHJZGNASJMOEI", new_my_address)

############ Test ################################################################################################################################################

# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics
mnemonic1 = "PASTE your phrase for account 1"
mnemonic2 = "PASTE your phrase for account 2"
mnemonic3 = "PASTE your phrase for account 3"
# never use mnemonics in production code, replace for demo purposes only

# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Specify your node address and token. This must be updated.
# algod_address = ""  # ADD ADDRESS
# algod_token = ""  # ADD TOKEN

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)


#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

print("Account 1 address: {}".format(accounts[1]['pk']))
print("Account 2 address: {}".format(accounts[2]['pk']))
print("Account 3 address: {}".format(accounts[3]['pk']))

# your terminal output should look similar to the following
# Account 1 address: ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ
# Account 2 address: AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4
# Account 3 address: IWR4CLLCN2TIVX2QPVVKVR5ER5OZGMWAV5QB2UIPYMPKBPLJZX4C37C4AA

# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True

# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction

txn = AssetConfigTxn(
    sender=accounts[1]['pk'],
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="LATINUM",
    asset_name="latinum",
    manager=accounts[2]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'],
    url="https://path/to/my/asset/details", 
    decimals=0)
# Sign with secret key of creator
stxn = txn.sign(accounts[1]['sk'])

# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
   
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.

print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
# print("Decoded note: {}".format(base64.b64decode(
#     confirmed_txn["txn"]["txn"]["note"]).decode()))

try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[1]['pk'], asset_id)
    print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
except Exception as e:
    print(e)

# terminal output should be similar to below
# Transaction WVG5HSCU7OIMFHLQGMPJF3NZ56A6FE3DMFUNBUKH73ZUMIU3N3HA confirmed in round 3982822.
# Waiting for confirmation...
# Transaction DDDNZWERVG54J32PLCJQENLC5FAFIFYY6ZSYRY25C3J26TJKJ5IA confirmed in round 3982906.
# Asset ID: 2653870
# {
#     "clawback": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "decimals": 0,
#     "default-frozen": false,
#     "freeze": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "manager": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "metadata-hash": "MTZlZmFhMzkyNGE2ZmQ5ZDNhNDgyNDc5OWE0YWM2NWQ=",
#     "name": "latinum",
#     "reserve": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "total": 1000,
#     "unit-name": "LATINUM",
#     "url": "https://path/to/my/asset/details"
# }
# Asset ID: 2653870
# {
#     "amount": 1000,
#     "asset-id": 2653870,
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "is-frozen": false
# }


# CHANGE MANAGER

# The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
# Keep reserve, freeze, and clawback address same as before, i.e. account 2
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True

# asset_id = 328952;

txn = AssetConfigTxn(
    sender=accounts[2]['pk'],
    sp=params,
    index=asset_id, 
    manager=accounts[1]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'])
# sign by the current manager - Account 2
stxn = txn.sign(accounts[2]['sk'])
# txid = algod_client.send_transaction(stxn)
# print(txid)

# Wait for the transaction to be confirmed
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
 
except Exception as err:
    print(err)
# Check asset info to view change in management. manager should now be account 1
print_created_asset(algod_client, accounts[1]['pk'], asset_id)
# terminal output should be similar to...
# Transaction Y7EYBJNFP7YPGCV7ZD47PMJZHXB2PRT3SZ534M7BZE7G55IMPKUA confirmed in round 3982910.
# Asset ID: 2653870
# {
#     "clawback": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "decimals": 0,
#     "default-frozen": false,
#     "freeze": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "manager": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "metadata-hash": "MTZlZmFhMzkyNGE2ZmQ5ZDNhNDgyNDc5OWE0YWM2NWQ=",
#     "name": "latinum",
#     "reserve": "AK6Q33PDO4RJZQPHEMODC6PUE5AR2UD4FBU6TNEJOU4UR4KC6XL5PWW5K4",
#     "total": 1000,
#     "unit-name": "LATINUM",
#     "url": "https://path/to/my/asset/details"
# }

# OPT-IN

# Check if asset_id is in account 3's asset holdings prior
# to opt-in
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True

account_info = algod_client.account_info(accounts[3]['pk'])
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1    
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break

if not holding:

    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = AssetTransferTxn(
        sender=accounts[3]['pk'],
        sp=params,
        receiver=accounts[3]["pk"],
        amt=0,
        index=asset_id)
    stxn = txn.sign(accounts[3]['sk'])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
 
    except Exception as err:
        print(err)
    # Now check the asset holding for that account.
    # This should now show a holding with a balance of 0.
    print_asset_holding(algod_client, accounts[3]['pk'], asset_id)

# terminal output should look similar to this...

# Transaction ACYWQVRO6XKQNIHHGH7PDIPKPGURES6YA7OCI654PTR75RKTL4FA confirmed in round 3982915.
# Asset ID: 2653870
# {
#     "amount": 0,
#     "asset-id": 2653870,
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "is-frozen": false
# }

# TRANSFER ASSET

# transfer asset of 10 from account 1 to account 3
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True
txn = AssetTransferTxn(
    sender=accounts[1]['pk'],
    sp=params,
    receiver=accounts[3]["pk"],
    amt=10,
    index=asset_id)
stxn = txn.sign(accounts[1]['sk'])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)
# The balance should now be 10.
print_asset_holding(algod_client, accounts[3]['pk'], asset_id)

# terminal output should look similar to this...
# Transaction AYL3FKK6IUWRV2RRCWFBZYO3STX2D74XML6HFWH4EELSDLMLUCCQ confirmed in round 3982920.
# Asset ID: 2653870
# {
#     "amount": 10,
#     "asset-id": 2653870,
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "is-frozen": false
# }

# FREEZE ASSET

params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True
# The freeze address (Account 2) freezes Account 3's latinum holdings.

txn = AssetFreezeTxn(
    sender=accounts[2]['pk'],
    sp=params,
    index=asset_id,
    target=accounts[3]["pk"],
    new_freeze_state=True   
    )
stxn = txn.sign(accounts[2]['sk'])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
except Exception as err:
    print(err)
# The balance should now be 10 with frozen set to true.
print_asset_holding(algod_client, accounts[3]['pk'], asset_id)

# Terminal output should look similar to this wih a frozen value of true...
# Transaction 5NFHUQ4GEQMT4EFPMIIBTHNOX4LS5GQLZRKCKCA2GAUVAS4PAGJQ confirmed in round 3982928.
# Asset ID: 2653870
# {
#     "amount": 10,
#     "asset-id": 2653870,
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "is-frozen": true
# }

# REVOKE ASSET

# The clawback address (Account 2) revokes 10 latinum from Account 3 and places it back with Account 1.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True

# Must be signed by the account that is the Asset's clawback address
txn = AssetTransferTxn(
    sender=accounts[2]['pk'],
    sp=params,
    receiver=accounts[1]["pk"],
    amt=10,
    index=asset_id,
    revocation_target=accounts[3]['pk']
    )
stxn = txn.sign(accounts[2]['sk'])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))      
except Exception as err:
    print(err)
# The balance of account 3 should now be 0.
# account_info = algod_client.account_info(accounts[3]['pk'])
print("Account 3")
print_asset_holding(algod_client, accounts[3]['pk'], asset_id)

# The balance of account 1 should increase by 10 to 1000.
print("Account 1")
print_asset_holding(algod_client, accounts[1]['pk'], asset_id)

# Terminal output should be similar to...
# Transaction 4UFNTECSEBAGJT52XLIBM7BQXHBTXUHLZ2U4M4XTZUAVE4VLKURQ confirmed in round 3982932.
# Account 3
# Asset ID: 2653870
# {
#     "amount": 0,
#     "asset-id": 2653870,
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "is-frozen": true
# }
# Account 1
# Asset ID: 2653870
# {
#     "amount": 1000,
#     "asset-id": 2653870,
#     "creator": "ATTR6RUEHHBHXKUHT4GUOYWNBVDV2GJ5FHUWCSFZLHD55EVKZWOWSM7ABQ",
#     "is-frozen": false
# }

# DESTROY ASSET
# With all assets back in the creator's account,
# the manager (Account 1) destroys the asset.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True

# Asset destroy transaction
txn = AssetConfigTxn(
    sender=accounts[1]['pk'],
    sp=params,
    index=asset_id,
    strict_empty_address_check=False
    )

# Sign with secret key of creator
stxn = txn.sign(accounts[1]['sk'])
# Send the transaction to the network and retrieve the txid.
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))     
except Exception as err:
    print(err)

# Asset was deleted.
try:
    print("Account 3 must do a transaction for an amount of 0, " )
    print("with a close_assets_to to the creator account, to clear it from its accountholdings")
    print("For Account 1, nothing should print after this as the asset is destroyed on the creator account")
   
    print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    print_created_asset(algod_client, accounts[1]['pk'], asset_id)
    # asset_info = algod_client.asset_info(asset_id)
except Exception as e:
    print(e)

# Transaction C7BOB7ZNVIJ477LEAIJYDNXIIFZTY7ETTB3QEV3GWRJ7BGOZMSGA confirmed in round 3983117.
# Account 3 must do a transaction for an amount of 0,
# with a close_assets_to to the creator account, to clear it from its accountholdings
# For Account 1, nothing should print after this if the asset is destroyed on the creator account

