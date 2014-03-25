#include "Budget.h"
#include "Command.h"


using namespace std;


Command::Command()
  :
  _document(NULL)
{
  // Empty
}


Command::~Command()
{
  // Empty
}


void
Command::SetDocument(Budget* document)
{
  _document = document;
}


//
// Add Category Command
//


AddCategoryCommand::AddCategoryCommand(string category, float amount)
  :
  Command(),
  _category(category),
  _amount(amount)
{
  // Empty
}


AddCategoryCommand::~AddCategoryCommand()
{
  // Empty
}


void
AddCategoryCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  _document->AddCategory(_category, _amount);
}


void
AddCategoryCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  _document->RemoveCategory(_category);
}


//
// Remove Category Command
//


RemoveCategoryCommand::RemoveCategoryCommand(string category)
  :
  Command(),
  _category(category),
  _transactions()
{
  // Empty
}


RemoveCategoryCommand::~RemoveCategoryCommand()
{
  list<Transaction*>::iterator it;
  
  for (it = _transactions.begin(); it != _transactions.end(); it++) {
    delete *it;
  }
}


void
RemoveCategoryCommand::SetDocument(Budget* document)
{
  Command::SetDocument(document);
  
  list<Transaction*>::iterator list_it;
  
  // Delete any old transactions (there probably aren't any)
  for (list_it = _transactions.begin(); list_it != _transactions.end(); list_it++) {
    delete *list_it;
  }
  
  Category* c = _document->Categories()->find(_category)->second;
  
  // Save all of the transactions that are in this category
  for (Category::Iterator i = c->Begin(); i != c->End(); i++) {
    Transaction* t = i->second;
    Transaction* new_t = new Transaction(t->Timestamp(), t->Reason(), t->Amount(), t->Action());
    _transactions.push_back(new_t);
  }
}


void
RemoveCategoryCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  // This will delete the category and all of its transactions
  _document->RemoveCategory(_category);
}


void
RemoveCategoryCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  // Add the category and all of its transactions
  // back into the budget
  list<Transaction*>::const_iterator it;
  
  for (it = _transactions.begin(); it != _transactions.end(); it++) {
    Transaction* t = *it;
    _document->AddTransaction(_category, t->Timestamp(), t->Reason(), t->Amount(), t->Action());
  }
}


//
// Remove Category Command
//


RenameCategoryCommand::RenameCategoryCommand(string oldname, string newname)
  :
  Command(),
  _oldname(oldname),
  _newname(newname)
{
  // Empty
}


RenameCategoryCommand::~RenameCategoryCommand()
{
  // Empty
}


void
RenameCategoryCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  _document->RenameCategory(_oldname, _newname);
}


void
RenameCategoryCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  _document->RenameCategory(_newname, _oldname);
}


//
// Add Money Command
//


AddMoneyCommand::AddMoneyCommand(string category, string timestamp, string reason, float amount)
  :
  Command(),
  _category(category),
  _timestamp(timestamp),
  _reason(reason),
  _amount(amount)
{
  // Empty
}


AddMoneyCommand::~AddMoneyCommand()
{
  // Empty
}


void
AddMoneyCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  _document->AddMoney(_category, _timestamp, _reason, _amount);
}


void
AddMoneyCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  _document->DeleteTransaction(_category, _timestamp);
}


//
// Remove Money Command
//


RemoveMoneyCommand::RemoveMoneyCommand(string category, string timestamp, string reason, float amount)
  :
  Command(),
  _category(category),
  _timestamp(timestamp),
  _reason(reason),
  _amount(amount)
{
  // Empty
}


RemoveMoneyCommand::~RemoveMoneyCommand()
{
  // Empty
}


void
RemoveMoneyCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  _document->RemoveMoney(_category, _timestamp, _reason, _amount);
}


void
RemoveMoneyCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  _document->DeleteTransaction(_category, _timestamp);
}


//
// Change Date Command
//


ChangeDateCommand::ChangeDateCommand(string category, string oldtimestamp, string newtimestamp)
  :
  Command(),
  _category(category),
  _oldtimestamp(oldtimestamp),
  _newtimestamp(newtimestamp)
{
  // Empty
}


ChangeDateCommand::~ChangeDateCommand()
{
  // Empty
}


void
ChangeDateCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  _document->ChangeDate(_category, _oldtimestamp, _newtimestamp);
}


void
ChangeDateCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  _document->ChangeDate(_category, _newtimestamp, _oldtimestamp);
}


//
// Delete Transaction Command
//


DeleteTransactionCommand::DeleteTransactionCommand(string category, string timestamp, string reason, float amount, string action)
  :
  Command(),
  _category(category),
  _timestamp(timestamp),
  _reason(reason),
  _amount(amount),
  _action(action)
{
  // Empty
}


DeleteTransactionCommand::~DeleteTransactionCommand()
{
  // Empty
}


void
DeleteTransactionCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  _document->DeleteTransaction(_category, _timestamp);
}


void
DeleteTransactionCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  _document->AddTransaction(_category, _timestamp, _reason, _amount, _action);
}


//
// Combine Command
//


CombineCommand::CombineCommand(Budget* other, string timestamp)
  :
  Command(),
  _other(other),
  _timestamp(timestamp)
{
  // Empty
}


CombineCommand::~CombineCommand()
{
  delete _other;
}


void
CombineCommand::Apply()
{
  if (_document == NULL) {
    return;
  }
  
  _document->Combine(_other, _timestamp);
}


void
CombineCommand::Undo()
{
  if (_document == NULL) {
    return;
  }
  
  // Delete the transactions in every category that
  // have this timestamp
  for (Budget::Iterator i = _other->Begin(); i != _other->End(); i++) {
    _document->DeleteTransaction(i->second->Name(), _timestamp);
  }
}
