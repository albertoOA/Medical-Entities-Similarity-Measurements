# !/usr/bin/env python3
class Sequence:
    def __init__(self):
        self.sequence = ''
        self.type = ''

    def __init__(self, sequence, type):
        self.sequence = sequence
        self.type = type

    def printout(self):
        print ('Sequence: ')
        print ('\t> Type: ' + self.type)
        print ('\t> Sequence: ' + self.sequence)
