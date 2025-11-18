# csv2qif
Convert credit card and bank CSV exports to QIF files

This utility should be able to handle a wide range of Comma-Separated Value (CSV) files or Excel format files exported from credit card or bank accounts. This software allows you to convert the CSV/Excel statement into a QIF file on your local computer.  QIF format files can be read by many types of financial software such as Quicken.

Usage
-----

Here is how to run this program:

    csv2qif statement.csv > statement.qif

where 'statement.csv' is a CSV file downloaded from a credit card company or bank.
This will create the file 'statement.qif' from the CSV file 'statement.csv'.

The program supports several options. Do:

    csv2qif --help
   
to see the supported options

Automatic Categorization
------------------------

If you provide a 'categories.txt' file in the same directory in which you
execute the **csv2qif** program or in the directory containing the
**csv2qif** program, it will used to automatically assign categories to
transactions if the payee matches know vendors.

**Format of 'categories.txt'**

Each line should have the vendor name, a comma, and then the category
to be used when the payee matches that vendor.  Empty lines are ignored.  A
default version of this file can be kept in the directory of the **csv2qif**
executable.  If a copy of this file is found in the directory that this ommand
is run in, it overrides the version in the executable directory.

Running on Windows
------------------

First you must install Python on your windows system.  See [https://www.python.org/downloads/windows/](to download Python for Windows).

Enjoy!

-Jonathan Cameron
 jmcameron@gmail.com