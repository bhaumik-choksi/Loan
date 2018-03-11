from flask import Flask, render_template, url_for, request, redirect, flash, session
import sys, math

import web3
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

from NeuralEngine.Predictor import *

app = Flask(__name__)

# Blockchain part #

# Run-only-once-in-the-start part begins
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

# Run-only-once-in-the-start part ends
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
    history = kwargs['history']

    return "~".join([name, age, job, gender, marr_status, liab, housing, res_since, status_ca, duration, purpose,
                     cred_amt, sav_act, emp_since, inst_rate, debtors, _property, plans, exist_cred, phone, foreign,
                     category, confidence, history])


def desquishify(compressed_string):
    s = compressed_string.split('~')
    return {
        'name': s[0], 'age': s[1], 'job': s[2],
        'gender': s[3], 'marr_status': s[4], 'liab': s[5],
        'housing': s[6], 'res_since': s[7], 'status_ca': s[8],
        'duration': s[9], 'purpose': s[10], 'cred_amt': s[11],
        'sav_act': s[12], 'emp_since': s[13], 'inst_rate': s[14],
        'debtors': s[15], '_property': s[16], 'plans': s[17],
        'exist_cred': s[18], 'phone': s[19], 'foreign': s[20],
        'category': s[21], 'confidence': s[22], 'history': s[23]
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


# TODO: Remove this test script later
# add = create_account("foo", "foo", borrower="True")
# print(login(add, "foo"))
# print("Login done")
# print("Creating application", create_application(add, 10, 1, 100, squishify(name='Alisha', age='21', job='wtf',
#                                                                             gender='f', marr_status='blh', liab='hh',
#                                                                             housing='ff', res_since='fff',
#                                                                             status_ca='dd', duration='222',
#                                                                             purpose='education', cred_amt='2255',
#                                                                             sav_act='44444', emp_since='5',
#                                                                             inst_rate='11', debtors='2',
#                                                                             _property='fds',
#                                                                             plans='22', exist_cred='9', phone='yes',
#                                                                             foreign='no')))



@app.route("/")
def main():
    return render_template('index.html')


@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Sign Up
        if request.form['btn'] == 'Sign Up':
            name = request.form['su_name']
            password = request.form['su_password']
            borrower = request.form['client_type']  # False for investors, True for borrowers

            account_address = create_account(password, name, borrower)

            return render_template('signup.html', account_address=account_address)

        # Login
        else:
            account_address = request.form['l_acc_add']
            password = request.form['l_password']

            success, client_type = login(account_address, password)

            if success:
                session['logged_in'] = True
                session['account_address'] = account_address
                session['client_type'] = client_type
                return (redirect(url_for('inv_dashboard_open_apps'))) if client_type == 'investor' else (
                    redirect(url_for('appl_dashboard_new_app')))
            else:
                return render_template('signup.html', error_l_pass="Invalid credentials.")

    return render_template('signup.html', account_address=None)


@app.route("/signout/")
def signout():
    logout(session['account_address'])
    session.clear()
    return redirect(url_for('main'))


@app.route("/inv_dashboard/open_apps/")
def inv_dashboard_open_apps():
    apps = view_open_applications()
    napps = len(apps)
    to_hide = 0
    if napps % 3 == 1:  # get number of blank cards
        to_hide = 2
    elif napps % 3 == 2:
        to_hide = 1
    ndecks = math.ceil(napps / 3)  # for 3 cards per deck
    return render_template('inv_dashboard.html', apps=apps, ndecks=ndecks, to_hide=to_hide, tab='open_apps')


@app.route("/inv_dashboard/profile/", methods=['GET', 'POST'])
def inv_dashboard_profile():
    if request.method == 'POST':
        # Deposit
        if request.form['transactBtn'] == 'Deposit':
            success = deposit(session['account_address'], request.form['deposit_amt'])
            msg = 'Transaction successful' if success else 'Transaction failed'
            balance = check_balance(session['account_address'])
            return render_template('inv_dashboard.html', balance=balance, tab='profile', deposit_msg=msg)

        # Withdraw
        else:
            success = withdraw(session['account_address'], request.form['withdraw_amt'])
            msg = 'Transaction successful' if success else 'Transaction failed'
            balance = check_balance(session['account_address'])
            return render_template('inv_dashboard.html', balance=balance, tab='profile', withdraw_msg=msg)

    return render_template('inv_dashboard.html', balance=check_balance(session['account_address']), tab='profile')


@app.route("/inv_dashboard/my_loan/", methods=['GET', 'POST'])
def inv_dashboard_my_loan():
    loan = view_my_loan(session['account_address'], session['client_type'])
    if not loan:
        loan = ""
    return render_template('inv_dashboard.html', loan=loan, tab='my_loan')


@app.route("/view_app/", methods=['GET', 'POST'])
def view_app():
    app_id = int(request.args.get('app_id', None))
    app = view_application_by_id(app_id)

    if request.method == 'POST':
        success = grant_loan(session['account_address'], app_id)
        if success:
            return redirect(url_for('inv_dashboard_my_loan', tab='my_loan'))
        else:
            return render_template('view_app.html', app=app)

    return render_template('view_app.html', app=app)


@app.route("/appl_dashboard/new_app", methods=['GET', 'POST'])
def appl_dashboard_new_app():
    if request.method == 'POST':

        # mapping from 0, 1, 2 to actual value
        jobs = {'A171': 'Unemployed/ Unskilled - non-resident', 'A172': 'Unskilled - resident',
                'A173': 'Skilled employee / Official',
                'A174': 'Management/ Self-employed/ Highly qualified employee/ Officer'}
        genders = {'0': 'Male', '1': 'Female'}
        marr_statuses = {'1': 'Married', '2': 'Single', '3': 'Divorced/ Separated', '4': 'Widowed'}
        housings = {'A151': 'Rent', 'A152': 'Own', 'A153': 'For free'}
        status_cas = {'A11': 'Less than 0', 'A12': 'Between 0 and 200', 'A13': 'More than 200',
                      'A14': 'No checking account'}
        purposes = {'A40': 'Car (new)', 'A41': 'Car (used)', 'A42': 'Furniture/ Equipment', 'A43': 'Radio/ Television',
                    'A44': 'Domestic appliances', 'A45': 'Repairs', 'A46': 'Education',
                    'A48': 'Retraining', 'A49': 'Business', 'A410': 'Others'}
        sav_acts = {'A61': 'Less than 100', 'A62': 'Between 100 and 500', 'A63': 'Between 500 and 1000',
                    'A64': 'More than 1000', 'A65': 'Unknown/ No savings account'}
        emp_sinces = {'A71': 'Unemployed', 'A72': 'Less than 1 year', 'A73': 'Between 1 and 4 years',
                      'A74': 'Between 4 and 7 years', 'A75': 'More than 7 years'}
        debtorss = {'A101': 'None', 'A102': 'Co-applicant', 'A103': 'Guarantor'}
        propertys = {'A121': 'Real estate', 'A122': 'Life Insurance', 'A123': 'Car or other',
                     'A124': 'Unknown/ No property'}
        planss = {'A141': 'Bank', 'A142': 'Stores', 'A143': 'None'}
        phones = {'A191': 'Yes, under my name', 'A192': 'No'}
        foreigns = {'A201': 'Yes', 'A202': 'No'}
        historys = {'A30': 'No credits taken', 'A31': 'All credits paid back duly',
                    'A32': 'Existing credits paid back duly till now', 'A33': 'Delay in paying off in the past',
                    'A34': 'Critical account'}

        status_sex = ''
        if request.form['gender'] == '0' and request.form['marr_status'] == '3':
            status_sex = 'A91'
        elif request.form['gender'] == '1' and (
                        request.form['marr_status'] == '3' or request.form['marr_status'] == '1'):
            status_sex = 'A92'
        elif request.form['gender'] == '0' and request.form['marr_status'] == '2':
            status_sex = 'A93'
        elif request.form['gender'] == '0' and (
                        request.form['marr_status'] == '4' or request.form['marr_status'] == '1'):
            status_sex = 'A94'
        elif request.form['gender'] == '1' and request.form['marr_status'] == '2':
            status_sex = 'A92'
        else:
            status_sex = 'A92'

        name = request.form['name']
        age = request.form['age']
        job = jobs[request.form['job']]
        gender = genders[request.form['gender']]
        marr_status = marr_statuses[request.form['marr_status']]
        liab = request.form['liab']
        housing = housings[request.form['housing']]
        res_since = request.form['res_since']
        status_ca = status_cas[request.form['status_ca']]
        duration = request.form['duration']
        purpose = purposes[request.form['purpose']]
        cred_amt = request.form['cred_amt']
        sav_act = sav_acts[request.form['sav_act']]
        emp_since = emp_sinces[request.form['emp_since']]
        inst_rate = request.form['inst_rate']
        debtors = debtorss[request.form['debtors']]
        _property = propertys[request.form['property']]
        plans = planss[request.form['plans']]
        exist_cred = request.form['exist_cred']
        phone = phones[request.form['phone']]
        foreign = foreigns[request.form['foreign']]
        history = historys[request.form['history']]

        predictor = Predictor()

        print("NN Processing")

        raw_op = predictor.predict(status_of_account=request.form['status_ca'], duration=request.form['duration'],
                                   history=request.form['history'],
                                   purpose=request.form['purpose'], amount=request.form['cred_amt'],
                                   saving_bonds=request.form['sav_act'],
                                   employment=request.form['emp_since'], rate=request.form['inst_rate'],
                                   status_sex=status_sex, other_coap=request.form['debtors'],
                                   resi_since=request.form['res_since'],
                                   property=request.form['property'], age=request.form['age'],
                                   other_plans=request.form['plans'],
                                   housing=request.form['housing'],
                                   existing_credits=request.form['exist_cred'],
                                   job=request.form['job'], liability=request.form['liab'],
                                   telephone=request.form['phone'],
                                   foreign=request.form['foreign'])

        print("Raw output from NN", raw_op)

        otherData = squishify(name=name, age=age, job=job, gender=gender, marr_status=marr_status,
                              liab=liab, housing=housing, res_since=res_since, status_ca=status_ca,
                              duration=duration, purpose=purpose, cred_amt=cred_amt,
                              sav_act=sav_act, emp_since=emp_since, inst_rate=inst_rate, debtors=debtors,
                              _property=_property, plans=plans, exist_cred=exist_cred, phone=phone, foreign=foreign,
                              category=raw_op['category'], confidence=str(raw_op['confidence']), history=history)

        success = create_application(session['account_address'], int(duration), int(inst_rate), int(cred_amt),
                                     otherData)

        if success:
            return render_template('appl_dashboard.html', balance=check_balance(session['account_address']), tab='profile')
        return render_template('appl_dashboard.html', tab='new_app')

    return render_template('appl_dashboard.html', tab='new_app')


@app.route("/appl_dashboard/profile/", methods=['GET', 'POST'])
def appl_dashboard_profile():
    if request.method == 'POST':
        # Deposit
        if request.form['transactBtn'] == 'Deposit':
            success = deposit(session['account_address'], request.form['deposit_amt'])
            msg = 'Transaction successful' if success else 'Transaction failed'
            balance = check_balance(session['account_address'])
            return render_template('appl_dashboard.html', balance=balance, tab='profile', deposit_msg=msg)

        # Withdraw
        else:
            success = withdraw(session['account_address'], request.form['withdraw_amt'])
            msg = 'Transaction successful' if success else 'Transaction failed'
            balance = check_balance(session['account_address'])
            return render_template('appl_dashboard.html', balance=balance, tab='profile', withdraw_msg=msg)

    return render_template('appl_dashboard.html', balance=check_balance(session['account_address']), tab='profile')


@app.route("/appl_dashboard/my_loan", methods=['GET', 'POST'])
def appl_dashboard_my_loan():
    loan = view_my_loan(session['account_address'], session['client_type'])
    if not loan:
        loan = ""

    # TODO: Display History in view application

    amount_with_interest, t_since_last_pay = estimate_interest(session['account_address'], session['client_type'])

    if request.method == 'POST':
        success = repay_loan(session['account_address'], request.form['amount'])
        if success:
            msg = 'Transaction successful'
            return render_template('appl_dashboard.html', loan=loan, msg=msg, amount_with_interest=amount_with_interest, t_since_last_pay=t_since_last_pay, tab='my_loan')
        else:
            msg = 'Transaction failed'
            return render_template('appl_dashboard.html', loan=loan, msg=msg, amount_with_interest=amount_with_interest, t_since_last_pay=t_since_last_pay, tab='my_loan')

    return render_template('appl_dashboard.html', amount_with_interest=amount_with_interest, t_since_last_pay=t_since_last_pay, loan=loan, tab='my_loan')


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(debug=True)
