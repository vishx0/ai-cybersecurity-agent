from web3 import Web3
import hashlib

# -----------------------------
# 🔹 CONNECT TO GANACHE
# -----------------------------
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if web3.is_connected():
    print("✅ Connected to blockchain")
else:
    print("❌ Blockchain connection failed")

# -----------------------------
# 🔹 CONTRACT DETAILS (EDIT THIS)
# -----------------------------
contract_address = Web3.to_checksum_address("PASTE_YOUR_CONTRACT_ADDRESS_HERE")

abi = PASTE_YOUR_ABI_HERE

contract = web3.eth.contract(address=contract_address, abi=abi)

# -----------------------------
# 🔹 HASH FUNCTION
# -----------------------------
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# -----------------------------
# 🔹 STORE HASH ON BLOCKCHAIN
# -----------------------------
def store_log_hash(log_data):
    try:
        account = web3.eth.accounts[0]

        log_string = str(log_data)
        log_hash = generate_hash(log_string)

        tx_hash = contract.functions.addLogHash(log_hash).transact({
            "from": account
        })

        web3.eth.wait_for_transaction_receipt(tx_hash)

        return log_hash

    except Exception as e:
        return f"Error: {str(e)}"