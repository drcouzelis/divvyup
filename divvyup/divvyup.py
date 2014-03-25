#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
import sys
import time
import wx
import wx.html
import __builtin__

import budget
import interface
import undowrapper


# Set the homepath variable to the directory
# where your application is located
__builtin__.__dict__['homepath'] = os.path.abspath(
    os.path.dirname(sys.argv[0]))


version = '0.5'
filetypes = 'DVY files (*.dvy)|*.dvy'


class MainFrame(interface.MainFrameShell):

    def __init__(self, *args, **kwds):
        interface.MainFrameShell.__init__(self, *args, **kwds)
        self.splitwindow.SetMinimumPaneSize(1)
        self.Bind(wx.EVT_SIZE, self.OnSplitterChanged)
        self.Bind(wx.EVT_CLOSE, self.OnFrameClosed)
        # Setup the list of envelopes
        self.category_list.InsertColumn(0, 'Category')
        self.category_list.InsertColumn(1, 'Amount', wx.LIST_FORMAT_RIGHT)
        # Setup the list of transactions
        self.transaction_list.InsertColumn(0, 'Date')
        self.transaction_list.InsertColumn(1, 'Message')
        self.transaction_list.InsertColumn(2, 'Amount', wx.LIST_FORMAT_RIGHT)
        self.transaction_list.InsertColumn(3, 'Action')
        self.OnSplitterChanged(None)
        # Set icons
        icons = wx.IconBundle()
        path = os.path.join(homepath, 'divvyup' + os.sep + 'icons' + os.sep)
        icons.AddIcon(wx.Icon(path + 'divvyup64x64.png', wx.BITMAP_TYPE_PNG))
        icons.AddIcon(wx.Icon(path + 'divvyup48x48.png', wx.BITMAP_TYPE_PNG))
        icons.AddIcon(wx.Icon(path + 'divvyup32x32.png', wx.BITMAP_TYPE_PNG))
        icons.AddIcon(wx.Icon(path + 'divvyup16x16.png', wx.BITMAP_TYPE_PNG))
        self.SetIcons(icons)
        # The current budget
        self.LoadBudget(budget.Budget())
  
    def CurrBudget(self):
        return self.budget_wrapper.curr()
  
    def OnNewBudgetPressed(self, event):
        event.Skip(False)
        warning = 'There are unsaved changes.\n' + \
                  'Are you sure you want to create a new budget?'
        if not self.CurrBudget().changed or \
            self.Confirm(warning, 'New Budget'):
            self.LoadBudget(budget.Budget())
  
    def OnOpenBudgetPressed(self, event):
        event.Skip(False)
        warning = 'There are unsaved changes.\n' + \
                  'Are you sure you want to open a budget?'
        if not self.CurrBudget().changed or \
            self.Confirm(warning, 'Open Budget'):
            filename = None
            dlg = wx.FileDialog(
                self,
                wildcard=filetypes,
                style=wx.FD_OPEN|wx.FD_CHANGE_DIR
            )
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath() # Get the filename from the dialog
            dlg.Destroy()
            if filename:
                self.LoadBudget(budget.Budget(filename))
  
    def OnCombineBudgetsPressed(self, event):
        event.Skip(False)
        filename = None
        dlg = wx.FileDialog(
            self,
            wildcard=filetypes,
            style=wx.FD_OPEN|wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath() # Get the filename from the dialog
        dlg.Destroy()
        if filename:
            self.CreateUndo()
            self.CurrBudget().combine(budget.Budget(filename), curr_date() + curr_time())
            self.RefreshBudget()
  
    def OnSaveBudgetPressed(self, event):
        if self.CurrBudget().has_filename():
            self.CurrBudget().save()
            self.UpdateTitle()
        else:
            self.OnSaveAsBudgetPressed(event)
  
    def OnSaveAsBudgetPressed(self, event):
        event.Skip(False)
        filename = None
        dlg = wx.FileDialog(
            self,
            wildcard=filetypes,
            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath() # Get the filename from the dialog
        dlg.Destroy()
        if filename:
            self.CurrBudget().save(filename)
            self.UpdateTitle()
  
    def OnQuitPressed(self, event):
        event.Skip(False)
        warning = 'There are unsaved changes.\n' + \
                  'Are you sure you want to quit?'
        if not self.CurrBudget().changed or \
            self.Confirm(warning, 'Quit'):
            self.Destroy()

    def OnExampleBudgetPressed(self, event):
        event.Skip(False)
        warning = 'There are unsaved changes.\n' + \
                  'Are you sure you want to load an example budget?'
        if not self.CurrBudget().changed or \
            self.Confirm(warning, 'Load Budget'):
            self.LoadBudget(budget.create_example_budget())

    def OnAboutPressed(self, event):
        event.Skip(False)
        #path = os.path.join(homepath, 'divvyup' + os.sep + 'icons' + os.sep)
        #info.SetIcon(wx.Icon(path + 'divvyup64x64.png', wx.BITMAP_TYPE_PNG))
        os.popen(os.path.join(homepath, 'divvyup' + os.sep + 'about.py'))

    def OnHelpPressed(self, event):
        event.Skip(False)
        HelpFrame(self)
  
    def OnAddCategoryPressed(self, event):
        event.Skip(False)
        dlg = AddCategoryDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.CreateUndo()
            self.CurrBudget().add_category(dlg.name, dlg.amount)
            self.RefreshBudget()
        dlg.Destroy()
  
    def OnRemoveCategory(self, event):
        event.Skip(False)
        self.CreateUndo()
        self.CurrBudget().remove_category(
            self.SelectedName(self.category_list)
        )
        self.RefreshBudget()

    def OnRenameCategory(self, event):
        event.Skip(False)
        dlg = RenameCategoryDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.CreateUndo()
            self.CurrBudget().rename_category(
                self.SelectedName(self.category_list), dlg.name
            )
            self.RefreshBudget()
        dlg.Destroy()
  
    def OnAddMoneyPressed(self, event):
        event.Skip(False)
        dlg = PutInCategoryDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.CreateUndo()
            self.CurrBudget().put_in(
                category=self.SelectedName(self.category_list),
                date=curr_date() + curr_time(),
                comment=dlg.comment,
                amount=dlg.amount
            )
            self.RefreshBudget()
        dlg.Destroy()
  
    def OnSubtractMoneyPressed(self, event):
        event.Skip(False)
        dlg = TakeOutCategoryDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.CreateUndo()
            self.CurrBudget().take_out(
                category=self.SelectedName(self.category_list),
                date=curr_date() + curr_time(),
                comment=dlg.comment,
                amount=dlg.amount
            )
            self.RefreshBudget()
        dlg.Destroy()

    def OnCategorySelected(self, event):
        event.Skip(False)
        self.UpdateTransactionList()
        self.UpdateCategoryControls()
  
    def OnCategoryDeselected(self, event):
        event.Skip(False)
        self.UpdateTransactionList()
        self.UpdateCategoryControls()
  
    def OnCategoryActivated(self, event):
        if self.SelectedIndex(self.category_list) >= 0:
            self.OnSubtractMoneyPressed(event)

    def OnUndoPressed(self, event):
        event.Skip(False)
        self.budget_wrapper.undo()
        self.RefreshBudget()
  
    def OnRedoPressed(self, event):
        event.Skip(False)
        self.budget_wrapper.redo()
        self.RefreshBudget()

    def OnEditTransactionPressed(self, event):
        event.Skip(False)
        # YOU LEFT OFF HERE!!
        envelope = self.SelectedName(self.category_list)
        transactions = self.CurrBudget().transactions(envelope)
        index = self.SelectedIndex(self.transaction_list)
        # Invert the index, because they were displayed in reverse order
        index = len(transactions) - 1 - index
        transaction = transactions[index]
        # Get values from the transaction
        date = transaction[budget.Budget.DATE]
        comment = transaction[budget.Budget.COMMENT]
        amount = transaction[budget.Budget.AMOUNT]
        action = transaction[budget.Budget.ACTION]
        if action == budget.Budget.SUB:
            dlg = TakeOutCategoryDialog(self)
        else:
            dlg = PutInCategoryDialog(self)
        dlg.amount_text_ctrl.SetValue(currency_to_string(amount))
        dlg.comment_text_ctrl.SetValue(comment)
        if int(date) < 0:
            dlg.date_label.Show(False)
            dlg.datepicker_ctrl.Show(False)
        else:
            pass
        #date = self.datepicker_ctrl.GetValue().Format('%Y%m%d')
        date = transaction[budget.Budget.DATE]
        datetime = wx.DateTime()
        datetime.ParseFormat(date, '%Y%m%d%H%M%S')
        dlg.datepicker_ctrl.SetValue(datetime)
        if dlg.ShowModal() == wx.ID_OK:
            self.CreateUndo()
            self.CurrBudget().delete_transaction_at_index(envelope, index)
            if int(date) < 0:
                newdate = -1
            else:
                # Newly selected date plus the original time
                newdate = dlg.date + date[9:]
            #print('New date: ' + str(newdate))
            if action == budget.Budget.SUB:
                self.CurrBudget().take_out(
                    category=envelope,
                    date=newdate,
                    comment=dlg.comment,
                    amount=dlg.amount
                )
            else:
                self.CurrBudget().put_in(
                    category=envelope,
                    date=newdate,
                    comment=dlg.comment,
                    amount=dlg.amount
                )
            self.RefreshBudget()
        dlg.Destroy()

    def OnDeleteTransactionPressed(self, event):
        event.Skip(False)
        self.CreateUndo()
        envelope = self.SelectedName(self.category_list)
        transactions = self.CurrBudget().transactions(envelope)
        if len(transactions) == 1:
            # Ask if you want to remove the envelope
            message = \
                'This is the only transaction in the category.\n' + \
                'Delete this category?'
            dlg = wx.MessageDialog(
                self,
                message,
                'Empty Category',
                wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION
            )
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                self.CurrBudget().remove_category(envelope)
            dlg.Destroy()
        else:
            index = self.SelectedIndex(self.transaction_list)
            # Invert the index, because they were displayed in reverse order
            index = len(transactions) - 1 - index
            transaction = transactions[index]
            self.CurrBudget().delete_transaction(envelope, transaction[0], transaction[1], transaction[2], transaction[3])
        self.RefreshBudget()

    def OnTransactionSelected(self, event):
        event.Skip(False)
        self.UpdateCategoryControls()
  
    def OnTransactionDeselected(self, event):
        event.Skip(False)
        self.UpdateCategoryControls()
  
    def OnTransactionActivated(self, event):
        if self.SelectedIndex(self.transaction_list) >= 0:
            self.OnEditTransactionPressed(event)

    def OnSplitterChanged(self, event):
        self.splitwindow.UpdateSize()
        # Category list
        width = self.category_list.GetClientSize().GetWidth()
        w1 = (width / 3) * 2
        if w1 > 200:
            w1 = 200
        self.category_list.SetColumnWidth(0, w1)
        self.category_list.SetColumnWidth(1, width - w1)
        # Transactions list
        width = self.transaction_list.GetClientSize().GetWidth()
        w1 = width / 4
        if w1 > 100:
            w1 = 100
        self.transaction_list.SetColumnWidth(0, w1)
        self.transaction_list.SetColumnWidth(1, width - (w1 * 3))
        self.transaction_list.SetColumnWidth(2, w1)
        self.transaction_list.SetColumnWidth(3, w1)
        self.main_panel.Layout()
        if event:
            event.Skip()

    def OnSplitterDoubleClick(self, event):
        event.Skip(False)
        self.splitwindow.SetSashPosition(220)
        self.OnSplitterChanged(None)

    def UpdateCategoryControls(self):
        enabled = False
        if self.SelectedIndex(self.category_list) >= 0:
            enabled = True
        self.remove_category_menu_item.Enable(enabled)
        self.rename_category_menu_item.Enable(enabled)
        self.add_money_menu_item.Enable(enabled)
        self.remove_money_menu_item.Enable(enabled)
        enabled = False
        if self.SelectedIndex(self.transaction_list) >= 0:
            enabled = True
        self.edit_transaction_menu_item.Enable(enabled)
        self.delete_transaction_menu_item.Enable(enabled)

    def CreateUndo(self):
        self.budget_wrapper.newversion()
  
    def LoadBudget(self, budget):
        self.budget_wrapper = undowrapper.UndoWrapper(budget)
        self.RefreshBudget()

    def RefreshBudget(self):
        self.UpdateTitle()
        self.UpdateCategoryList()
        self.UpdateTransactionList()
        self.UpdateTotal()
        self.UpdateCategoryControls()
        self.UpdateUndoControls()

    def UpdateTitle(self):
        name = self.CurrBudget().get_name()
        if not name:
            name = '[new budget]'
        saved = ''
        if self.CurrBudget().changed:
            saved = '*'
        self.SetTitle('DivvyUp - ' + saved + name)

    def UpdateCategoryList(self):
        selection = self.SelectedIndex(self.category_list)
        # Remove old envelopes from the GUI
        self.category_list.DeleteAllItems()
        for name in self.CurrBudget().categories():
            index = self.category_list.InsertStringItem(sys.maxint, name)
            self.category_list.SetStringItem(
                index, 1, currency_to_string(
                    self.CurrBudget().amount(name)
                )
            )
        if selection >= 0:
            if selection >= self.category_list.GetItemCount():
                selection = self.category_list.GetItemCount() - 1
            self.category_list.Select(selection)
            
    def UpdateTransactionList(self):
        selection = self.SelectedIndex(self.transaction_list)
        # Clear the list
        self.transaction_list.DeleteAllItems()
        # Fill in the list
        transactions = self.CurrBudget().transactions(
            self.SelectedName(self.category_list))
        for transaction in transactions:
            date = transaction[budget.Budget.DATE]
            if int(date) > 0:
                formatted_date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
            else:
                formatted_date = ''
            index = 0; # Insert in reverse order
            self.transaction_list.InsertStringItem(
                index,
                formatted_date
            )
            self.transaction_list.SetStringItem(
                index, 1, transaction[budget.Budget.COMMENT]
            )
            self.transaction_list.SetStringItem(
                index, 2, currency_to_string(
                    transaction[budget.Budget.AMOUNT]
                )
            )
            if transaction[budget.Budget.ACTION] == budget.Budget.ADD:
                self.transaction_list.SetStringItem(
                    index, 3, 'Put In'
                )
            else:
                self.transaction_list.SetStringItem(
                    index, 3, 'Take Out'
                )
        if selection >= 0:
            if selection >= self.transaction_list.GetItemCount():
                selection = self.transaction_list.GetItemCount() - 1
            self.transaction_list.Select(selection)
        # Show the amount in the envelope
        # Can be replaced with the amount that's in the envelopes list
        amount = self.CurrBudget().amount(
            self.SelectedName(self.category_list)
        )
        self.category_amount_label.SetLabel(
            'Amount: $' + currency_to_string(amount)
        )
        self.main_panel.Layout()

    def UpdateTotal(self):
        self.budget_total_label.SetLabel('Total: $' + currency_to_string(
            self.CurrBudget().total())
        )
        self.main_panel.Layout()

    def UpdateUndoControls(self):
        self.undo_menu_item.Enable(self.budget_wrapper.can_undo())
        self.redo_menu_item.Enable(self.budget_wrapper.can_redo());

    def OnFrameClosed(self, event):
        warning = 'There are unsaved changes.\n' + \
                  'Are you sure you want to quit?'
        if not self.CurrBudget().changed or \
            self.Confirm(warning, 'Quit'):
            self.Destroy()
        else:
            event.Veto()
  
    def Confirm(self, warning, title):
        dialog = wx.MessageDialog(self, warning, title,
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            return True
        else:
            return False

    def SelectedName(self, listctrl):
        index = self.SelectedIndex(listctrl)
        if index >= 0:
            return listctrl.GetItem(index, 0).GetText()
        return None

    def SelectedIndex(self, listctrl):
        return listctrl.GetFirstSelected()


class AddCategoryDialog(interface.AddCategoryDialogShell):

    def __init__(self, *args, **kwds):
        interface.AddCategoryDialogShell.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_KEY_UP, self.OnCancelCategory)
        self.amount = 0.00
        self.budget_amount = \
            self.GetParent().CurrBudget().total()
        self.category_name_text_ctrl.SetFocus()
        self.UpdateBudgetAmount()
  
    def OnCancelCategory(self, event):
        if isinstance(event, wx.KeyEvent) and \
           event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        elif not isinstance(event, wx.KeyEvent):
            self.EndModal(wx.ID_CANCEL)
  
    def OnAddCategoryPressed(self, event):
        event.Skip(False)
        self.name = self.category_name_text_ctrl.GetValue()
        if not self.name:
            message = 'Please enter a name for the category.'
            dlg = wx.MessageDialog(
                self,
                message,
                'No Category Name',
                wx.OK|wx.ICON_ERROR
            )
            dlg.ShowModal()
            dlg.Destroy()
        elif self.name in \
            self.GetParent().CurrBudget().categories():
            message = 'Please enter an unused name for the category.'
            dlg = wx.MessageDialog(
                self,
                message,
                'Used Category Name',
                wx.OK|wx.ICON_ERROR
            )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.EndModal(wx.ID_OK)
  
    def OnChangeAmount(self, event):
        event.Skip(False)
        self.amount = string_to_currency(self.amount_text_ctrl.GetValue())
        self.UpdateBudgetAmount()

    def UpdateBudgetAmount(self):
        self.budget_amount_label.SetLabel(
            'Budget Total: $' + currency_to_string(
                self.budget_amount + self.amount
            )
        )
        self.Layout()


class EditCategoryDialog(interface.EditCategoryDialogShell):

    def __init__(self, *args, **kwds):
        interface.EditCategoryDialogShell.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_KEY_UP, self.OnCancelPressed)
        self.envelope = self.GetParent().SelectedName(
            self.GetParent().category_list
        )
        self.SetTitle(self.envelope)
        self.budget = self.GetParent().CurrBudget()
        self.amount = 0.00
        self.category_amount = self.budget.amount(self.envelope)
        self.budget_amount = self.budget.total()

    def OnCancelPressed(self, event):
        if isinstance(event, wx.KeyEvent) and \
           event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        elif not isinstance(event, wx.KeyEvent):
            self.EndModal(wx.ID_CANCEL)

    def OnEditPressed(self, event):
        event.Skip(False)
        self.amount = string_to_currency(self.amount_text_ctrl.GetValue())
        self.comment = self.comment_text_ctrl.GetValue()
        self.date = self.datepicker_ctrl.GetValue().Format('%Y%m%d') + curr_time()
        if self.amount > 0.00:
            self.EndModal(wx.ID_OK)
        else:
            message = 'Please enter an amount of money.'
            dlg = wx.MessageDialog(
                self,
                message,
                'No Amount',
                wx.OK|wx.ICON_ERROR
            )
            dlg.ShowModal()
            dlg.Destroy()

    def OnChangeAmount(self, event):
        event.Skip(False)
        self.amount = string_to_currency(self.amount_text_ctrl.GetValue())
        self.UpdateCategoryAmount()
        self.UpdateBudgetAmount()
        self.Layout()

    def UpdateCategoryAmount(self):
        print('Pretending to update envelope amount.')

    def UpdateBudgetAmount(self):
        print('Pretending to update budget amount.')


class TakeOutCategoryDialog(EditCategoryDialog):

    def __init__(self, *args, **kwds):
        EditCategoryDialog.__init__(self, *args, **kwds)
        self.category_name_label.SetLabel('From ' + self.envelope)
        self.action_label.SetLabel('Take Out: $')
        self.edit_button.SetLabel('Take Out')
        self.amount_text_ctrl.SetValue(
            currency_to_string(
                self.budget.last_removed(self.envelope)
            )
        )
        self.amount_text_ctrl.SetFocus()
        self.amount_text_ctrl.SetSelection(-1, -1)
        self.UpdateCategoryAmount()
        self.UpdateBudgetAmount()
        self.Layout()

    def UpdateCategoryAmount(self):
        self.category_amount_label.SetLabel(
            'Category: $' + currency_to_string(
                self.category_amount - self.amount
            )
        )

    def UpdateBudgetAmount(self):
        self.budget_amount_label.SetLabel(
            'Budget: $' + currency_to_string(
                self.budget_amount - self.amount
            )
        )


class PutInCategoryDialog(EditCategoryDialog):

    def __init__(self, *args, **kwds):
        EditCategoryDialog.__init__(self, *args, **kwds)
        self.category_name_label.SetLabel('To ' + self.envelope)
        self.action_label.SetLabel('Put In: $')
        self.edit_button.SetLabel('Put In')
        self.amount_text_ctrl.SetValue(
            currency_to_string(
                self.budget.last_added(self.envelope)
            )
        )
        self.amount_text_ctrl.SetFocus()
        self.amount_text_ctrl.SetSelection(-1, -1)
        self.UpdateCategoryAmount()
        self.UpdateBudgetAmount()
        self.Layout()

    def UpdateCategoryAmount(self):
        self.category_amount_label.SetLabel(
            'Category: $' + currency_to_string(
                self.category_amount + self.amount
            )
        )

    def UpdateBudgetAmount(self):
        self.budget_amount_label.SetLabel(
            'Budget: $' + currency_to_string(
                self.budget_amount + self.amount
            )
        )


class RenameCategoryDialog(interface.RenameCategoryDialogShell):

    def __init__(self, *args, **kwds):
        interface.RenameCategoryDialogShell.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_KEY_UP, self.OnCancelPressed)
        self.envelope = self.GetParent().SelectedName(
            self.GetParent().category_list
        )
        self.category_name_label.SetLabel('Rename ' + self.envelope)
        self.category_name_text_ctrl.SetValue(self.envelope)
        self.category_name_text_ctrl.SetFocus()
        self.category_name_text_ctrl.SetSelection(-1, -1)

    def OnCancelPressed(self, event):
        if isinstance(event, wx.KeyEvent) and \
           event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        elif not isinstance(event, wx.KeyEvent):
            self.EndModal(wx.ID_CANCEL)

    def OnRenamePressed(self, event):
        event.Skip(False)
        self.name = self.category_name_text_ctrl.GetValue()
        if not self.name:
            message = 'Please enter a name for the category.'
            dlg = wx.MessageDialog(
                self,
                message,
                'No Category Name',
                wx.OK|wx.ICON_ERROR
            )
            dlg.ShowModal()
            dlg.Destroy()
        elif self.name in \
            self.GetParent().CurrBudget().categories():
            message = 'Please enter an unused name for the category.'
            dlg = wx.MessageDialog(
                self,
                message,
                'Used Category Name',
                wx.OK|wx.ICON_ERROR
            )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.EndModal(wx.ID_OK)


class HelpFrame(interface.HelpFrameShell):

    def __init__(self, *args, **kwds):
        interface.HelpFrameShell.__init__(self, *args, **kwds)

        # Setup widgets
        self.main_panel = wx.Panel(self, -1)
        self.close_button = wx.Button(self.main_panel, -1, "&Close")
        self.Bind(wx.EVT_BUTTON, self.OnClosePressed, self.close_button)
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(
            self.close_button,
            0,
            wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,
            10
        )
        self.main_panel.SetSizer(main_sizer)
        frame_sizer.Add(self.main_panel, 1, wx.EXPAND, 0)
        self.SetSizer(frame_sizer)

        # Setup HTML
        htmlwin = wx.html.HtmlWindow(
            self.main_panel,
            wx.ID_ANY,
            style=wx.NO_BORDER
        )
        htmlwin.SetStandardFonts()
        htmlwin.LoadPage(os.path.join(homepath, 'divvyup' + os.sep + 'help' + os.sep + 'tutorial.html'))
        main_sizer.Insert(
            before=0,
            item=htmlwin,
            proportion=1,
            flag=wx.ALL|wx.EXPAND,
            border=10
        )

        # Show window
        self.Layout()
        self.Center()
        self.Show()

    def OnClosePressed(self, event):
        event.Skip(False)
        self.Close()


def curr_date():
    return time.strftime('%Y%m%d', time.localtime())


def curr_time():
    return time.strftime('%H%M%S', time.localtime())


def date_to_string(date):
    pass


def string_to_date(string):
    pass


def currency_to_string(currency):
    string = '0.00'
    try:
        #string = '{:.2f}'.format(float(currency)) # Python 2.6 or greater
        string = '%(value).2f' % {'value': float(currency)}
    except ValueError:
        pass
    return string


def string_to_currency(string):
    currency = 0.00
    try:
        #string = '{:.2f}'.format(float(string)) # Python 2.6 or greater
        string = '%(value).2f' % {'value': float(string)}
        currency = float(string)
    except ValueError:
        pass
    return currency


def main():
    app = wx.PySimpleApp(0)
    app.SetAppName('divvyup')
    app.SetClassName('divvyup')
    wx.InitAllImageHandlers()
    main_frame = MainFrame(None, -1, 'divvyup')
    app.SetTopWindow(main_frame)
    main_frame.Show()
    # Parse command line options
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        main_frame.LoadBudget(budget.Budget(sys.argv[1]))
    app.MainLoop()


if __name__ == '__main__':
    main()

