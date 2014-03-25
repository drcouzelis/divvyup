#include <stdio.h>
#include <fstream>
#include <malloc.h>
#include <iomanip>
#include <iostream>
#include <sstream>

#include "Budget.h"
#include "Utilities.h"


using namespace std;


//
// CSV functions
//


typedef struct
{
  Budget* budget;
  
  int index;
  
  string category;
  string timestamp;
  string reason;
  float amount;
  string action;
  
  bool error;
  
} ParseData;


void
endfield(void *s, size_t len, void *data)
{
  ParseData* record = (ParseData*)data;

  if (record->error) {
    return;
  }
  
  char* field = (char*)s;
  field[len] = '\0';

  switch (record->index) {
  case 0:
    record->category = field;
    break;
  case 1:
    record->timestamp = field;
    break;
  case 2:
    record->reason = field;
    break;
  case 3:
    record->amount = 0;
    sscanf(field, "%f", &(record->amount));
    break;
  case 4:
    record->action = field;
    break;
  }

  record->index++;
}


void
endrecord(int c, void *data)
{
  ParseData* record = (ParseData*)data;

  if (record->error) {
    return;
  }
  
  if (record->action == Transaction::ADD) {
    record->budget->AddMoney(
      record->category,
      record->timestamp,
      record->reason,
	  record->amount
    );
  } else { // Transaction::SUB
    record->budget->RemoveMoney(
      record->category,
      record->timestamp,
      record->reason,
      record->amount
    );
  }

  record->index = 0;
}


//
// Budget
//


Budget::Budget()
  :
  _changed(false),
  _error(false),
  _filename(),
  _name(),
  _categories()
{
  // Empty
}


Budget::Budget(string name, string filename)
  :
  _changed(false),
  _error(false),
  _filename(filename),
  _name(name),
  _categories()
{
  ifstream file(_filename.c_str(), ios::binary);

  // Parse the CSV file
  if (!file) {
    _error = true;
	return;
  }

  csv_parser parser;

  csv_init(&parser, 0);
  
  ParseData record;
  record.budget = this;
  record.index = 0;
  record.error = false;
 
  string buffer;

  while (!file.eof()) {
    getline(file, buffer);
    csv_parse(&parser, buffer.c_str(), buffer.length(), endfield, endrecord, &record);
  }

  csv_fini(&parser, endfield, endrecord, &record);
  
  csv_free(&parser);

  file.close();
}

 
Budget::~Budget()
{
  for (Budget::Iterator i = Begin(); i != End(); i++) {
    delete i->second;
  }
}


bool
Budget::IsError()
{
  return _error;
}


void
Budget::SetName(string name)
{
  _name = name;
}


string
Budget::Name()
{
  return _name;
}


float
Budget::Total()
{
  float total = 0;
  
  for (Budget::Iterator i = Begin(); i != End(); i++) {
    total += i->second->Total();
  }
  
  return total;
}


string
Budget::Filename()
{
  return _filename;
}


void
Budget::SetFilename(string filename)
{
  _filename = filename;
}


bool
Budget::IsChanged()
{
  return _changed;
}


bool
Budget::Save()
{
  if (_filename.empty()) {
    return false;
  }
  
  ofstream file(_filename.c_str());
  
  if (!file) {
    return false;
  }

  // Save each category
  for (Budget::Iterator i = Begin(); i != End(); i++) {
    i->second->Save(file);
  }

  file.close();

  _changed = false;

  return true;
}


void
Budget::AddCategory(string category, float amount)
{
  // Don't do anything if the category already exists
  if (_CategoryExists(category)) {
    return;
  }
  
  Category* c = new Category(category);
  
  // Set the initial amount
  // TODO: Set the timestamp to current time
  Transaction* t = new Transaction("2011030111123", "Initial amount",
    amount, Transaction::ADD);
  
  c->AddTransaction(t);
  
  _categories[category] = c;
}


void
Budget::RemoveCategory(string category)
{
  delete _categories.find(category)->second;
  _categories.erase(category);
}


void
Budget::RenameCategory(string oldname, string newname)
{
  // Don't do anything if the old name doesn't exist
  if (!_CategoryExists(oldname)) {
    return;
  }
  
  // Don't do anything if the new name already exists
  if (_CategoryExists(newname)) {
    return;
  }
  
  // Temporarily remove the category
  Category* c = _categories.find(oldname)->second;
  _categories.erase(oldname);
  
  // Rename it
  c->SetName(newname);
  _categories[newname] = c;
}


float
Budget::PrevAdded(string category)
{
  if (!_CategoryExists(category)) {
    return 0;
  }
  
  Category* c = _categories.find(category)->second;
  
  // Start at the end and work your way back,
  // looking for an ADD transaction
  for (Category::RevIterator i = c->RevBegin(); i != c->RevEnd(); i++) {
    if (i->second->Action() == Transaction::ADD) {
      return i->second->Amount();
	}
  }
  
  // There aren't any transactions
  return 0;
}


float
Budget::PrevRemoved(string category)
{
  if (!_CategoryExists(category)) {
    return 0;
  }
  
  Category* c = _categories.find(category)->second;
  
  // Start at the end and work your way back,
  // looking for a SUB transaction
  for (Category::RevIterator i = c->RevBegin(); i != c->RevEnd(); i++) {
    if (i->second->Action() == Transaction::SUB) {
      return i->second->Amount();
	}
  }
  
  // There aren't any transactions
  return 0;
}


float
Budget::CategoryTotal(string category)
{
  if (!_CategoryExists(category)) {
    return 0;
  }
  
  Category* c = _categories.find(category)->second;
  
  float total = 0;
  
  for (Category::Iterator i = c->Begin(); i != c->End(); i++) {
    total += i->second->Amount();
  }
  
  return total;
}


Budget::CategoryMap*
Budget::Categories()
{
  return &_categories;
}


Budget::Iterator
Budget::Begin()
{
  return _categories.begin();
}


Budget::Iterator
Budget::End()
{
  return _categories.end();
}


void
Budget::AddTransaction(string category, string timestamp, string reason, float amount, string action)
{
  if (!_CategoryExists(category)) {
    _categories[category] = new Category(category);
  }
  
  Category* c = _categories.find(category)->second;
  
  // Create the new transaction
  Transaction* t = new Transaction(timestamp, reason, amount, action);
  
  c->AddTransaction(t);
}


void
Budget::AddMoney(string category, string timestamp, string reason, float amount)
{
  AddTransaction(category, timestamp, reason, amount, Transaction::ADD);
}


void
Budget::RemoveMoney(string category, string timestamp, string reason, float amount)
{
  AddTransaction(category, timestamp, reason, amount, Transaction::SUB);
}


bool
Budget::ChangeDate(string category, string oldtimestamp, string newtimestamp)
{
  if (!_CategoryExists(category)) {
    return false;
  }
  
  Category* c = _categories.find(category)->second;
  
  // Don't do anything if the old timestamp doesn't exist
  if (c->Transactions()->count(oldtimestamp) == 0) {
    return false;
  }
  
  // Don't do anything if the new timestamp already exists
  if (c->Transactions()->count(newtimestamp) > 0) {
    return false;
  }
  
  // Temporarily remove the transaction
  Transaction* t = c->Transactions()->find(oldtimestamp)->second;
  c->Transactions()->erase(oldtimestamp);
  
  // Rename it
  t->SetTimestamp(newtimestamp);
  c->AddTransaction(t);
  
  return true;
}


void
Budget::DeleteTransaction(string category, string timestamp)
{
  if (!_CategoryExists(category)) {
    return;
  }
  
  Category* c = _categories.find(category)->second;
  
  // Delete the transaction
  c->DeleteTransaction(timestamp);
  
  // If the category no longer has any transactions,
  // delete it
  if (c->Transactions()->empty()) {
    RemoveCategory(category);
  }
}


bool
Budget::Combine(Budget* other, string timestamp)
{
  cout << "Pretending to combine" << Name() << " and " << other->Name() << "." << endl;
  return true;
}

 
bool
Budget::_CategoryExists(string category)
{
  if (_categories.count(category) == 0) {
    return false;
  }
  
  return true;
}


//
// Category
//


Category::Category(string name)
  :
  _name(name),
  _transactions()
{
  // Empty
}


Category::~Category()
{
  for (Category::Iterator i = Begin(); i != End(); i++) {
    delete i->second;
  }
};


void
Category::SetName(string name)
{
  _name = name;
}


string
Category::Name()
{
  return _name;
}


float
Category::Total()
{
  float total = 0;
  
  map<string, Transaction*>::iterator it;
  
  for (it = _transactions.begin(); it != _transactions.end(); it++) {
    total += it->second->Amount();
  }
  
  return total;
}


void
Category::Save(ofstream& file)
{
  
  for (Category::Iterator i = Begin(); i != End(); i++) {
    
    Transaction* t = i->second;

    csv_fwrite(file, Name());
    file << ',';

    csv_fwrite(file, t->Timestamp());
    file << ',';

    csv_fwrite(file, t->Reason());
    file << ',';

    ostringstream amount;
    amount.setf(ios::showpoint);
    amount.setf(ios::fixed);
    amount << setprecision(2) << t->Amount();
    csv_fwrite(file, amount.str());
    file << ',';

    csv_fwrite(file, t->Action());
    file << "\r\n"; // Carriage return + line feed (DOS style newline)
  }
}


void
Category::AddTransaction(Transaction* transaction)
{
  if (transaction == NULL) {
    return;
  }
  
  _transactions[transaction->Timestamp()] = transaction;
}


void
Category::DeleteTransaction(string timestamp)
{
  if (_transactions.count(timestamp) > 0) {
    delete _transactions.find(timestamp)->second;
    _transactions.erase(timestamp);
  }
}


Category::TransactionMap*
Category::Transactions()
{
  return &_transactions;
}


Category::Iterator
Category::Begin()
{
  return _transactions.begin();
}


Category::Iterator
Category::End()
{
  return _transactions.end();
}


Category::RevIterator
Category::RevBegin()
{
  return _transactions.rbegin();
}


Category::RevIterator
Category::RevEnd()
{
  return _transactions.rend();
}


//
// Transaction
//


const string Transaction::ADD = "ADD";
const string Transaction::SUB = "SUB";


Transaction::Transaction(string timestamp, string reason, float amount, string action)
  :
  _timestamp(timestamp),
  _reason(reason),
  _amount(amount),
  _action(action)
{
  // Empty
}


void
Transaction::SetTimestamp(string timestamp)
{
  _timestamp = timestamp;
}


string
Transaction::Timestamp()
{
  return _timestamp;
}


string
Transaction::Date()
{
  ostringstream date;
  date << _timestamp.substr(YEAR_IDX, YEAR_LEN) << "-" \
       << _timestamp.substr(MONTH_IDX, MONTH_LEN) << "-" \
       << _timestamp.substr(DAY_IDX, DAY_LEN);
  return date.str();
}


string
Transaction::Reason()
{
  return _reason;
}


float
Transaction::Amount()
{
  return _amount;
}


string
Transaction::Action()
{
  return _action;
}


//
// CSV
//


/* Error Codes */
#define CSV_SUCCESS 0
#define CSV_EPARSE 1   /* Parse error in strict mode */
#define CSV_ENOMEM 2   /* Out of memory while increasing buffer size */
#define CSV_ETOOBIG 3  /* Buffer larger than SIZE_MAX needed */
#define CSV_EINVALID 4 /* Invalid code,should never be received from csv_error*/


/* parser options */
#define CSV_STRICT 1    /* enable strict mode */
#define CSV_REPALL_NL 2 /* report all unquoted carriage returns and linefeeds */
#define CSV_STRICT_FINI 4 /* causes csv_fini to return CSV_EPARSE if last
                             field is quoted and doesn't containg ending 
                             quote */
#define CSV_APPEND_NULL 8 /* Ensure that all fields are null-ternimated */


/* Character values */
#define CSV_TAB    0x09
#define CSV_SPACE  0x20
#define CSV_CR     0x0d
#define CSV_LF     0x0a
#define CSV_COMMA  0x2c
#define CSV_QUOTE  0x22


#define ROW_NOT_BEGUN           0
#define FIELD_NOT_BEGUN         1
#define FIELD_BEGUN             2
#define FIELD_MIGHT_HAVE_ENDED  3


/*
  Explanation of states
  ROW_NOT_BEGUN    There have not been any fields encountered for this row
  FIELD_NOT_BEGUN  There have been fields but we are currently not in one
  FIELD_BEGUN      We are in a field
  FIELD_MIGHT_HAVE_ENDED
                   We encountered a double quote inside a quoted field, the
                   field is either ended or the quote is literal
*/


#define MEM_BLK_SIZE 128


#define SUBMIT_FIELD(p) \
  do { \
   if (!quoted) \
     entry_pos -= spaces; \
   if (p->options & CSV_APPEND_NULL) \
     ((p)->entry_buf[entry_pos+1]) = '\0'; \
   if (cb1) \
     cb1(p->entry_buf, entry_pos, data); \
   pstate = FIELD_NOT_BEGUN; \
   entry_pos = quoted = spaces = 0; \
 } while (0)


#define SUBMIT_ROW(p, c) \
  do { \
    if (cb2) \
      cb2(c, data); \
    pstate = ROW_NOT_BEGUN; \
    entry_pos = quoted = spaces = 0; \
  } while (0)


#define SUBMIT_CHAR(p, c) ((p)->entry_buf[entry_pos++] = (c))


int
csv_init(struct csv_parser *p, unsigned char options)
{
  /* Initialize a csv_parser object returns 0 on success, -1 on error */
  if (p == NULL)
    return -1;

  p->entry_buf = NULL;
  p->pstate = ROW_NOT_BEGUN;
  p->quoted = 0;
  p->spaces = 0;
  p->entry_pos = 0;
  p->entry_size = 0;
  p->status = 0;
  p->options = options;
  p->quote_char = CSV_QUOTE;
  p->delim_char = CSV_COMMA;
  p->is_space = NULL;
  p->is_term = NULL;
  p->blk_size = MEM_BLK_SIZE;
  p->malloc_func = NULL;
  p->realloc_func = realloc;
  p->free_func = free;

  return 0;
}


void
csv_free(struct csv_parser *p)
{
  /* Free the entry_buffer of csv_parser object */
  if (p == NULL)
    return;

  if (p->entry_buf)
    p->free_func(p->entry_buf);

  p->entry_buf = NULL;
  p->entry_size = 0;

  return;
}


int
csv_fini(struct csv_parser *p, void (*cb1)(void *, size_t, void *), void (*cb2)(int c, void *), void *data)
{
  /* Finalize parsing.  Needed, for example, when file does not end in a newline */
  int quoted = p->quoted;
  int pstate = p->pstate;
  size_t spaces = p->spaces;
  size_t entry_pos = p->entry_pos;

  if (p == NULL)
    return -1;


  if (p->pstate == FIELD_BEGUN && p->quoted && p->options & CSV_STRICT && p->options & CSV_STRICT_FINI) {
    /* Current field is quoted, no end-quote was seen, and CSV_STRICT_FINI is set */
    p->status = CSV_EPARSE;
    return -1;
  }

  switch (p->pstate) {
    case FIELD_MIGHT_HAVE_ENDED:
      p->entry_pos -= p->spaces + 1;  /* get rid of spaces and original quote */
      /* Fall-through */
    case FIELD_NOT_BEGUN:
    case FIELD_BEGUN:
      quoted = p->quoted, pstate = p->pstate;
      spaces = p->spaces, entry_pos = p->entry_pos;
      SUBMIT_FIELD(p);
      SUBMIT_ROW(p, -1);
    case ROW_NOT_BEGUN: /* Already ended properly */
      ;
  }

  /* Reset parser */
  p->spaces = p->quoted = p->entry_pos = p->status = 0;
  p->pstate = ROW_NOT_BEGUN;

  return 0;
}


static int
csv_increase_buffer(struct csv_parser *p)
{
  /* Increase the size of the entry buffer.  Attempt to increase size by 
   * p->blk_size, if this is larger than SIZE_MAX try to increase current
   * buffer size to SIZE_MAX.  If allocation fails, try to allocate halve 
   * the size and try again until successful or increment size is zero.
   */

  size_t to_add = p->blk_size;
  void *vp;

  if ( p->entry_size >= 0 - to_add )
    to_add = 0 - p->entry_size;

  if (!to_add) {
    p->status = CSV_ETOOBIG;
    return -1;
  }

  while ((vp = p->realloc_func(p->entry_buf, p->entry_size + to_add)) == NULL) {
    to_add /= 2;
    if (!to_add) {
      p->status = CSV_ENOMEM;
      return -1;
    }
  }

  /* Update entry buffer pointer and entry_size if successful */
  p->entry_buf = (unsigned char *)vp;
  p->entry_size += to_add;
  return 0;
}

 
size_t
csv_parse(struct csv_parser *p, const void *s, size_t len, void (*cb1)(void *, size_t, void *), void (*cb2)(int c, void *), void *data)
{
  unsigned const char *us = (unsigned char *)s;  /* Access input data as array of unsigned char */
  unsigned char c;              /* The character we are currently processing */
  size_t pos = 0;               /* The number of characters we have processed in this call */

  /* Store key fields into local variables for performance */
  unsigned char delim = p->delim_char;
  unsigned char quote = p->quote_char;
  int (*is_space)(unsigned char) = p->is_space;
  int (*is_term)(unsigned char) = p->is_term;
  int quoted = p->quoted;
  int pstate = p->pstate;
  size_t spaces = p->spaces;
  size_t entry_pos = p->entry_pos;


  if (!p->entry_buf && pos < len) {
    /* Buffer hasn't been allocated yet and len > 0 */
    if (csv_increase_buffer(p) != 0) { 
      p->quoted = quoted, p->pstate = pstate, p->spaces = spaces, p->entry_pos = entry_pos;
      return pos;
    }
  }

  while (pos < len) {
    /* Check memory usage, increase buffer if neccessary */
    if (entry_pos == ((p->options & CSV_APPEND_NULL) ? p->entry_size - 1 : p->entry_size) ) {
      if (csv_increase_buffer(p) != 0) {
        p->quoted = quoted, p->pstate = pstate, p->spaces = spaces, p->entry_pos = entry_pos;
        return pos;
      }
    }

    c = us[pos++];

    switch (pstate) {
      case ROW_NOT_BEGUN:
      case FIELD_NOT_BEGUN:
        if (is_space ? is_space(c) : c == CSV_SPACE || c == CSV_TAB) { /* Space or Tab */
          continue;
        } else if (is_term ? is_term(c) : c == CSV_CR || c == CSV_LF) { /* Carriage Return or Line Feed */
          if (pstate == FIELD_NOT_BEGUN) {
            SUBMIT_FIELD(p);
            SUBMIT_ROW(p, (unsigned char)c); 
          } else {  /* ROW_NOT_BEGUN */
            /* Don't submit empty rows by default */
            if (p->options & CSV_REPALL_NL) {
              SUBMIT_ROW(p, (unsigned char)c);
            }
          }
          continue;
        } else if (c == delim) { /* Comma */
          SUBMIT_FIELD(p);
          break;
        } else if (c == quote) { /* Quote */
          pstate = FIELD_BEGUN;
          quoted = 1;
        } else {               /* Anything else */
          pstate = FIELD_BEGUN;
          quoted = 0;
          SUBMIT_CHAR(p, c);
        }
        break;
      case FIELD_BEGUN:
        if (c == quote) {         /* Quote */
          if (quoted) {
            SUBMIT_CHAR(p, c);
            pstate = FIELD_MIGHT_HAVE_ENDED;
          } else {
            /* STRICT ERROR - double quote inside non-quoted field */
            if (p->options & CSV_STRICT) {
              p->status = CSV_EPARSE;
              p->quoted = quoted, p->pstate = pstate, p->spaces = spaces, p->entry_pos = entry_pos;
              return pos-1;
            }
            SUBMIT_CHAR(p, c);
            spaces = 0;
          }
        } else if (c == delim) {  /* Comma */
          if (quoted) {
            SUBMIT_CHAR(p, c);
          } else {
            SUBMIT_FIELD(p);
          }
        } else if (is_term ? is_term(c) : c == CSV_CR || c == CSV_LF) {  /* Carriage Return or Line Feed */
          if (!quoted) {
            SUBMIT_FIELD(p);
            SUBMIT_ROW(p, (unsigned char)c);
          } else {
            SUBMIT_CHAR(p, c);
          }
        } else if (!quoted && (is_space? is_space(c) : c == CSV_SPACE || c == CSV_TAB)) { /* Tab or space for non-quoted field */
            SUBMIT_CHAR(p, c);
            spaces++;
        } else {  /* Anything else */
          SUBMIT_CHAR(p, c);
          spaces = 0;
        }
        break;
      case FIELD_MIGHT_HAVE_ENDED:
        /* This only happens when a quote character is encountered in a quoted field */
        if (c == delim) {  /* Comma */
          entry_pos -= spaces + 1;  /* get rid of spaces and original quote */
          SUBMIT_FIELD(p);
        } else if (is_term ? is_term(c) : c == CSV_CR || c == CSV_LF) {  /* Carriage Return or Line Feed */
          entry_pos -= spaces + 1;  /* get rid of spaces and original quote */
          SUBMIT_FIELD(p);
          SUBMIT_ROW(p, (unsigned char)c);
        } else if (is_space ? is_space(c) : c == CSV_SPACE || c == CSV_TAB) {  /* Space or Tab */
          SUBMIT_CHAR(p, c);
          spaces++;
        } else if (c == quote) {  /* Quote */
          if (spaces) {
            /* STRICT ERROR - unescaped double quote */
            if (p->options & CSV_STRICT) {
              p->status = CSV_EPARSE;
              p->quoted = quoted, p->pstate = pstate, p->spaces = spaces, p->entry_pos = entry_pos;
              return pos-1;
            }
            spaces = 0;
            SUBMIT_CHAR(p, c);
          } else {
            /* Two quotes in a row */
            pstate = FIELD_BEGUN;
          }
        } else {  /* Anything else */
          /* STRICT ERROR - unescaped double quote */
          if (p->options & CSV_STRICT) {
            p->status = CSV_EPARSE;
            p->quoted = quoted, p->pstate = pstate, p->spaces = spaces, p->entry_pos = entry_pos;
            return pos-1;
          }
          pstate = FIELD_BEGUN;
          spaces = 0;
          SUBMIT_CHAR(p, c);
        }
        break;
     default:
       break;
    }
  }
  p->quoted = quoted, p->pstate = pstate, p->spaces = spaces, p->entry_pos = entry_pos;
  return pos;
}


bool
csv_fwrite (ofstream &fp, string src)
{
  if (fp == NULL || fp.eof())
    return false;

  fp << '"';

  for (unsigned int i = 0; i < src.length(); i++) {
    if (src[i] == '"') {
      fp << '"';
    }
    fp << src[i];
  }

  fp << '"';

  return true;
}
