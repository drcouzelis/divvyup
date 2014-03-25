#ifndef COMMAND_H
#define COMMAND_H


#include <list>
#include <string>


using namespace std;


class Budget;
class Category;
class Transaction;

class Command;
class AddCategoryCommand;
class RemoveCategoryCommand;
class RenameCategoryCommand;
class AddMoneyCommand;
class RemoveMoneyCommand;
class ChangeDateCommand;
class DeleteTransactionCommand;
class CombineCommand;


class Command
{
public:
  Command();
  virtual ~Command();
  virtual void SetDocument(Budget* document);
  virtual void Apply() = 0;
  virtual void Undo() = 0;
protected:
  Budget* _document; // The command does not own the document
};


class AddCategoryCommand : public Command
{
public:
  AddCategoryCommand(string category, float amount);
  virtual ~AddCategoryCommand();
  virtual void Apply();
  virtual void Undo();
private:
  string _category;
  float _amount;
};


class RemoveCategoryCommand : public Command
{
public:
  RemoveCategoryCommand(string category);
  virtual ~RemoveCategoryCommand();
  virtual void SetDocument(Budget* document);
  virtual void Apply();
  virtual void Undo();
private:
  string _category;
  list<Transaction*> _transactions;
};


class RenameCategoryCommand : public Command
{
public:
  RenameCategoryCommand(string oldname, string newname);
  virtual ~RenameCategoryCommand();
  virtual void Apply();
  virtual void Undo();
private:
  string _oldname;
  string _newname;
};


class AddMoneyCommand : public Command
{
public:
  AddMoneyCommand(string category, string timestamp, string reason, float amount);
  virtual ~AddMoneyCommand();
  virtual void Apply();
  virtual void Undo();
private:
  string _category;
  string _timestamp;
  string _reason;
  float _amount;
};


class RemoveMoneyCommand : public Command
{
public:
  RemoveMoneyCommand(string category, string timestamp, string reason, float amount);
  virtual ~RemoveMoneyCommand();
  virtual void Apply();
  virtual void Undo();
private:
  string _category;
  string _timestamp;
  string _reason;
  float _amount;
};


class ChangeDateCommand : public Command
{
public:
  ChangeDateCommand(string category, string oldtimestamp, string newtimestamp);
  virtual ~ChangeDateCommand();
  virtual void Apply();
  virtual void Undo();
private:
  string _category;
  string _oldtimestamp;
  string _newtimestamp;
};


class DeleteTransactionCommand : public Command
{
public:
  DeleteTransactionCommand(string category, string timestamp, string reason, float amount, string action);
  virtual ~DeleteTransactionCommand();
  virtual void Apply();
  virtual void Undo();
private:
  string _category;
  string _timestamp;
  string _reason;
  float _amount;
  string _action;
};


class CombineCommand : public Command
{
public:
  CombineCommand(Budget* other, string timestamp);
  virtual ~CombineCommand();
  virtual void Apply();
  virtual void Undo();
private:
  Budget* _other;
  string _timestamp;
};


#endif
