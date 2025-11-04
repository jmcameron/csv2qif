import os
import sys
from dateutil import parser
from datetime import datetime

from utils import detect, readCategories, sanitizeAmount, vendor_prefixes

exec_dir = os.path.dirname(os.path.realpath(__file__))

def csv2qif(args: object):
   
    # First, read the categories
    catmap = {}
    if os.path.exists('categories.txt'):
       # Local version overrides one in executable directory
       catmap = readCategories('categories.txt')
    elif os.path.exists(os.path.join(exec_dir, 'categories.txt')):
       catmap = readCategories(os.path.join(exec_dir, 'categories.txt'))
    else:
       catmap = {}

    # If printing categories is request, print them and exit
    if args.printcats:
        print()
        print("CATEGORIES:")
        vendlen = max([len(v) for v in catmap])
        fmt = "  %%%ds: %%s" % vendlen
        for vend in sorted(catmap.keys()):
            cat = catmap[vend]
            print(fmt % (vend, cat))
        print()
        sys.exit()
        
    # Get the info about the CSV file
    info = detect(args.csvfilename)
    NEGATE = info['negate']
    SKIP_LINES = info['header_line']
    DATE = info['date']
    PAYEE = info['description']
    AMOUNT = info['amount']
    CREDIT = info['credit']
    CATEGORY = info['category']
    
    # Read the data from the csvfile
    unknown_payees = set()
    header = None
    data = []
    
    # Read the csv file
    with open(args.csvfilename, 'r') as f:
        # Skip lines if necessary
        for _ in range(SKIP_LINES):
            next(f)
        header_raw = f.readline()
        
        # Read and process the data
        lines = f.readlines()
        for line in lines:
            if len(line.strip()) == 0:
                # Skip blank lines
                continue
            if line.find('Beginning balance') >= 0:
                # Skip irrelevant line
                continue
            fields = [s.strip() for s in line.split(',')]
            payee = fields[PAYEE]
            for prefix in vendor_prefixes:
                payee = payee.removeprefix(prefix)
            payee = " ".join(payee.strip().split())  # Remove extra blanks
            date_str = fields[DATE].strip()
            date = parser.parse(date_str)
            line_data = {
                'date' : date.strftime("%m/%d/%Y"),
                'payee' : payee,   
                'amount' : sanitizeAmount(fields[AMOUNT]),
                'category' : fields[CATEGORY] if CATEGORY != None else None,
                'credit' : fields[CREDIT] if CREDIT != None else None,
                'memo' : None,
            }
            data.append(line_data)

    # Process the header (for reference, if necessary)    
    header = [s.lower().strip() for s in header_raw.split(',')]
            
    # Do one more pass over the data to fix things
    has_credit = CREDIT != None
    negate = -1 if NEGATE else 1
    for line in data:
        # Fix the amount
        amount = negate * line['amount']
        if has_credit and line['credit'] != '':
            # Override the amount with the credit, if available   
            amount = sanitizeAmount(line['credit'])
        line['amount'] = amount

        # Check for known payees
        payee = line['payee']
        category = ''
        for p, cat in catmap.items():
            if payee.upper().startswith(p.upper()):
                category = cat
        if category == '':
            # If the payee is unknown, insert the suggested
            # category as a memo for the users reference
            unknown_payees.add(payee.upper())
            line['memo'] = line['category']
            line['category'] = ''
        else:
            line['category'] = category

    for line in data:
        print("D%s" % line['date'])
        print("T%.2f" % line['amount'])
        print("P%s" % line['payee'])
        print("L%s" % line['category'])
        if line['memo']:
            print("M%s" % line['memo'])
        print("^")

    if args.complain:
        print("\nUnrecognized Payees:", file=sys.stderr)
        for payee in sorted([s for s in unknown_payees]):
            print("   %s" % payee, file=sys.stderr)
