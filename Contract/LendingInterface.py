import web3
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

src = open('P2PLending.sol')
src = "\n".join(list(line.replace("\n", "") for line in src))
print("Contract Code Loaded")

w3provider = Web3(web3.providers.rpc.HTTPProvider("http://localhost:8545"))
compiled_sol = compile_source(src)
contract_interface = compiled_sol['<stdin>:P2PLending']

P2PLending_contract = w3provider.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = P2PLending_contract.deploy(transaction={'from': w3provider.eth.accounts[0], 'gas': 4100000})
tx_receipt = w3provider.eth.getTransactionReceipt(tx_hash)

contract_address = tx_receipt['contractAddress']
print("Contract is deployed at the address ", contract_address)

contract_read_interface = w3provider.eth.contract(contract_interface['abi'], contract_address,
                                                  ContractFactoryClass=ConciseContract)
contract_txn_interface = P2PLending_contract(contract_address)


def createAccount(password, name, borrower=True):
    account_address = w3provider.personal.newAccount(password)

    # Give some ether to fund gas for txns
    w3provider.eth.sendTransaction(
        {'from': w3provider.eth.accounts[0], 'to': account_address, 'gas': 4100000, 'value': 50000000})

    # Unlock for 3 seconds to run the create<User> Txns
    w3provider.personal.unlockAccount(account_address, password, 3)

    if borrower:
        contract_txn_interface.call({'from': account_address, 'gas': 4100000}).createBorrower(name)
    else:
        contract_txn_interface.call({'from': account_address, 'gas': 4100000}).createInvestor(name)

    return account_address


def login(address, password):
    try:
        w3provider.personal.unlockAccount(address, password, 3600)
        # TODO: Return customer type from contract for dynamic UI
        # TODO: Store address in session variable
        return [True]
    except:
        return [False]


def logout(address):
    try:
        web3.personal.lockAccount(address)
        # TODO: Destroy the session variable that stores the address
        return True
    except:
        return False


def checkBalance(account_address):
    # TODO: On login, save account_address to global, maybe?
    return contract_txn_interface.call({'from': account_address, 'gas': 4100000}).viewBalance()


def withdraw(account_address, amount):
    try:
        contract_txn_interface.transact({'from': account_address, 'gas': 4100000}).withdraw(int(amount))
        return True
    except:
        return False


def deposit(account_address, amount):
    contract_txn_interface.transact({'from': account_address, 'gas': 4100000}).deposit(int(amount))
    return True


def squishify(*args, **kwargs):
    # TODO: Change this to actually do something
    return "1~2~3~4"


def desquishify(compressed_string):
    # TODO: Change this to actually do something
    return compressed_string.split("~")


def createApplication(account_address, duration, interest_rate, credit_amount, otherData):
    try:
        contract_txn_interface.transact({'from': account_address, 'gas': 4100000}) \
            .createApplication(int(duration), int(interest_rate), int(credit_amount), otherData)
        return True
    except:
        return False


def get_num_applications():
    return contract_txn_interface.call({'from': w3provider.eth.accounts[0], 'gas': 4100000}).getNumApplications()


def get_num_loans():
    return contract_txn_interface.call({'from': w3provider.eth.accounts[0], 'gas': 4100000}).getNumLoans()


add = createAccount(input("Enter Password"), input("Enter name"), borrower=True)
print(login(add, input("Enter Password to Login")))
print("Creating application", createApplication(add, 10, 1, 100, squishify()))
print("Num Loans", get_num_loans())
print("Num Applications", get_num_applications())