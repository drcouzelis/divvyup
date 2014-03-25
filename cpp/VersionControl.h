#ifndef VERSIONCONTROL_H
#define VERSIONCONTROL_H


#include <vector>


using namespace std;


class Budget;
class Command;

class VersionControl;


class VersionControl
{
public:
  VersionControl(Budget* document);
  ~VersionControl();

  void ApplyCommand(Command* command);
  
  Budget* Document();

  void Undo();
  void Redo();
  
  bool CanUndo();
  bool CanRedo();
  
private:
  Budget* _document; // Version control will delete the document
  
  vector<Command*> _commands; // Version control will delete the commands
  unsigned int _currcommand;
  unsigned int _savedcommand;
};


#endif
