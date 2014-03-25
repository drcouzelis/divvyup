#include "Utilities.h"


string
CurrTimestamp()
{
  return string("2011030111123");
}


string
DateToTimestamp(string oldtimestamp, string formatteddate)
{
  // A formatted date has hyphens and no time: YYYY-MM-DD
  ostringstream newdate;
  newdate << formatteddate.substr(YEAR_IDX, YEAR_LEN) \
          << formatteddate.substr(MONTH_IDX + 1, MONTH_LEN) \
          << formatteddate.substr(DAY_IDX + 2, DAY_LEN);
  return newdate.str() + oldtimestamp.substr(TIME_IDX, TIME_LEN);
}


string
TimestampToDate(string timestamp)
{
  ostringstream date;
  date << timestamp.substr(YEAR_IDX, YEAR_LEN) << "-" \
       << timestamp.substr(MONTH_IDX, MONTH_LEN) << "-" \
       << timestamp.substr(DAY_IDX, DAY_LEN);
  return date.str();
}


string
FormatAmount(float amount)
{
  ostringstream stream;
  stream.setf(ios::showpoint);
  stream.setf(ios::fixed);
  stream << setprecision(2) << amount;
  return stream.str();
}
