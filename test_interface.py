from Contract.LendingInterface import *
import pytest

def test_initialization():
    assert contract_address[0:2] == '0x'

def test_account_creation():
    test_add = create_account('pass','john',"True")
    assert login(test_add, 'pass')[0] == True

def test_logout():
    test_add = create_account('pass','john',"True")
    login(test_add, 'pass')
    logout(test_add)
    assert withdraw(test_add, 100) == False

    
def test_check_balance():
    test_add = create_account('pass','john',"True")
    login(test_add, 'pass')
    deposit(test_add, 50)
    assert check_balance(test_add) == 50
        
def test_check_withdraw():
    test_add = create_account('pass','john',"True")
    login(test_add, 'pass')
    deposit(test_add, 50)
    withdraw(test_add, 50)
    assert check_balance(test_add) == 0