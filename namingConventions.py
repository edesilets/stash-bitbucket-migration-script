import os
import csv
import pprint

class NamingConventions():
    TSV_FILE = '\t'
    CSV_FILE = ','
    results  = {}
    csvPath  = ''

    def __init__(self):
        self.setCSVpath()

    def setCSVpath(self):
        self.csvPath = os.path.normpath(os.getcwd()+"/test/update-names.tsv")

    def csvArray(self):
        with open(self.csvPath) as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
            for row in reader: # each row is a list
                self.results.append(row)
        return self.results

    def svDict(self, TSV_or_CSV = TSV_FILE):
        if not isinstance(TSV_or_CSV, basestring):
            print "delimiter must be TSV_FILE, CSV_FILE, or string delimiter"

        # to ignore HEADERS in file. No auto-detect headers.
        i = 0
        with open(self.csvPath, mode='r') as csvfile:
            reader = csv.reader(csvfile, delimiter=TSV_or_CSV)
            for row in reader:
                if not i == 0:
                    self.results[row[0]] = {
                            "new_name": row[1],
                            "new_key": row[2],
                            "description": row[3]
                        }
                i+=1
