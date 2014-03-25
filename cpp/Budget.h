#ifndef BUDGET_H
#define BUDGET_H


#include <map>
#include <string>


using namespace std;


class Command;

class Budget;
class Category;
class Transaction;


class Budget
{
public:
  typedef map<string, Category*> CategoryMap;
  typedef CategoryMap::iterator Iterator;
  
  
  Budget();
  Budget(string name, string filename);
  
  ~Budget();
  
  bool IsError();
  
  void SetName(string name);
  string Name();
  
  float Total();
  
  // File management
  void SetFilename(string filename);
  string Filename();
  
  bool IsChanged();
  
  bool Save();
  
  // Categories
  void AddCategory(string category, float amount);
  void RemoveCategory(string category);
  void RenameCategory(string oldname, string newname);
  
  float PrevAdded(string category);
  float PrevRemoved(string category);
  float CategoryTotal(string category);
  
  Budget::CategoryMap* Categories();
  
  Budget::Iterator Begin();
  Budget::Iterator End();
  
  // Transactions
  void AddTransaction(string category, string timestamp, string reason, float amount, string action);
  void AddMoney(string category, string timestamp, string reason, float amount);
  void RemoveMoney(string category, string timestamp, string reason, float amount);
  bool ChangeDate(string category, string oldtimestamp, string newtimestamp);
  void DeleteTransaction(string category, string timestamp);
  
  bool Combine(Budget* other, string timestamp);
  
private:
  void _SetChanged();
  bool _CategoryExists(string category);
  void _SetError();

  bool _changed;
  bool _error;

  string _filename;
  string _name;

  Budget::CategoryMap _categories;
};


class Category
{
public:
  typedef map<string, Transaction*> TransactionMap;
  typedef TransactionMap::iterator Iterator;
  typedef TransactionMap::reverse_iterator RevIterator;

  Category(string name);
  ~Category();

  void SetName(string name);
  string Name();

  float Total();
  
  void Save(ofstream& file);
  
  // Transactions
  void AddTransaction(Transaction* transaction);
  void DeleteTransaction(string timestamp);
  
  Category::TransactionMap* Transactions();
  
  Category::Iterator Begin();
  Category::Iterator End();
  
  Category::RevIterator RevBegin();
  Category::RevIterator RevEnd();
  
private:
  string _name;
  TransactionMap _transactions;
};


class Transaction
{
public:
  static const string ADD;
  static const string SUB;

  Transaction(string timestamp, string reason, float amount, string action);

  void SetTimestamp(string timestamp);
  string Timestamp();
  
  string Date();
  string Reason();
  float Amount();
  string Action();

private:
  string _timestamp;
  string _reason;
  float _amount;
  string _action;
};


//
// CSV
//


struct csv_parser {
  int pstate;         /* Parser state */
  int quoted;         /* Is the current field a quoted field? */
  size_t spaces;      /* Number of continious spaces after quote or in a non-quoted field */
  unsigned char * entry_buf;   /* Entry buffer */
  size_t entry_pos;   /* Current position in entry_buf (and current size of entry) */
  size_t entry_size;  /* Size of entry buffer */
  int status;         /* Operation status */
  unsigned char options;
  unsigned char quote_char;
  unsigned char delim_char;
  int (*is_space)(unsigned char);
  int (*is_term)(unsigned char);
  size_t blk_size;
  void *(*malloc_func)(size_t);
  void *(*realloc_func)(void *, size_t);
  void (*free_func)(void *);
};


int csv_init(struct csv_parser *p, unsigned char options);
int csv_fini(struct csv_parser *p, void (*cb1)(void *, size_t, void *), void (*cb2)(int, void *), void *data);
void csv_free(struct csv_parser *p);
size_t csv_parse(struct csv_parser *p, const void *s, size_t len, void (*cb1)(void *, size_t, void *), void (*cb2)(int, void *), void *data);
bool csv_fwrite(ofstream &fp, string src);


#endif
