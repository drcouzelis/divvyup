#!/usr/bin/env python

import datetime

import budget2
import version


def create_example_budget():
    budget = budget2.Budget()
    budget.add_category('Auto', 50.00)
    category = budget.category('Auto')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -25.00, 'Gas'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), -5.00, 'Oil'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), -3.00, 'Air freshener'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 5.00, 'Paycheck'))
    budget.add_category('Electric', 25.00)
    category = budget.category('Electric')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -20.00, 'Bill'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 10.00, 'Paycheck'))
    budget.add_category('Food', 60.00)
    category = budget.category('Food')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -35.79, 'Grocery store'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), -5.00, 'Fast food'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), -1.50, 'Soft drink'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 40.00, 'Paycheck'))
    budget.add_category('Medical', 100.00)
    category = budget.category('Medical')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -80.00, 'Yearly checkup'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 5.00, 'Paycheck'))
    budget.add_category('Misc', 10.00)
    category = budget.category('Misc')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -6.00, 'Game'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), -3.00, 'Cleaning supplies'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 5.00, 'Paycheck'))
    budget.add_category('Phone', 30.00)
    category = budget.category('Phone')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -28.50, 'Bill'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 15.00, 'Paycheck'))
    budget.add_category('Rent', 200.00)
    category = budget.category('Rent')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -200, 'Monthly rent'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 100.00, 'Paycheck'))
    budget.add_category('Savings', 15.00)
    category = budget.category('Savings')
    category.add_transaction(budget2.Transaction(datetime.date.today(), 5.00, 'Paycheck'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 25.00, 'Birthday'))
    budget.add_category('Water', 10.00)
    category = budget.category('Water')
    category.add_transaction(budget2.Transaction(datetime.date.today(), -9.30, 'Bill'))
    category.add_transaction(budget2.Transaction(datetime.date.today(), 5.00, 'Paycheck'))
    return budget


budget_ = create_example_budget()
print(str(budget_))
with open('/home/couzelis/tmp/test.dvy', 'w') as file_:
    budget2.write(budget_, file_)
print('---------------------------')
with open('/home/couzelis/tmp/test.dvy') as file_:
    budget_ = budget2.read(file_)
print(str(budget_))
print('Last added to Savings: ' + str(budget_.category('Savings').last_added()))
print('Last removed from Food: ' + str(budget_.category('Food').last_removed()))
