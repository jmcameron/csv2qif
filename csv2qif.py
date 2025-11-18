import os
import sys
import csv
from dateutil import parser
from datetime import datetime

from utils import detect, readCategories, sanitizeAmount, vendor_prefixes

exec_dir = os.path.dirname(os.path.realpath(__file__))

def csv2qif(args: object):
    
    # Process the output filename
    OUTPUT = args.output
    if type(args.output) == str:
        OUTPUT = open(args.output, 'w')
    
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
    with open(args.csvfilename, 'r') as csvfile:
        # Skip lines if necessary
        for _ in range(SKIP_LINES):
            next(csvfile)
            
        csv_reader = csv.reader(csvfile)
       
        # Read and process the data
        for line_num, fields in enumerate(csv_reader, start=1):
            if line_num == 1:
                header = fields
                continue
            if len(fields) == 0:
                # Skip blank lines
                continue

            # Extract the data
            payee = fields[PAYEE].strip()
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
        print("D%s" % line['date'], file=OUTPUT)
        print("T%.2f" % line['amount'], file=OUTPUT)
        print("P%s" % line['payee'], file=OUTPUT)
        print("L%s" % line['category'], file=OUTPUT)
        if line['memo']:
            print("M%s" % line['memo'], file=OUTPUT)
        print("^", file=OUTPUT)

    if args.complain:
        print("\nUnrecognized Payees:", file=sys.stderr)
        for payee in sorted([s for s in unknown_payees]):
            print("   %s" % payee, file=sys.stderr)

    if type(args.output) == str:
        OUTPUT.close()