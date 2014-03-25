#ifndef UTILITIES_H
#define UTILITIES_H


#include <iomanip>
#include <sstream>
#include <string>


using namespace std;


//
// Timestamp helpers
//

const int YEAR_IDX = 0;
const int YEAR_LEN = 4; // YYYY
const int MONTH_IDX = 4;
const int MONTH_LEN = 2; // MM
const int DAY_IDX = 6;
const int DAY_LEN = 2; // DD

const int TIME_IDX = 8;
const int TIME_LEN = 10; // HHMMSSMMMM


string CurrTimestamp();

string DateToTimestamp(string oldtimestamp, string formatteddate);
string TimestampToDate(string timestamp);

string FormatAmount(float amount);


#endif
