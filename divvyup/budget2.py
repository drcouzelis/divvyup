#!/usr/bin/env python

import copy
import csv
import datetime


def write(budget, file):
    '''Write a budget to a file using the CSV format.'''
    if not file:
        return
    data = list()
    for name, category in sorted(list(budget.categories.items())):
        for transaction in category.transactions:
            date = transaction.date.strftime('%Y%m%d')
            comment = transaction.comment
            amount = '{:.2f}'.format(transaction.amount)
            data.append([name] + [date, comment, amount])
    csv.writer(file).writerows(data)


def read(file):
    '''Return the budget loaded from the file using the CSV format.'''
    if not file:
        return
    budget = Budget()
    for row in csv.reader(file):
        category = row[0]
        transaction = Transaction()
        year = int(row[1][0:4])
        month = int(row[1][4:6])
        day = int(row[1][6:8])
        transaction.date = datetime.date(year, month, day)
        transaction.comment = row[2]
        transaction.amount = float(row[3])
        if category not in budget.categories:
            budget.categories[category] = Category()
        budget.categories[category].transactions.append(transaction)
    return budget


class Budget:
    '''A budget has a list of categories.'''

    def __init__(self):
        '''Create an empty budget.'''
        self.categories = dict()

    def __str__(self):
        '''A nicely formatted string representation of the budget.'''
        formatted = str()
        for name, category in list(self.categories.items()):
            formatted += '{}: {:.2f}\n{}\n'.format(name, category.amount(), \
                    category)
        formatted += 'Total: {:.2f}'.format(self.amount())
        return formatted

    def category(self, name):
        '''Returns the category with the given name.'''
        return self.categories[name]

    def combine(self, other):
        '''Combine all of the categories and transactions from another budget
        into this budget.'''
        for name, transactions in list(other.categories.items()):
            for transaction in transactions:
                self.categories[name].append(copy.copy(transaction))

    def add_category(self, name, amount=float(0)):
        '''Add a category with an an initial amount.'''
        if name not in self.categories:
            self.categories[name] = Category()
            transaction = Transaction()
            transaction.date = datetime.date.today()
            transaction.amount = amount
            transaction.comment = 'Initial amount'
            self.categories[name].transactions.append(transaction)

    def rename_category(self, old, new):
        '''Rename a category. The transactions are untouched.'''
        if old in self.categories:
            self.categories[new] = self.categories[old]
            del self.categories[old]

    def remove_category(self, name):
        '''Remove a category. This will also delete the transactions
        associated with the category.'''
        if name in self.categories:
            del self.categories[name]

    def amount(self):
        '''The amount of money allocated in this budget.'''
        amount = float(0)
        for name, category in self.categories.items():
            amount += category.amount()
        return amount


class Category:
    '''A category has a list of transactions.'''

    def __init__(self):
        '''Create a new empty category to store transactions.'''
        self.transactions = list()

    def __str__(self):
        '''A nicely formatted string representation of the category.'''
        formatted = str()
        first = True
        for transaction in self.transactions:
            if first:
                first = False
            else:
                formatted += '\n'
            formatted += '  ' + str(transaction)
        return formatted

    def add_transaction(self, transaction):
        '''Adds the transaction to the category.'''
        self.transactions.append(transaction)

    def remove_transaction(self, transaction):
        '''Removes the transaction from the category.'''
        for index, other in enumerate(category.transactions):
            if transaction == other:
                del self.transactions[index]
                break

    def last_added(self):
        '''Returns the most recent transaction with a positive amount.'''
        for transaction in reversed(self.transactions):
            if transaction.amount > 0:
                return transaction

    def last_removed(self):
        '''Returns the most recent transaction with a negative amount.'''
        for transaction in reversed(self.transactions):
            if transaction.amount < 0:
                return transaction

    def amount(self):
        '''The amount of money in this category.'''
        amount = float(0)
        for transaction in self.transactions:
            amount += transaction.amount
        return amount


class Transaction:
    '''An addition or removal of money.'''

    def __init__(self, date=None, amount=float(), comment=''):
        '''A transaction has a date, as defined by datetime.date, a floating
        point amount, positive or negative, and a comment string.'''
        self.date = date
        self.amount = amount
        self.comment = comment

    def __str__(self):
        '''A nicely formatted string representation of the transaction.'''
        return '{}, {}, {:.2f}'.format(self.date.strftime('%Y%m%d'), \
                self.comment, self.amount)

    def __eq__(self, other):
        '''Returns true if the two transactions are equivalent.'''
        if self.date == other.date and self.amount == other.amount and \
                self.comment == other.comment:
            return True
        return False
