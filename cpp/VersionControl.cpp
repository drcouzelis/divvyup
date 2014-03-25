#include "Budget.h"
#include "Command.h"
#include "VersionControl.h"


VersionControl::VersionControl(Budget* document)
  :
  _document(document),
  _commands(),
  _currcommand(0),
  _savedcommand(0)
{
  // Empty
}


VersionControl::~VersionControl()
{
  vector<Command*>::iterator it;
  
  for (it = _commands.begin(); it != _commands.end(); it++) {
    delete *it;
  }
  
  delete _document;
}


void
VersionControl::ApplyCommand(Command* command)
{
  command->SetDocument(_document);
  
  _commands.push_back(command);
  Redo();
  
  vector<Command*>::iterator it;
  
  // Delete any commands that come after this
  // Start at the location of the current command
  for (it = _commands.begin() + _currcommand; it != _commands.end(); it++) {
    delete *it;
    it = _commands.erase(it);
  }
}

Budget*
VersionControl::Document()
{
  return _document;
}


void
VersionControl::Undo()
{
  if (CanUndo()) {
    _commands[_currcommand - 1]->Undo();
    _currcommand--;
  }
}


void
VersionControl::Redo()
{
  if (CanRedo()) {
    _currcommand++;
    _commands[_currcommand - 1]->Apply();
  }
}


bool
VersionControl::CanUndo()
{
  if (_currcommand > 0) {
    return true;
  }
  
  return false;
}


bool
VersionControl::CanRedo()
{
  if (_currcommand < _commands.size()) {
    return true;
  }
  
  return false;
}

