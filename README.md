# barcode-search

A simple ArchivesSpace barcode lookup tool. Returns a CSV containing collection and container data for each barcode.

## Requirements

* Python 3.4+
* `requests` module
* ArchivesSpace 2.4+

__NOTE:__ If running the executable files, the Python-related requirements will automatically be installed.

## Quick Start

* Clone or download repository.
* If using executable file: Mac users open `barcode_search_mac` file, PC users open `barcode_search.exe`.
* If using `.py` file:

```
$ cd /Users/username/pathtofile
$ python barcode_search.py
``` 

## Tutorial

`barcode_search` is a simple command-line tool that searches for barcodes via the ArchivesSpace API, and returns a CSV file containing collection and container data needed to track the off-site transfers of Yale's Manuscripts and Archives department. To use the program, click on the appropriate executable file and follow the on-screen prompts:

1. Enter ArchivesSpace login information

Enter the URL for the ArchivesSpace API and your ArchivesSpace username and password to connect to the system.

2. Enter path to input CSV file

The tool takes a CSV like the included barcodes.csv example file as input. Be sure to include a header in the CSV file, as the tool skips the first row. At this point the tool will create an output CSV file in the same directory as the input CSV.

3. Wait...

The script should continue running even if it encounters an error retrieving data from ArchivesSpace. If for some reason it stops before finishing, please submit an [issue](https://github.com/ucancallmealicia/barcode_search/issues). Please include a description of any error messages received.

4. Review outfiles!

The tool creates two outfiles - a program log and a CSV outfile containing collection and container data. 

The log file contains status and error messages recorded during script runtime.

The following data is included on the output CSV:

* Barcode
* Series
* Collection identifier
* Collection title
* Container profile
* Container number

Both files will open automatically after the script finishes.
