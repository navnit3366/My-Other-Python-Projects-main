"""An Account class with different subclasses"""
class AmountError(Exception):
    """A class defining Amount Error"""


    def __init__(self, account, err_msg):
        self.account = account
        self.err_msg = err_msg

    def __str__(self):
        return 'AmountError (' + self.err_msg + ') on ' + str(self.account)



class BalanceError(Exception):
    """Exception for withdrawing above overdraft limit"""


    def __init__(self,account):
        self.account = account

    def __str__(self):
        return 'BalanceError (Withdrawal would exceed '\
               'your overdraft limit) ' + str(self.account)
class Account:
    """An example of model account"""
    acc_count = 0


    @classmethod
    def allowed_acc(cls):
        """class method to monitor amount of account created"""
        cls.acc_count += 1
        print('New account created')

    def __init__(self,acc_no, name, balance, acc_type):
        Account.allowed_acc()
        self.acc_no = acc_no
        self.name = name
        self._balance = balance
        self.acc_type = acc_type

    def __str__(self):
        return f"Account[{self.acc_no}] - {self.name},{self.acc_type} account = {self.balance}"

    def deposit(self, amount):
        """Deposit a given amount"""
        if amount >= 0:
            self._balance += amount
        else:
            raise AmountError(self.__str__(),
                              'Cannot deposit negative amounts')

    def withdraw(self, amount):
        """Withdraw a given amount"""
        if amount < 0:
            raise AmountError(self.__str__(),
                              'Cannot withdraw negative amounts')
        if (self._balance - amount) < 0:
            print('Insufficient funds', self._balance)
        else:
            self._balance -= amount

    @property
    def balance(self):
        """Get available balance"""
        return self._balance


class CurrentAccount(Account):
    """An account that allows overdraft"""
    acc_count = 0


    @classmethod
    def allowed_acc(cls):
        cls.acc_count += 1

    def __init__(self, acc_no, name, balance, ov_limit):
        CurrentAccount.allowed_acc()
        super().__init__(acc_no, name, balance, 'current')
        self.ov_limit = ov_limit

    def withdraw(self, amount):
        if amount < 0:
            raise AmountError(self.__str__(),
                              'Cannot withdraw negative amounts')
        val = self._balance - amount
        if val >= -self.ov_limit:
            self._balance -= amount
        else:
            raise BalanceError(self.__str__())

    def __str__(self):
        return super().__str__() + '(overdraft-limit: ' + str(self.ov_limit) + ')'


class DepositAccount(Account):
    """An account that allows has interest"""
    acc_count = 0


    @classmethod
    def allowed_acc(cls):
        cls.acc_count += 1

    def __init__(self, acc_no, name, balance, int_rate):
        DepositAccount.allowed_acc()
        super().__init__(acc_no, name, balance, 'deposit')
        self.int_rate = int_rate

    def __str__(self):
        return super().__str__() + '(' + str(self.int_rate) + ' interest rate)'


class InvestmentAccount(Account):
    """Account with investment type"""
    acc_count = 0


    @classmethod
    def allowed_acc(cls):
        cls.acc_count += 1

    def __init__(self, acc_no, name, balance, inv_type):
        InvestmentAccount.allowed_acc()
        super().__init__(acc_no, name, balance, 'investment')
        self.inv_type = inv_type

    def __str__(self):
        return super().__str__() + '( safe ' + str(self.inv_type) + ')'


def main():
    """Scope it to __main__"""
    acc1 = DepositAccount('133', 'Dave', 2344, 0.6)
    acc2 = CurrentAccount('344', 'Yoyo', 70000, 10000)
    try:
        acc1.deposit(-1)
    except AmountError as err:
        print(err)

    try:
        print('\nbalance:', acc2.balance)
        acc2.withdraw(80001.00)
        print('\nbalance:', acc2.balance)
    except  BalanceError as err:
        print('\nHandling Exception')
        print(err)

if __name__ == '__main__':
    main()
