# !/usr/bin/env python3
class Classification:

    def __init__(self):
        self.description = ''
        self.direct_parent = ''
        self.kingdom = ''
        self.superclass = ''
        self.class_type =''
        self.subclass = ''

    def __init__(self, description, direct_parent, kingdom, superclass, class_type, subclass):
        self.description = description
        self.direct_parent = direct_parent
        self.kingdom = kingdom
        self.superclass = superclass
        self.class_type = class_type
        self.subclass = subclass

    def printout(self):
        print ('Classification: ')
        print ('\t> Description: ' + self.description)
        print ('\t> Direct parent: ' + self.direct_parent)
        print  ('\t> Kingdom: ' + self.kingdom)
        print ('\t> Superclass: ' + self.superclass)
        print ('\t> Class: ' + self.class_type)
        print ('\t> Subclass: ' + self.subclass)


  ## Example of how the information realted to 'Classification' appears in DrugBank database.
  # <classification>
  #   <description/>
  #   <direct-parent>Peptides</direct-parent>
  #   <kingdom>Organic Compounds</kingdom>
  #   <superclass>Organic Acids</superclass>
  #   <class>Carboxylic Acids and Derivatives</class>
  #   <subclass>Amino Acids, Peptides, and Analogues</subclass>
  # </classification>