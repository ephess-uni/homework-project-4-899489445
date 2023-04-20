# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date in old_dates:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
        new_date = datetime_obj.strftime('%d %b %Y')
        new_dates.append(new_date)
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("Start date must be a string.")
    if not isinstance(n, int):
        raise TypeError("Number of days must be an integer.")
    start_date = datetime.strptime(start, '%Y-%m-%d')
    dates = [start_date + timedelta(days=i) for i in range(n)]
    return dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    if not isinstance(start_date, str):
        raise TypeError("start_date must be a string")
    date_objects = date_range(start_date, len(values))
    return list(zip(date_objects, values))



def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees_by_patron = defaultdict(float)

    with open(infile, 'r') as f:
        reader = DictReader(f)
        
        for row in reader:
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            
            days_late = (date_returned - date_due).days
            if days_late > 0:
                late_fee = days_late * 0.25
                
                late_fees_by_patron[row['patron_id']] += late_fee

    with open(outfile, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        
        for patron_id, late_fees in late_fees_by_patron.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': '{:.2f}'.format(late_fees)})


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
