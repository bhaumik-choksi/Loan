import web3
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

src = '''
pragma solidity ^0.4.0;

contract Coin {
    // The keyword "public" makes those variables
    // readable from outside.
    address public minter;
    mapping (address => uint) public balances;


    // Events allow light clients to react on
    // changes efficiently.
    event Sent(address from, address to, uint amount);

    // This is the constructor whose code is
    // run only when the contract is created.
    function Coin() public {
        minter = msg.sender;
    }

    function mint(address receiver, uint amount) public {
        if (msg.sender != minter) return;
        balances[receiver] += amount;
    }

    function send(address receiver, uint amount) public {
        if (balances[msg.sender] < amount) return;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        Sent(msg.sender, receiver, amount);
    }

    function getBalance(address acc) returns (uint){
    return balances[acc];
    }

    function setBalance(address acc, uint amt){
    balances[acc]=amt;
    }

    function greet() constant returns (string) {
    return 'Hail Bhaumik';
    }
}
'''

# Connect to TestRPC
w3 = Web3(web3.providers.rpc.HTTPProvider("http://localhost:8545"))

compiled_sol = compile_source(src)
contract_interface = compiled_sol['<stdin>:Coin']

contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 4100000})
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

contract_address = tx_receipt['contractAddress']

# Note: Store to contract address to avoid deploying new contract on every run
# This will fail if TestRPC is restarted
print("Contract is deployed at the address ", contract_address)

contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

my_contract = contract(contract_address)

print(contract_instance.greet())
# my_contract.transact({'from': w3.eth.accounts[0], 'gas': 4100000}).setBalance(w3.eth.accounts[0], 60)

# my_contract.transact({'from': w3.eth.accounts[0], 'gas': 4100000}).mint(w3.eth.accounts[0], 60)
# my_contract.transact({'from': w3.eth.accounts[0], 'gas': 4100000}).send(w3.eth.accounts[1], 20)
# print(contract_instance.getBalance(w3.eth.accounts[1]))


# print("Latest block is ", w3.eth.getBlock('latest'))
# print(w3.eth.getTransactionFromBlock(1, 0))

loop = True

newacc  = w3.personal.newAccount('harambe')
w3.personal.unlockAccount(newacc, 'shit', 300)

while loop:
    option = int(input("1.Balance Acc 1 2.Mint Acc 1 3.Balance Acc 2 4.Transfer 1 to 2\n"))
    if option == 1:
        print(contract_instance.getBalance(w3.eth.accounts[0]))
    elif option == 2:
        amount = int(input("Enter Amount"))
        my_contract.transact({'from': w3.eth.accounts[0], 'gas': 4100000}).mint(w3.eth.accounts[0], amount)
    elif option == 3:
        print(contract_instance.getBalance(w3.eth.accounts[1]))
    elif option == 4:
        amount = int(input("Enter Amount"))
        w3.eth.sendTransaction({'from': w3.eth.accounts[0], 'to': newacc ,'gas': 4100000, 'value':50000000})
        w3.eth.sendTransaction({'from': newacc, 'to': w3.eth.accounts[1], 'gas': 4100000, 'value': 4000000})
    elif option == 5:
       my_contract.transact({'from': w3.eth.accounts[0], 'gas': 4100000}).mint(newacc, 500)
       print(w3.eth.getBalance(newacc))
    else:
        break

# msg = "Hello World"
# ac = w3.personal.newAccount('t')
# print(w3.personal.listAccounts)
# w3.personal.unlockAccount(ac, 't')
# s = w3.eth.sign(ac,msg)
# print("Signature", s)

