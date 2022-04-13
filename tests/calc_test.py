from hashlib import new
import pytest
from app.calculations import add, BankAccount

# name your test function test_xxx


@pytest.fixture
def zero_bank_account():
    return BankAccount(0)


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected", [(5, 3, 8), (1, 1, 2), (10, 20, 30)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 4) == 55
