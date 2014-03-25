#!/usr/bin/env python

import copy

import budget2


class Version:
    def __init__(self, document):
        self.document = document
        self._commands = list()
        self._currcommand = 0
        self._savedcommand = 0

    def apply(self, command):
        command.document = self.document
        self._commands.append(command)
        self.redo()
        # Delete any commands that come after this one
        self._commands = self._commands[:self._currcommand]

    def undo(self):
        if self.can_undo():
            self._commands[self._currcommand - 1].undo()
            self._currcommand -= 1

    def redo(self):
        if self.can_redo():
            self._currcommand += 1
            self._commands[self._currcommand - 1].apply()

    def can_undo(self):
        return True if self._currcommand > 0 else False

    def can_redo(self):
        return True if self.currcommand < len(self._commands) else False


class BudgetCommand:
    def __init__(self, budget):
        self.budget = budget

    def apply(self):
        pass

    def undo(self):
        pass


class AddCategory (BudgetCommand):
    def __init__(self, budget, category, amount):
        super().__init__(budget)
        self._category = category
        self._amount = amount

    def apply(self):
        self.budget.add_category(self._category, self._amount)

    def undo(self):
        self.budget.remove_category(self._category)


class RemoveCategory (BudgetCommand):
    def __init__(self, budget, category):
        super().__init__(budget)
        self._category = category
        self._transactions = None

    def apply(self):
        # Save the transactions before removing them
        self._transactions = copy.copy(self.budget._categories[self._category])
        self.budget.remove_category(self._category)

    def undo(self):
        for transaction in self._transactions:
            self.budget.add_transaction(self._category, *transaction)


class RenameCategory (BudgetCommand):
    def __init__(self, budget, oldname, newname):
        super().__init__(budget)
        self._old = oldname
        self._new = newname

    def apply(self):
        self.budget.rename_category(self._old, self._new)

    def undo(self):
        self.budget.rename_category(self._new, self._old)


class AddMoney (BudgetCommand):
    def __init__(self, budget, category, date, comment, amount):
        super().__init__(budget)
        self._category = category
        self._date = date
        self._comment = comment
        self._amount = amount

    def apply(self):
        self.budget.put_in(self._category, self._date, self._comment,
                self._amount)

    def undo(self):
        self.budget.delete_transaction(self._category, self._date,
                self._amount, budget.Budget.ADD, self._comment)


class RemoveMoney (BudgetCommand):
    def __init__(self, budget, category, date, comment, amount):
        super().__init__(budget)
        self._category = category
        self._date = date
        self._comment = comment
        self._amount = amount

    def apply(self):
        self.budget.take_out(self._category, self._date, self._comment,
                self._amount)

    def undo(self):
        self.budget.delete_transaction(self._category, self._date,
                self._amount, budget.Budget.SUB, self._comment)


class ChangeDate (BudgetCommand):
    def __init__(self, budget, category, olddate, newdate):
        super().__init__(budget)
        self._category = category
        self._old = olddate
        self._new = newdate

    def apply(self):
        pass

    def undo(self):
        pass


class DeleteTransaction (BudgetCommand):
    def __init__(self, budget, category, date, comment, amount, action):
        super().__init__(budget)
        self._category = category
        self._date = date
        self._comment = comment
        self._amount = amount
        self._action = action

    def apply(self):
        self.budget.delete_transaction(self._category, self._date,
                self._amount, self._action, self._comment)

    def undo(self):
        self.budget._add_transaction(self._category, self._date, self._comment,
                self._amount, self._action)


class Combine (BudgetCommand):
    def __init__(self, budget, other, date):
        super().__init__(budget)
        self._other = other
        self._date = date

    def apply(self):
        self.budget.combine(self._other, self._date)

    def undo(self):
        for category in self._other._categories:
            for t in category:
                self.budget.delete_transaction(category, self._date,
                        t[budget.Budget.AMOUNT], t[budget.Budget.ACTION],
                        t[budget.Budget.COMMENT])
