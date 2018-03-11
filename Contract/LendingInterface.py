import web3
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

# Run-only-once-in-the-start part begins
src = open('P2PLending.sol')
src = "\n".join(list(line.replace("\n", "") for line in src))
print("Contract Code Loaded")

w3provider = Web3(web3.providers.rpc.HTTPProvider("http://localhost:8545"))
compiled_sol = compile_source(src)
contract_interface = compiled_sol['<stdin>:P2PLending']

P2PLending_contract = w3provider.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = P2PLending_contract.deploy(transaction={'from': w3provider.eth.accounts[0]})
tx_receipt = w3provider.eth.getTransactionReceipt(tx_hash)

contract_address = tx_receipt['contractAddress']
print("Contract is deployed at the address ", contract_address)

contract_read_interface = w3provider.eth.contract(contract_interface['abi'], contract_address,
                                                  ContractFactoryClass=ConciseContract)
contract_txn_interface = P2PLending_contract(contract_address)


# Run-only-once-in-the-start part ends

def create_account(password, name, borrower):
    account_address = w3provider.personal.newAccount(password)

    # Give some ether to fund gas for txns
    w3provider.eth.sendTransaction(
        {'from': w3provider.eth.accounts[0], 'to': account_address, 'value': 50000000})

    # Unlock for 3 seconds to run the create<User> Txns
    w3provider.personal.unlockAccount(account_address, password, 3)

    if borrower == "True":
        contract_txn_interface.transact({'from': account_address}).createBorrower(name)
    else:
        contract_txn_interface.transact({'from': account_address}).createInvestor(name)

    return account_address


def login(account_address, password):
    # TODO: Store address in session variable
    try:
        w3provider.personal.unlockAccount(account_address, password, 3600)
        is_borrower = contract_read_interface.isBorrower(account_address)
        is_investor = contract_read_interface.isInvestor(account_address)
        if is_borrower:
            return [True, "borrower"]
        elif is_investor:
            return [True, "investor"]
        else:
            return [False, "INVALID"]
    except:
        return [False, None]


def logout(account_address):
    try:
        web3.personal.lockAccount(account_address)
        # TODO: Destroy the session variable that stores the address
        return True
    except:
        return False


def check_balance(account_address):
    # TODO: On login, save account_address to global, maybe?
    return contract_txn_interface.call({'from': account_address}).viewBalance()


def withdraw(account_address, amount):
    try:
        contract_txn_interface.transact({'from': account_address}).withdraw(int(amount))
        return True
    except:
        return False


def deposit(account_address, amount):
    contract_txn_interface.transact({'from': account_address}).deposit(int(amount))
    return True


def squishify(*args, **kwargs):
    name = kwargs['name']
    age = kwargs['age']
    job = kwargs['job']
    gender = kwargs['gender']
    marr_status = kwargs['marr_status']
    liab = kwargs['liab']
    housing = kwargs['housing']
    res_since = kwargs['res_since']
    status_ca = kwargs['status_ca']
    duration = kwargs['duration']
    purpose = kwargs['purpose']
    cred_amt = kwargs['cred_amt']
    sav_act = kwargs['sav_act']
    emp_since = kwargs['emp_since']
    inst_rate = kwargs['inst_rate']
    debtors = kwargs['debtors']
    _property = kwargs['_property']
    plans = kwargs['plans']
    exist_cred = kwargs['exist_cred']
    phone = kwargs['phone']
    foreign = kwargs['foreign']
    category = kwargs['category']
    confidence = kwargs['confidence']

    return "~".join([name, age, job, gender, marr_status, liab, housing, res_since, status_ca, duration, purpose,
                     cred_amt, sav_act, emp_since, inst_rate, debtors, _property, plans, exist_cred, phone, foreign,
                     category, confidence])


def desquishify(compressed_string):
    s = compressed_string.split('~')
    return {
        'name': s[0], 'age': s[1], 'job': s[2],
        'gender': s[3], 'marr_status': s[4], 'liab': s[5],
        'housing': s[6], 'res_since': s[7], 'status_ca': s[8],
        'duration': s[9], 'purpose': s[10], 'cred_amt': s[11],
        'sav_act': s[12], 'emp_since': s[13], 'inst_rate': [14],
        'debtors': s[15], '_property': s[16], 'plans': s[17],
        'exist_cred': s[18], 'phone': s[19], 'foreign': s[20],
        'category': s[21], 'confidence': s[22]
    }


def create_application(account_address, duration, interest_rate, credit_amount, otherData):
    try:
        contract_txn_interface.transact({'from': account_address}) \
            .createApplication(int(duration), int(interest_rate), int(credit_amount), otherData)
        return True
    except:
        return False


def get_num_applications():
    return contract_txn_interface.call({'from': w3provider.eth.accounts[0]}).getNumApplications()


def get_num_loans():
    return contract_txn_interface.call({'from': w3provider.eth.accounts[0]}).getNumLoans()


def view_open_applications():
    open_applications = []
    n = get_num_applications()
    for i in range(1, n + 1):
        is_open = contract_read_interface.ifApplicationOpen(i)
        if is_open:
            raw_data = contract_read_interface.getApplicationData(i)
            open_applications.append({
                'application_id': raw_data[0][0],
                'duration': raw_data[0][1],
                'amount': raw_data[0][2],
                'interest_rate': raw_data[0][3],
                # TODO: De-squishify other data
                'other_data': raw_data[1],
                'borrower': raw_data[2]
            })
    return open_applications


def view_open_applications():
    open_applications = []
    n = get_num_applications()
    for i in range(1, n + 1):
        is_open = contract_read_interface.ifApplicationOpen(i)
        if is_open:
            raw_data = contract_read_interface.getApplicationData(i)
            other_data = desquishify(raw_data[1])
            open_applications.append({
                'application_id': raw_data[0][0],
                'duration': raw_data[0][1],
                'amount': raw_data[0][2],
                'interest_rate': raw_data[0][3],
                'name': other_data['name'],
                'purpose': other_data['purpose'],
                'job': other_data['job'],
                'age': other_data['age'],
                'category': other_data['category'],
                'confidence': other_data['confidence'],
                'borrower': raw_data[2]
            })
    return open_applications


def grant_loan(account_address, app_id):
    try:
        contract_txn_interface.transact({'from': account_address}).grantLoan(int(app_id))
        return True
    except:
        return False


def view_my_loan(account_address, userType):
    if userType == "borrower":
        n = get_num_loans()
        for i in range(1, n + 1):
            is_open = contract_read_interface.ifLoanOpen(i)
            if is_open:
                raw_data = contract_read_interface.getLoanData(i)
                if raw_data[1].lower() == account_address.lower():
                    return {
                        'loan_id': raw_data[0][0],
                        'interest_rate': raw_data[0][1],
                        'duration': raw_data[0][2],
                        'principal_amount': raw_data[0][3],
                        'original_amount': raw_data[0][4],
                        'paid_amount': raw_data[0][5],
                        'start_time': raw_data[0][6],
                        'monthly_checkpoint': raw_data[0][7],
                        'application_id': raw_data[0][8],
                        'borrower': raw_data[1],
                        'investor': raw_data[2]
                    }
        return False
    elif userType == "investor":
        n = get_num_loans()
        for i in range(1, n + 1):
            is_open = contract_read_interface.ifLoanOpen(i)
            if is_open:
                raw_data = contract_read_interface.getLoanData(i)
                if raw_data[2].lower() == account_address.lower():
                    return {
                        'loan_id': raw_data[0][0],
                        'interest_rate': raw_data[0][1],
                        'duration': raw_data[0][2],
                        'principal_amount': raw_data[0][3],
                        'original_amount': raw_data[0][4],
                        'paid_amount': raw_data[0][5],
                        'start_time': raw_data[0][6],
                        'monthly_checkpoint': raw_data[0][7],
                        'application_id': raw_data[0][8],
                        'borrower': raw_data[1],
                        'investor': raw_data[2]
                    }
        return False
    else:
        return False


def estimate_interest(account_address, userType):
    # Select how fast you want time to move
    TIME_STEP = {'seconds': 1, 'minutes': 60, 'hours': 3600, 'days': 3600 * 24, 'months': 3600 * 24 * 30}

    if userType == "investor":
        return False
    else:
        loan_data = view_my_loan(account_address, userType)
        if loan_data != False:
            p = loan_data['principal_amount']
            r = loan_data['interest_rate']
            checkpoint = loan_data['monthly_checkpoint']
            start_time = loan_data['start_time']
            n = 12  # n is the number of times interest is compounded annually
            amount_with_interest = p

            # Note that this time is not the actual time, but a timestamp in num_of_seconds
            current_time = contract_read_interface.getTime()
            time_elapsed = (current_time - start_time) / TIME_STEP['seconds']
            t_since_last_payment = time_elapsed - checkpoint

            print(current_time, "Current Time")
            print(start_time, "Start time")
            print(checkpoint, "Checkpoint")
            print(time_elapsed, "Time elapsed")

            if t_since_last_payment != 0:
                amount_with_interest = p * (1 + r / (100 * n)) ** (time_elapsed)
                amount_with_interest = int(amount_with_interest)
                return [int(amount_with_interest), int(t_since_last_payment)]
            else:
                return [int(p), 0]


def repay_loan(account_address, amount):
    try:
        amount_with_interest, months_since_last_checkpoint = estimate_interest(account_address, 'borrower')
        amount = int(amount)  # Typecast for safety B|
        contract_txn_interface.transact({'from': account_address}) \
            .repayLoan(amount, amount_with_interest, months_since_last_checkpoint)
        return True
    except:
        return False


def view_application_by_id(index):
    n = get_num_applications()
    if index > n or index < 1:
        return False
    else:
        raw_data = contract_read_interface.getApplicationData(index)
        return desquishify(raw_data[1])


def view_loan_by_id(index):
    n = get_num_loans()
    if index > n or index < 1:
        return False
    else:
        raw_data = contract_read_interface.getLoanData(index)
        return {
            'loan_id': raw_data[0][0],
            'interest_rate': raw_data[0][1],
            'duration': raw_data[0][2],
            'principal_amount': raw_data[0][3],
            'original_amount': raw_data[0][4],
            'paid_amount': raw_data[0][5],
            'start_time': raw_data[0][6],
            'monthly_checkpoint': raw_data[0][7],
            'application_id': raw_data[0][8],
            'borrower': raw_data[1],
            'investor': raw_data[2]
        }


def get_full_blockchain():
    n = w3provider.eth.blockNumber
    blocks_with_txns = []
    for i in range(10):
        block = w3provider.eth.getBlock(i)
        blocks_with_txns.append(block)

    return blocks_with_txns


def view_my_txns_from_blockchain(account_address):
    n = w3provider.eth.blockNumber
    print(n, "Blocks in the blockchain")
    output = []
    for block_num in range(n):
        txn_count = w3provider.eth.getBlockTransactionCount(block_num)
        for i in range(txn_count):
            raw_data = dict(w3provider.eth.getTransactionFromBlock(block_num, i))
            if raw_data['from'].lower() == account_address.lower() or raw_data['to'].lower() == account_address.lower():
                output.append({
                    'from': raw_data['from'],
                    'to': raw_data['to'],
                    'blockNumber': raw_data['blockNumber'],
                    'hash': raw_data['hash']
                })

    return output


# Tester code below
# bor = create_account("foo", "foo", "True")
# login(bor, "foo")
# print("Creating application", create_application(bor, 24, 5, 100, 'x'))
# print(deposit(bor, 5000), "Deposit")
#
# inv = create_account("bar", "bar", "False")
# login(inv, "bar")
# deposit(inv, 100000)
# print("Granting Loan", grant_loan(inv, 1))

# Create Dummy Applications
# for i in range(5):
#     dummy = create_account("foo", "foo", "True")
#     login(dummy, "foo")
#     create_application(dummy, 24, 5, 100, 'x')
#     print("Dummy Application Created")

#
# amount_with_interest, months_since_last_checkpoint = estimate_interest(bor, 'borrower')
# print(repay_loan(bor, amount_with_interest))
# print(view_my_loan(inv, "investor"))

from NeuralEngine import Trainer, Predictor

# T = Trainer()
# T.train_all_and_save(filename="german.xlsx", epochs=30, batch_size=5)
P = Predictor()
op = P.predict(status_of_account="A11", duration="6", history="A34", purpose="A43", amount="1169", saving_bonds="A65",
               employment="A75", rate="4",
               status_sex="A93", other_coap="A101", resi_since="4", property="A121", age="67", other_plans="A143",
               housing="A152",
               existing_credits="2", job="A173", liability="1", telephone="A192", foreign="A201")
print(op)
