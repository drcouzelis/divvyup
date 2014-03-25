#!/usr/bin/env python

from gi.repository import Gtk
from gi.repository import GdkPixbuf


class AboutDialog(Gtk.AboutDialog):

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
        try:
            self.set_logo(GdkPixbuf.Pixbuf.new_from_file('divvyup/icons/divvyup64x64.png'))
        except:
            self.set_logo(GdkPixbuf.Pixbuf.new_from_file('icons/divvyup64x64.png'))


if __name__ == '__main__':
    dialog = AboutDialog()
    dialog.run()
    dialog.destroy()
