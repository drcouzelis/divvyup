#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Fri Jan 13 01:22:15 2012

import wx

# begin wxGlade: extracode
# end wxGlade



class MainFrameShell(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrameShell.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.main_panel = wx.Panel(self, -1)
        self.splitwindow = wx.SplitterWindow(self.main_panel, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.window_1_pane_2 = wx.Panel(self.splitwindow, -1)
        self.window_1_pane_1 = wx.Panel(self.splitwindow, -1)
        
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.new_budget_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_NEW, "", "Create a new budget", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.new_budget_menu_item)
        self.open_budget_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_OPEN, "&Open...\tCtrl+O", "Open an existing budget", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.open_budget_menu_item)
        wxglade_tmp_menu.AppendSeparator()
        self.combine_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Combine...", "Combine two budgets", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.combine_menu_item)
        wxglade_tmp_menu.AppendSeparator()
        self.save_budget_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_SAVE, "", "Save the current budget", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.save_budget_menu_item)
        self.save_as_budget_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_SAVEAS, "Save &As...\tShift+Ctrl+S", "Save the current budget with a new name", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.save_as_budget_menu_item)
        wxglade_tmp_menu.AppendSeparator()
        self.quit_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_EXIT, "", "Quit DivvyUp", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.quit_menu_item)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&Budget")
        wxglade_tmp_menu = wx.Menu()
        self.undo_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_UNDO, "&Undo\tCtrl+Z", "Undo a change to the budget", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.undo_menu_item)
        self.redo_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_REDO, "&Redo\tCtrl+Y", "Redo a change to the budget", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.redo_menu_item)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&Edit")
        wxglade_tmp_menu = wx.Menu()
        self.add_category_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_ADD, "&Add...\tCtrl+E", "Add a new category", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.add_category_menu_item)
        self.remove_category_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_REMOVE, "", "Remove the selected category", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.remove_category_menu_item)
        self.rename_category_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "Re&name...\tF2", "Rename the selected category", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.rename_category_menu_item)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&Category")
        wxglade_tmp_menu = wx.Menu()
        self.remove_money_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Take Out...", "Take money out of the selected category", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.remove_money_menu_item)
        self.add_money_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Put In...", "Put money into the selected category", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.add_money_menu_item)
        wxglade_tmp_menu.AppendSeparator()
        self.edit_transaction_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_EDIT, "&Edit...", "Edit the selected transaction", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.edit_transaction_menu_item)
        self.delete_transaction_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_DELETE, "", "Delete the selected transaction", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.delete_transaction_menu_item)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&Transaction")
        wxglade_tmp_menu = wx.Menu()
        self.example_budget_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Example Budget", "Create an example budget", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.example_budget_menu_item)
        self.help_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_HELP, "&Tutorial...\tCtrl+H", "Learn how to use DivvyUp", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.help_menu_item)
        wxglade_tmp_menu.AppendSeparator()
        self.about_menu_item = wx.MenuItem(wxglade_tmp_menu, wx.ID_ABOUT, "&About...", "About DivvyUp", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.about_menu_item)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "&Help")
        self.SetMenuBar(self.frame_1_menubar)
        # Menu Bar end
        self.statusbar = self.CreateStatusBar(1, 0)
        self.category_list = wx.ListCtrl(self.window_1_pane_1, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING|wx.SUNKEN_BORDER)
        self.budget_total_label = wx.StaticText(self.window_1_pane_1, -1, "Total: $[500.00]")
        self.transaction_list = wx.ListCtrl(self.window_1_pane_2, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING|wx.SUNKEN_BORDER)
        self.category_amount_label = wx.StaticText(self.window_1_pane_2, -1, "Amount: $[25.00]")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.OnNewBudgetPressed, self.new_budget_menu_item)
        self.Bind(wx.EVT_MENU, self.OnOpenBudgetPressed, self.open_budget_menu_item)
        self.Bind(wx.EVT_MENU, self.OnCombineBudgetsPressed, self.combine_menu_item)
        self.Bind(wx.EVT_MENU, self.OnSaveBudgetPressed, self.save_budget_menu_item)
        self.Bind(wx.EVT_MENU, self.OnSaveAsBudgetPressed, self.save_as_budget_menu_item)
        self.Bind(wx.EVT_MENU, self.OnQuitPressed, self.quit_menu_item)
        self.Bind(wx.EVT_MENU, self.OnUndoPressed, self.undo_menu_item)
        self.Bind(wx.EVT_MENU, self.OnRedoPressed, self.redo_menu_item)
        self.Bind(wx.EVT_MENU, self.OnAddCategoryPressed, self.add_category_menu_item)
        self.Bind(wx.EVT_MENU, self.OnRemoveCategory, self.remove_category_menu_item)
        self.Bind(wx.EVT_MENU, self.OnRenameCategory, self.rename_category_menu_item)
        self.Bind(wx.EVT_MENU, self.OnSubtractMoneyPressed, self.remove_money_menu_item)
        self.Bind(wx.EVT_MENU, self.OnAddMoneyPressed, self.add_money_menu_item)
        self.Bind(wx.EVT_MENU, self.OnEditTransactionPressed, self.edit_transaction_menu_item)
        self.Bind(wx.EVT_MENU, self.OnDeleteTransactionPressed, self.delete_transaction_menu_item)
        self.Bind(wx.EVT_MENU, self.OnExampleBudgetPressed, self.example_budget_menu_item)
        self.Bind(wx.EVT_MENU, self.OnHelpPressed, self.help_menu_item)
        self.Bind(wx.EVT_MENU, self.OnAboutPressed, self.about_menu_item)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnCategoryDeselected, self.category_list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnCategorySelected, self.category_list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnCategoryActivated, self.category_list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnTransactionDeselected, self.transaction_list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnTransactionSelected, self.transaction_list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnTransactionActivated, self.transaction_list)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSplitterChanged, self.splitwindow)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnSplitterDoubleClick, self.splitwindow)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrameShell.__set_properties
        self.SetTitle("DivvyUp")
        self.SetSize((640, 500))
        self.statusbar.SetStatusWidths([-1])
        # statusbar fields
        statusbar_fields = [""]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrameShell.__do_layout
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_22 = wx.BoxSizer(wx.VERTICAL)
        sizer_21 = wx.BoxSizer(wx.VERTICAL)
        sizer_21.Add(self.category_list, 1, wx.EXPAND, 0)
        sizer_21.Add(self.budget_total_label, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        self.window_1_pane_1.SetSizer(sizer_21)
        sizer_22.Add(self.transaction_list, 1, wx.EXPAND, 0)
        sizer_22.Add(self.category_amount_label, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        self.window_1_pane_2.SetSizer(sizer_22)
        self.splitwindow.SplitVertically(self.window_1_pane_1, self.window_1_pane_2, 220)
        sizer_7.Add(self.splitwindow, 1, wx.EXPAND, 0)
        self.main_panel.SetSizer(sizer_7)
        sizer_6.Add(self.main_panel, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_6)
        self.Layout()
        # end wxGlade

    def OnNewBudgetPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnNewBudgetPressed' not implemented!"
        event.Skip()

    def OnOpenBudgetPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnOpenBudgetPressed' not implemented!"
        event.Skip()

    def OnCombineBudgetsPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnCombineBudgetsPressed' not implemented!"
        event.Skip()

    def OnSaveBudgetPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnSaveBudgetPressed' not implemented!"
        event.Skip()

    def OnSaveAsBudgetPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnSaveAsBudgetPressed' not implemented!"
        event.Skip()

    def OnQuitPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnQuitPressed' not implemented!"
        event.Skip()

    def OnUndoPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnUndoPressed' not implemented!"
        event.Skip()

    def OnRedoPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnRedoPressed' not implemented!"
        event.Skip()

    def OnAddCategoryPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnAddCategoryPressed' not implemented!"
        event.Skip()

    def OnRemoveCategory(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnRemoveCategory' not implemented!"
        event.Skip()

    def OnRenameCategory(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnRenameCategory' not implemented!"
        event.Skip()

    def OnSubtractMoneyPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnSubtractMoneyPressed' not implemented!"
        event.Skip()

    def OnAddMoneyPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnAddMoneyPressed' not implemented!"
        event.Skip()

    def OnEditTransactionPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnEditTransactionPressed' not implemented!"
        event.Skip()

    def OnDeleteTransactionPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnDeleteTransactionPressed' not implemented!"
        event.Skip()

    def OnExampleBudgetPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnExampleBudgetPressed' not implemented!"
        event.Skip()

    def OnHelpPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnHelpPressed' not implemented!"
        event.Skip()

    def OnAboutPressed(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnAboutPressed' not implemented!"
        event.Skip()

    def OnCategoryDeselected(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnCategoryDeselected' not implemented!"
        event.Skip()

    def OnCategorySelected(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnCategorySelected' not implemented!"
        event.Skip()

    def OnCategoryActivated(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnCategoryActivated' not implemented!"
        event.Skip()

    def OnTransactionDeselected(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnTransactionDeselected' not implemented!"
        event.Skip()

    def OnTransactionSelected(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnTransactionSelected' not implemented!"
        event.Skip()

    def OnTransactionActivated(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnTransactionActivated' not implemented!"
        event.Skip()

    def OnSplitterChanged(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnSplitterChanged' not implemented!"
        event.Skip()

    def OnSplitterDoubleClick(self, event): # wxGlade: MainFrameShell.<event_handler>
        print "Event handler `OnSplitterDoubleClick' not implemented!"
        event.Skip()

# end of class MainFrameShell


class AddCategoryDialogShell(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: AddCategoryDialogShell.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_4 = wx.StaticText(self, -1, "Category Name:")
        self.category_name_text_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
        self.label_3 = wx.StaticText(self, -1, "Initial Amount: $", style=wx.ALIGN_RIGHT)
        self.amount_text_ctrl = wx.TextCtrl(self, -1, "0.00", style=wx.TE_PROCESS_ENTER|wx.TE_RIGHT)
        self.budget_amount_label = wx.StaticText(self, -1, "Budget Total: $[250.00]")
        self.cancel_category_button = wx.Button(self, -1, "Cancel")
        self.add_category_button = wx.Button(self, -1, "Add Category")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.OnAddCategoryPressed, self.category_name_text_ctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnAddCategoryPressed, self.amount_text_ctrl)
        self.Bind(wx.EVT_TEXT, self.OnChangeAmount, self.amount_text_ctrl)
        self.Bind(wx.EVT_BUTTON, self.OnCancelCategory, self.cancel_category_button)
        self.Bind(wx.EVT_BUTTON, self.OnAddCategoryPressed, self.add_category_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: AddCategoryDialogShell.__set_properties
        self.SetTitle("Add Category")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: AddCategoryDialogShell.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_19.Add(self.label_4, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_19.Add(self.category_name_text_ctrl, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_3.Add(sizer_19, 0, wx.EXPAND, 0)
        sizer_16.Add(self.label_3, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_16.Add(self.amount_text_ctrl, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_3.Add(sizer_16, 0, wx.EXPAND, 0)
        sizer_3.Add(self.budget_amount_label, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT, 10)
        sizer_11.Add(self.cancel_category_button, 0, wx.ALL, 10)
        sizer_9.Add(sizer_11, 1, wx.ALIGN_BOTTOM, 0)
        sizer_12.Add(self.add_category_button, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        sizer_9.Add(sizer_12, 1, wx.ALIGN_BOTTOM, 0)
        sizer_3.Add(sizer_9, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_3)
        sizer_3.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnAddCategoryPressed(self, event): # wxGlade: AddCategoryDialogShell.<event_handler>
        print "Event handler `OnAddCategoryPressed' not implemented!"
        event.Skip()

    def OnChangeAmount(self, event): # wxGlade: AddCategoryDialogShell.<event_handler>
        print "Event handler `OnChangeAmount' not implemented!"
        event.Skip()

    def OnCancelCategory(self, event): # wxGlade: AddCategoryDialogShell.<event_handler>
        print "Event handler `OnCancelCategory' not implemented!"
        event.Skip()

# end of class AddCategoryDialogShell


class EditCategoryDialogShell(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: EditCategoryDialogShell.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.category_name_label = wx.StaticText(self, -1, "[Category Name]")
        self.action_label = wx.StaticText(self, -1, "[Action]: $")
        self.amount_text_ctrl = wx.TextCtrl(self, -1, "0.00", style=wx.TE_PROCESS_ENTER|wx.TE_RIGHT)
        self.category_amount_label = wx.StaticText(self, -1, "Category: $[100.00]")
        self.budget_amount_label = wx.StaticText(self, -1, "Budget: $[250.00]")
        self.label_3 = wx.StaticText(self, -1, "Comment:")
        self.comment_text_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_RIGHT)
        self.date_label = wx.StaticText(self, -1, "Date:")
        self.datepicker_ctrl = wx.DatePickerCtrl(self, -1, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        self.cancel_button = wx.Button(self, -1, "Cancel")
        self.edit_button = wx.Button(self, -1, "[Edit]")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.OnEditPressed, self.amount_text_ctrl)
        self.Bind(wx.EVT_TEXT, self.OnChangeAmount, self.amount_text_ctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEditPressed, self.comment_text_ctrl)
        self.Bind(wx.EVT_BUTTON, self.OnCancelPressed, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.OnEditPressed, self.edit_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: EditCategoryDialogShell.__set_properties
        self.SetTitle("[Category Name]")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: EditCategoryDialogShell.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.category_name_label, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_4.Add(self.action_label, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_4.Add(self.amount_text_ctrl, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(self.category_amount_label, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT, 10)
        sizer_1.Add(self.budget_amount_label, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT, 10)
        sizer_5.Add(self.label_3, 0, wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_5.Add(self.comment_text_ctrl, 1, wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_1.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_10.Add(self.date_label, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT, 10)
        sizer_6.Add(sizer_10, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(self.datepicker_ctrl, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_13.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_13, 0, wx.EXPAND, 0)
        sizer_11.Add(self.cancel_button, 0, wx.ALL, 10)
        sizer_9.Add(sizer_11, 1, wx.ALIGN_BOTTOM, 0)
        sizer_12.Add(self.edit_button, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        sizer_9.Add(sizer_12, 1, wx.ALIGN_BOTTOM, 0)
        sizer_2.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def OnEditPressed(self, event): # wxGlade: EditCategoryDialogShell.<event_handler>
        print "Event handler `OnEditPressed' not implemented!"
        event.Skip()

    def OnChangeAmount(self, event): # wxGlade: EditCategoryDialogShell.<event_handler>
        print "Event handler `OnChangeAmount' not implemented!"
        event.Skip()

    def OnCancelPressed(self, event): # wxGlade: EditCategoryDialogShell.<event_handler>
        print "Event handler `OnCancelPressed' not implemented!"
        event.Skip()

# end of class EditCategoryDialogShell


class RenameCategoryDialogShell(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RenameCategoryDialogShell.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.category_name_label = wx.StaticText(self, -1, "Rename [Category Name]")
        self.label_1 = wx.StaticText(self, -1, "To:")
        self.category_name_text_ctrl = wx.TextCtrl(self, -1, "[Category Name]", style=wx.TE_PROCESS_ENTER)
        self.cancel_button = wx.Button(self, -1, "Cancel")
        self.rename_button = wx.Button(self, -1, "Rename")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.OnRenamePressed, self.category_name_text_ctrl)
        self.Bind(wx.EVT_BUTTON, self.OnCancelPressed, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.OnRenamePressed, self.rename_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RenameCategoryDialogShell.__set_properties
        self.SetTitle("Rename")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RenameCategoryDialogShell.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.category_name_label, 0, wx.LEFT|wx.RIGHT|wx.TOP, 10)
        sizer_4.Add(self.label_1, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_4.Add(self.category_name_text_ctrl, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_11.Add(self.cancel_button, 0, wx.ALL, 10)
        sizer_9.Add(sizer_11, 1, wx.ALIGN_BOTTOM, 0)
        sizer_12.Add(self.rename_button, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        sizer_9.Add(sizer_12, 1, wx.ALIGN_BOTTOM, 0)
        sizer_2.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def OnRenamePressed(self, event): # wxGlade: RenameCategoryDialogShell.<event_handler>
        print "Event handler `OnRenamePressed' not implemented!"
        event.Skip()

    def OnCancelPressed(self, event): # wxGlade: RenameCategoryDialogShell.<event_handler>
        print "Event handler `OnCancelPressed' not implemented!"
        event.Skip()

# end of class RenameCategoryDialogShell


class HelpFrameShell(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: HelpFrameShell.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: HelpFrameShell.__set_properties
        self.SetTitle("DivvyUp Tutorial")
        self.SetSize((600, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: HelpFrameShell.__do_layout
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class HelpFrameShell


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    main_frame = MainFrameShell(None, -1, "")
    app.SetTopWindow(main_frame)
    main_frame.Show()
    app.MainLoop()