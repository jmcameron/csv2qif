# csv2qif utils
import sys
import csv

# Prefixes various credit card processing companies insert in payee name
vendor_prefixes = ['GglPay ', 'TST*', 'SQ *', 'IC*', 'UEP*']

def detect(filename: str):
    """
    Do preliminary scan of the CSV file to find 
    the header and other information about the file.

    Args:
        filename (str): The filename for the input CSV file

    Returns:
        dict: the information detected from the csv file:
        {
            'header_line': int,
            'negate': boolean (True if amount values should negated),
            'date': int <index of the date field'>, 
            'description': int <index of the description field'>, 
            'amount': int <index of the amount field'>, 
            'credit': int <index of the credit field (or None if not present)'>, 
            'category': int <index of the category field (or None)'>}
        }
    """
    known_headings = set([
        'amount', 'category', 'credit', 'credits(+)', 'date', 'debit', 'debits(-)',
        'description', 'memo', 'post date', 'transaction date', 'type' ])
    
    header = None
    info = {
        'negate': False
    }
    
    # Do an initial read through to find the header line
    with open(filename) as csvfile:
        for line_number, line in enumerate(csvfile):
            fields = [s.replace('\n', '').lower() for s in line.split(',') if s != '' ]
            intersection = known_headings.intersection(set(fields))
            if len(intersection) >= 3:
                header = fields
                info['header_line'] = line_number
    
    # Find the column for each field we need
    info['date'] = findField(header, 'date', ['date', 'transaction date'])
    info['description'] = findField(header, 'description', ['description'])
    info['amount'] = findField(header, 'amount', ['amount', 'debit', 'debits(-)'])
    info['credit'] = findField(header, 'credit', ['credit', 'credits(+)'])
    info['category'] = findField(header, 'category', ['category'])
    
    # Do another pass through the data to see if we need to negate the amounts
    if 'debit' in header and 'credit' in header:
        info['negate'] = True
    elif 'debits(-)' in header:
        info['negate'] = False
    else:
        num = 0
        num_negative = 0
        with open(filename) as csvfile:
            for line_number, line in enumerate(csvfile):
                if line_number > info['header_line']:
                    fields = [s.replace('\n', '').lower() for s in line.split(',') if s != '' ]
                    amount = sanitizeAmount(fields[info['amount']])
                    num += 1
                    if amount < 0:
                        num_negative += 1            
        info['negate'] = num_negative < num / 3

    return info

def findField(header: list, field: str, altNames):
    """Find column index for 'field'

    Args:
        header (list): list of header fields
        field (str): the canonical name of the field
        altNames (_type_): a list of alternate names for the field

    Returns:
        int: the index of the column for the 'field' or None if not found
    """    
    for name in altNames:
        if name in header:
            return header.index(name)
    return None

def sanitizeAmount(num_str: str):
    """Sanitize the amount

    Args:
        num_str (str): the string version of the amount from the CSV file

    Returns:
        float: the sanitized value
    """
    if num_str == '':
        return 0
    num_str = num_str.removeprefix('$')
    num = num_str.strip('"').replace(',', '')
    return float(num)

def readCategories(filename: str):
    """Read the category data from a file

    Args:
        filename (str): filename for the category file

    Returns:
        dict: { vendor : category, ...}
    """
      
    cats = {}
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i, row in enumerate(csvreader):
            if len(row) == 0:
                # Ignore blank lines
                continue
            if len(row) < 2:
                print("Syntax error in line %d: Need 2 fields separated "
                    "by a comma: vendor, category!" % i, file=sys.stderr)
                print(row, file=sys.stderr)
                continue
            vendor = row[0].strip()
            
            # Strip of known vendor-related prefixes
            for prefix in vendor_prefixes:
                vendor = vendor.removeprefix(prefix)
            vendor = vendor.strip()    
            category = row[1].strip()
            if vendor and category:
                cats[vendor] = category
            else:
                if not vendor:
                    print("Error in line %d: vendor field is "
                            "empty (before the comma)!" % i, file=sys.stderr)
                else:
                    print("Error in line %d: category field for "
                            "vendor='%s' is empty (after the comma)!" % (i, vendor), file=sys.stderr)
                continue
    return cats
