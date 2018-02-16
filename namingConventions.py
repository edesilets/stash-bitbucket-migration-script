import os
import csv
import pprint

class NamingConventions():
    results = []
    csvPath = ''

    def __init__(self):
        print "hello"
        self.setCSVpath()

    def setCSVpath(self):
        self.csvPath = os.path.normpath(os.getcwd()+"/test/update-names.csv")

    def csvArray(self):
        with open(self.csvPath) as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
            for row in reader: # each row is a list
                self.results.append(row)
        return self.results
