#!/usr/bin/env python2

import csv
import os


class Budget(object):
    
    # Indices to the transaction lists
    DATE = 0
    COMMENT = 1
    AMOUNT = 2
    ACTION = 3
    
    ADD = 'ADD'
    SUB = 'SUB'

    def __init__(self, filename=None):
        # A dictionary of categories
        # filled with a list of transactions
        # Example:
        # {
        #     'Groceries':[
        #         ['-1', 'Initial amount', 100.00, Budget.ADD],
        #         ['20101112', 'Wegmans', 15.67, Budget.SUB],
        #         ['20101118', 'Wegmans', 20.12, Budget.SUB]
        #     ]
        # }
        self._categories = {}
        self._filename = filename
        if filename:
            with open(filename) as file_:
                reader = csv.reader(file_)
                for row in reader:
                    self._add_transaction(category=row[0], date=row[1],
                        comment=row[2], amount=float(row[3]), action=row[4])
        self._mark_changed(False)

    def has_filename(self):
        return True if self._filename else False
  
    def get_name(self):
        return os.path.basename(self._filename) if self._filename else None
  
    def save(self, filename=None):
        if filename:
            if not filename.endswith('.dvy'):
                filename = filename + '.dvy'
            self._filename = filename
        writer = csv.writer(open(self._filename, 'w'))
        writer.writerows(self._to_csv())
        self._mark_changed(False)

    def combine(self, budget, date):
        for category in budget.categories():
            self._add_transaction(category=category, date=date,
                comment='From ' + budget.get_name(),
                    amount=budget.amount(category), action=Budget.ADD)
        self._mark_changed()
  
    def add_category(self, category, amount):
        if category not in self._categories:
            self._add_transaction(category=category, date='-1',
                comment='Initial amount', amount=amount, action=Budget.ADD)

    def rename_category(self, old, new):
        if old in self._categories:
            self._categories[new] = self._categories[old]
            del self._categories[old]
            self._mark_changed()
  
    def remove_category(self, category):
        if category in self._categories:
            del self._categories[category]
            self._mark_changed()
  
    def delete_transaction(self, category, date, amount, action, comment):
        transactions = self._categories[category]
        to_delete = [date, amount, action, comment]
        for index, transaction in enumerate(transactions):
            if transaction == to_delete:
                del self._categories[category][index]
                self._mark_changed()
                break
  
    def delete_transaction_at_index(self, category, index):
        if category in self._categories:
            del self._categories[category][index]
            self._mark_changed()
  
    def categories(self):
        return sorted(self._categories.keys())
    
    def transactions(self, category):
        return self._categories.get(category, [])
  
    def amount(self, category):
        try:
            amount = 0
            for transaction in self._categories[category]:
                if transaction[Budget.ACTION] == Budget.ADD:
                    amount += transaction[Budget.AMOUNT]
                elif transaction[Budget.ACTION] == Budget.SUB:
                    amount -= transaction[Budget.AMOUNT]
            return amount
        except KeyError:
            return 0
  
    def put_in(self, category, date, comment, amount):
        self._add_transaction(category=category, date=date, amount=amount,
            action=Budget.ADD, comment=comment)
  
    def take_out(self, category, date, comment, amount):
        self._add_transaction(category=category, date=date, amount=amount,
            action=Budget.SUB, comment=comment)
  
    def last_added(self, category):
        try:
            amount = 0
            for transaction in self._categories[category]:
                if transaction[Budget.ACTION] == Budget.ADD:
                    amount = transaction[Budget.AMOUNT]
            return amount
        except KeyError:
            return 0
  
    def last_removed(self, category):
        try:
            amount = 0
            for transaction in self._categories[category]:
                if transaction[Budget.ACTION] == Budget.SUB:
                    amount = transaction[Budget.AMOUNT]
            return amount
        except KeyError:
            return 0

    def total(self):
        amount = 0
        for category in list(self._categories.keys()):
            amount += self.amount(category)
        return amount

    def _add_transaction(self, category, date, comment, amount, action):
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append([date, comment, amount, action])
        for category, transactions in list(self._categories.items()):
            transactions.sort()
        self._mark_changed()

    def _mark_changed(self, changed=True):
        self.changed = changed
  
    def _to_csv(self):
        data = []
        for category, transactions in list(self._categories.items()):
            for transaction in transactions:
                line = [category] + transaction
                data.append(line)
        return data


def create_example_budget():
    budget = Budget()
    budget.add_category('Auto', 50.00)
    budget.add_category('Electric', 25.00)
    budget.add_category('Groceries', 60.00)
    budget.add_category('Medical', 100.00)
    budget.add_category('Misc', 10.00)
    budget.add_category('Phone', 30.00)
    budget.add_category('Rent', 200.00)
    budget.add_category('Savings', 15.00)
    budget.add_category('Water', 10.00)
    return budget
