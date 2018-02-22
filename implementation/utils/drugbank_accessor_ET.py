# !/usr/bin/env python3
import xml.etree.cElementTree as ET
import nltk
from scipy.spatial.distance import *
from nltk.stem.porter import PorterStemmer
import string
import numpy as np
import re as re
import os
import sys


HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(HERE, ".."))

from classes.Classification import Classification
from classes.Drug import Drug
from classes.Sequence import Sequence

def map_drugbank_from_file(file):
    # file = open(filename, 'r')
    tree = ET.parse(file)
    # file.close()
    #drugs = []
    drugs = {}
    # dictionary with the namespaces
    ns = {'drugbank': 'http://www.drugbank.ca', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

    # iterate over all drugs - children of drugbank
    count = 0
    for drugtag in tree.getroot():
        ids = drugtag.findall('drugbank:drugbank-id', ns)
        primary = drugtag.find("drugbank:drugbank-id[@primary='true']", ns).text


        other_ids = []
        for other in ids:
            if other.text != primary:
                if other.text ==None:
                    other.text = ''
                other_ids.append(other.text)

        name = drugtag.find('drugbank:name', ns).text
        # Prints the drug names which are no strings (strange chars)
        if (not isinstance(name, str)):
            print('id: ' + primary + ' name: ' + name)
        description = drugtag.find('drugbank:description', ns).text
        indication = drugtag.find('drugbank:indication', ns).text
        pharmacodynamics = drugtag.find('drugbank:pharmacodynamics',ns).text

        #check if any of the texts are None, primary and name shouldn't be none so not checking for them
        if description == None:
            description = ''
        if indication ==None:
            indication = ''
        if pharmacodynamics==None:
            pharmacodynamics = ''

        classification = None
        classificationtag = drugtag.find('drugbank:classification', ns)
        if classificationtag != None:
            class_description = classificationtag.find('drugbank:description', ns).text
            direct_parent = classificationtag.find('drugbank:direct-parent', ns).text
            kingdom = classificationtag.find('drugbank:kingdom', ns).text
            superclass = classificationtag.find('drugbank:superclass', ns).text
            class_type = classificationtag.find('drugbank:class', ns).text
            subclass = classificationtag.find('drugbank:subclass', ns).text

            # check if any of the texts are None
            if class_description == None:
                class_description = ''
            if direct_parent == None:
                direct_parent = ''
            if kingdom == None:
                kingdom = ''
            if superclass == None:
                superclass = ''
            if class_type == None:
                class_type = ''
            if subclass == None:
                subclass = ''
            classification =  Classification(class_description, direct_parent, kingdom, superclass,
                                             class_type, subclass)
        synonyms = []
        synonymstag = drugtag.find('drugbank:synonyms', ns)
        for syn in synonymstag:
            synonyms.append(syn.text)

        international_brands = []
        ibstag = drugtag.find('drugbank:international-brands', ns)
        for ib in ibstag:
            ibname = ib.find('drugbank:name', ns).text
            international_brands.append(ibname)

        categories = []
        catstag = drugtag.find('drugbank:categories', ns)
        for cat in catstag:
            catname = cat.find('drugbank:category', ns).text
            categories.append(catname)

        sequences = []
        seqstag = drugtag.find('drugbank:sequences', ns)
        if seqstag!= None:
            for seq in seqstag:
                seqdict = seq.attrib
                seqtype = seqdict.get('format')
                seqname = seq.text
                sequences.append(Sequence(seqname, seqtype))

        molecular_weight = 0.0
        molecular_formula = ''
        propstag = drugtag.find('drugbank:experimental-properties', ns)
        for prop in propstag:
            propkind = prop.find('drugbank:kind', ns).text
            if propkind == 'Molecular Weight':
                molecular_weight = prop.find('drugbank:value', ns).text
            if propkind == 'Molecular Formula':
                molecular_formula = prop.find('drugbank:value', ns).text

        pathways_drugs = []
        pathways_enzymes = []
        pathwaystag = drugtag.find('drugbank:pathways', ns)
        if pathwaystag != None:
            for pathwaytag in pathwaystag:
                drugstag_pw = pathwaytag.find('drugbank:drugs', ns)
                for drugtag_pw in drugstag_pw:
                    drugid = drugtag_pw.find('drugbank:drugbank-id', ns).text
                    pathways_drugs.append(drugid)
                enzymestag = pathwaytag.find('drugbank:enzymes', ns)
                if enzymestag != None:
                    for uniprot in enzymestag:
                        #uniprotid = enzymetag.find('drugbank:uniprot-id', ns).text
                        pathways_enzymes.append(uniprot.text)

        # atc_code = ''
        # atccode = drugtag.find('drugbank:atc-codes/drugbank:atc-code', ns)
        # if atccode != None:
        #     atc_code = atccode.attrib["code"]

        atc_codes = []
        atccodes = drugtag.find('drugbank:atc-codes', ns)
        for atccode in atccodes:
            #mm = atccode.find('drugbank:atc-code', ns)
            atc_code = atccode.attrib["code"]
            if atc_code!=None:
                atc_codes.append(atc_code)

        if(description!='' and pharmacodynamics != '' and classification != None and atc_codes !=[]):

            drug = Drug(primary, other_ids, name, description, indication, pharmacodynamics,
                        classification, synonyms, international_brands,
                        categories, sequences, molecular_weight, molecular_formula, pathways_drugs, pathways_enzymes, atc_codes)
            drugs[primary] = drug

    return drugs

def drug_term_dictionary(drugs, kys, attr="description"):
    if type(attr) is not list:
        attrs = [attr]
    else:
        attrs = attr

    token_list = [None] * len(kys)
    n_non_empty_drugs = 0
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    for i in kys.keys():
        # Add more text processing: remove numbers, etc
        text = ''
        for a in attrs:
            text = text + ' ' + getattr(drugs[kys[i]], a)
        text = regex.sub('', text)
        if len(text) > 0:
            n_non_empty_drugs += 1
            token_list[i] = text.lower()#.translate(string.punctuation)
    print(len(drugs) - n_non_empty_drugs, " drugs found with empty fields")
    return token_list

def drug_term_dictionary2(drugs, attr="description"):
    token_dict = {}
    drug_list = drugs.keys()
    n_non_empty_drugs = 0
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    for d in drug_list:
        # Add more text processing: remove numbers, etc
        text = getattr(drugs[d], attr)
        text = regex.sub('', text)
        if len(text) > 0:
            n_non_empty_drugs += 1
            token_dict[d] = text.lower()#.translate(string.punctuation)
    print(len(drug_list) - n_non_empty_drugs, " drugs found with empty " + attr + " field")
    return token_dict

def tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
    return stems

def cosine(vector1, vector2):
    """
    related documents j and q are in the concept space by comparing the vectors :
    cosine  = ( V1 * V2 ) / ||V1|| x ||V2||
    """
    return float(np.dot(vector1,vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))

def upper_tri_as_list(matr):
    tri_list = []
    n = matr.shape[0]
    # iterates over the keys
    for i in range(0,n):
        for j in range(i+1, n):
            tri_list.append(matr[i,j])
    return tri_list