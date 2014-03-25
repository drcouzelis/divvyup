#!/usr/bin/env python

import locale
from gi.repository import GdkPixbuf
from gi.repository import Gtk

import budget2 as budget


def example_budget():
    bud = budget.Budget()
    return bud


def cell_format_money(tree_column, cell, tree_model, iter, data):
#    import IPython
#    IPython.embed()
    amount = float(cell.get_property('text'))
    cell.set_property('text', '{:.2f}'.format(amount))


class Window (Gtk.Window):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.connect('delete-event', self.on_quit)

        # Menubar
        self.menubar = MenuBar(self)

        # Split pane
        self.paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        w, h = self.get_size()
        self.paned.set_position(w / 3)

        # Category list
        self.add_category_list()
        self.paned.pack1(self.category_view, resize=True, shrink=False)

        # Transaction list
        self.add_transaction_list()
        self.paned.pack2(self.transaction_view, resize=True, shrink=False)

        # EXAMPLE
        #self.category_list.append(['Cameras', 100.00])
        #self.category_list.append(['Food', 60.00])
        #self.category_list.append(['Video Games', 120.00])
        #self.transaction_list.append(['2012-02-03', 3.00, 'Salad'])
        #self.transaction_list.append(['2012-01-02', -5.00, 'Hamburger'])
        #self.transaction_list.append(['2012-01-01', 123.45, 'Initial amount'])
        self.load_budget(example_budget())

        # Layout
        vbox = Gtk.VBox(homogeneous=False, spacing=0)
        vbox.pack_start(child=self.menubar, expand=False, fill=True, padding=0)
        vbox.pack_start(child=self.paned, expand=True, fill=True, padding=0)
        self.add(vbox)

        self.update_titlebar()

        self.show_all()

    def load_budget(self, budget_):
        self.budget = budget_
        # YOU LEFT OFF HERE!!
        # strftime(locale.nl_langinfo(locale.D_FMT)

    def add_category_list(self):
        self.category_list = Gtk.ListStore(str, float)
        self.category_view = Gtk.TreeView(self.category_list)

        render = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Category', render, text=0)
        #column.set_sort_column_id(0)
        column.set_expand(True)
        self.category_view.append_column(column)

        render = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Amount', render, text=1)
        #column.set_sort_column_id(1)
        column.set_cell_data_func(render, cell_format_money)
        self.category_view.append_column(column)

    def add_transaction_list(self):
        self.transaction_list = Gtk.ListStore(str, float, str)
        self.transaction_view = Gtk.TreeView(self.transaction_list)

        render = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Date', render, text=0)
        #column.set_sort_column_id(0)
        self.transaction_view.append_column(column)

        render = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Amount', render, text=1)
        #column.set_sort_column_id(1)
        column.set_cell_data_func(render, cell_format_money)
        self.transaction_view.append_column(column)

        render = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Comment', render, text=2)
        #column.set_sort_column_id(2)
        column.set_expand(True)
        self.transaction_view.append_column(column)

    def on_budget_new(self, widget, data):
        pass

    def on_budget_open(self, widget, data):
        pass

    def on_budget_combine(self, widget, data):
        pass

    def on_budget_save(self, widget, data):
        pass

    def on_budget_save_as(self, widget, data):
        pass

    def on_quit(self, widget, data):
        Gtk.main_quit()

    def on_undo(self, widget, data):
        pass

    def on_redo(self, widget, data):
        pass

    def on_cut(self, widget, data):
        pass

    def on_copy(self, widget, data):
        pass

    def on_paste(self, widget, data):
        pass

    def on_preferences(self, widget, data):
        pass

    def on_category_add(self, widget, data):
        pass

    def on_category_remove(self, widget, data):
        pass

    def on_category_rename(self, widget, data):
        pass

    def on_transaction_add(self, widget, data):
        pass

    def on_transaction_edit(self, widget, data):
        pass

    def on_transaction_delete(self, widget, data):
        pass

    def on_example(self, widget, data):
        pass

    def on_tutorial(self, widget, data):
        pass

    def on_about(self, widget, data):
        dialog = AboutDialog()
        dialog.set_transient_for(self)
        dialog.run()
        dialog.destroy()

    def update_titlebar(self):
        self.set_title('DivvyUp - [new budget]')


class MenuBar (Gtk.MenuBar):

    def __init__(self, window):
        super().__init__()
        self.window = window

        self.accel_group = Gtk.AccelGroup()
        self.window.add_accel_group(self.accel_group)

        self.append(self.create_budget_menu())
        self.append(self.create_edit_menu())
        self.append(self.create_category_menu())
        self.append(self.create_transaction_menu())
        self.append(self.create_help_menu())

    def create_budget_menu(self):
        menuitem = Gtk.MenuItem.new_with_mnemonic('_Budget')

        # Menu items
        self.budget_new_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_NEW, self.accel_group)
        self.budget_open_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_OPEN, self.accel_group)
        self.budget_combine_menuitem = Gtk.MenuItem.new_with_mnemonic('_Combine...')
        self.budget_save_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_SAVE, self.accel_group)
        self.budget_save_as_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_SAVE_AS, self.accel_group)
        self.budget_quit_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT, self.accel_group)

        # Add to menu
        menu = Gtk.Menu()
        menu.append(self.budget_new_menuitem)
        menu.append(self.budget_open_menuitem)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.budget_combine_menuitem)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.budget_save_menuitem)
        menu.append(self.budget_save_as_menuitem)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.budget_quit_menuitem)
        menuitem.set_submenu(menu)

        # Activate
        self.budget_new_menuitem.connect('activate', self.window.on_budget_new, None)
        self.budget_open_menuitem.connect('activate', self.window.on_budget_open, None)
        self.budget_combine_menuitem.connect('activate', self.window.on_budget_combine, None)
        self.budget_save_menuitem.connect('activate', self.window.on_budget_save, None)
        self.budget_save_as_menuitem.connect('activate', self.window.on_budget_save_as, None)
        self.budget_quit_menuitem.connect('activate', self.window.on_quit, None)

        return menuitem

    def create_edit_menu(self):
        menuitem = Gtk.MenuItem.new_with_mnemonic('_Edit')

        # Menu items
        self.edit_undo_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_UNDO, self.accel_group)
        self.edit_redo_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_REDO, self.accel_group)
        self.edit_cut_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_CUT, self.accel_group)
        self.edit_copy_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_COPY, self.accel_group)
        self.edit_paste_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PASTE, self.accel_group)
        self.edit_preferences_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PREFERENCES, self.accel_group)

        # Add to menu
        menu = Gtk.Menu()
        menu.append(self.edit_undo_menuitem)
        menu.append(self.edit_redo_menuitem)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.edit_cut_menuitem)
        menu.append(self.edit_copy_menuitem)
        menu.append(self.edit_paste_menuitem)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.edit_preferences_menuitem)
        menuitem.set_submenu(menu)

        # Activate
        self.edit_undo_menuitem.connect('activate', self.window.on_undo, None)
        self.edit_redo_menuitem.connect('activate', self.window.on_redo, None)
        self.edit_cut_menuitem.connect('activate', self.window.on_cut, None)
        self.edit_copy_menuitem.connect('activate', self.window.on_copy, None)
        self.edit_paste_menuitem.connect('activate', self.window.on_paste, None)
        self.edit_preferences_menuitem.connect('activate', self.window.on_preferences, None)

        return menuitem

    def create_category_menu(self):
        menuitem = Gtk.MenuItem.new_with_mnemonic('_Category')

        # Menu items
        self.category_add_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ADD, self.accel_group)
        self.category_remove_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_REMOVE, self.accel_group)
        self.category_rename_menuitem = Gtk.ImageMenuItem.new_with_mnemonic('Re_name')

        # Accelerators
        self.category_add_menuitem.add_accelerator('activate',
                self.accel_group, *Gtk.accelerator_parse('<control>e'),
                accel_flags=Gtk.AccelFlags.VISIBLE)
        self.category_rename_menuitem.add_accelerator('activate',
                self.accel_group, *Gtk.accelerator_parse('F2'),
                accel_flags=Gtk.AccelFlags.VISIBLE)

        # Add to menu
        menu = Gtk.Menu()
        menu.append(self.category_add_menuitem)
        menu.append(self.category_remove_menuitem)
        menu.append(self.category_rename_menuitem)
        menuitem.set_submenu(menu)

        # Activate
        self.category_add_menuitem.connect('activate', self.window.on_category_add, None)
        self.category_remove_menuitem.connect('activate', self.window.on_category_remove, None)
        self.category_rename_menuitem.connect('activate', self.window.on_category_rename, None)

        return menuitem

    def create_transaction_menu(self):
        menuitem = Gtk.MenuItem.new_with_mnemonic('_Transaction')

        # Menu items
        self.transaction_add_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ADD, self.accel_group)
        self.transaction_edit_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_EDIT, self.accel_group)
        self.transaction_delete_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_DELETE, self.accel_group)

        # Add to menu
        menu = Gtk.Menu()
        menu.append(self.transaction_add_menuitem)
        menu.append(self.transaction_edit_menuitem)
        menu.append(self.transaction_delete_menuitem)
        menuitem.set_submenu(menu)

        # Activate
        self.transaction_add_menuitem.connect('activate', self.window.on_transaction_add, None)
        self.transaction_edit_menuitem.connect('activate', self.window.on_transaction_edit, None)
        self.transaction_delete_menuitem.connect('activate', self.window.on_transaction_delete, None)

        return menuitem

    def create_help_menu(self):
        menuitem = Gtk.MenuItem.new_with_mnemonic('_Help')

        # Menu items
        self.help_example_menuitem = Gtk.MenuItem.new_with_mnemonic('_Example Budget...')
        self.help_tutorial_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_HELP, self.accel_group)
        self.help_about_menuitem = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT, self.accel_group)

        # Add to menu
        menu = Gtk.Menu()
        menu.append(self.help_example_menuitem)
        menu.append(self.help_tutorial_menuitem)
        menu.append(Gtk.SeparatorMenuItem.new())
        menu.append(self.help_about_menuitem)
        menuitem.set_submenu(menu)

        # Activate
        self.help_example_menuitem.connect('activate', self.window.on_example, None)
        self.help_tutorial_menuitem.connect('activate', self.window.on_tutorial, None)
        self.help_about_menuitem.connect('activate', self.window.on_about, None)

        return menuitem


class AboutDialog (Gtk.AboutDialog):

    def __init__(self):
        super().__init__()
        self.set_program_name('DivvyUp Personal Finance')
        self.set_version('0.6')
        self.set_copyright('Copyright 2012 David Couzelis')
        self.set_comments('A simple application that uses the envelope\n' \
                          'system to help you budget your money.')
        self.set_license( \
'This program is free software: you can redistribute it and/or modify ' + \
'it under the terms of the GNU General Public License as published by ' + \
'the Free Software Foundation, either version 3 of the License, or ' + \
'(at your option) any later version.\n' + \
'\n' + \
'This program is distributed in the hope that it will be useful, ' + \
'but WITHOUT ANY WARRANTY; without even the implied warranty of ' + \
'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the ' + \
'GNU General Public License for more details.\n' + \
'\n' + \
'You should have received a copy of the GNU General Public License ' + \
'along with this program. If not, see http://www.gnu.org/licenses/.')
        self.set_wrap_license(True)
        self.set_title('DivvyUp - About')
        self.set_website('http://www.sourceforge.net/projects/enbudget/')
        self.set_website_label('Project home page')
        self.set_authors(['David Couzelis'])
        self.set_logo(GdkPixbuf.Pixbuf.new_from_file('icons/divvyup64x64.png'))


# Main
if __name__ == '__main__':
    # Load the user's default locale settings
    locale.setlocale(locale.LC_ALL, '')

    Gtk.Window.set_default_icon_name('divvyup')
    window = Window()
    Gtk.main()
