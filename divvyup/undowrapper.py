'''Provides undo and redo functionality.'''
#!/usr/bin/env python2

import copy

class UndoWrapper:
    '''This class provides undo and redo functionality of an item.
       Before modifying the item, use the "newinstance" method.
       Use the "undo" and "redo" methods to change the current item.
       Use the "curr" method to get the current instance of the item.'''

    def __init__(self, item):
        self.items = [item]
        self.index = 0
    
    def curr(self):
        '''Returns the current item.'''
        return self.items[self.index]
    
    def can_undo(self):
        '''Returns true if an undoredo is possible.'''
        if self.index > 0:
            return True
        return False
    
    def can_redo(self):
        '''Returns true if a redo is possible.'''
        if self.index < len(self.items) - 1:
            return True
        return False
    
    def newversion(self):
        '''Create a copy of the item and set it as the new current item.'''
        item = self.curr()
        if self.index < len(self.items) - 1:
            # Clear any "redo"s
            del(self.items[self.index + 1:])
        self.items.append(copy.deepcopy(item))
        self.index += 1
    
    def undo(self):
        '''Change the current item to an older version.'''
        if self.can_undo():
            self.index -= 1
    
    def redo(self):
        '''Change the current item to a more recent version.'''
        if self.can_redo():
            self.index += 1

