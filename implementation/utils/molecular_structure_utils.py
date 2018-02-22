# !/usr/bin/env python3
import copy
import rdkit.DataStructs
import xml.etree.cElementTree as ET

def similarity_matrix_molecular_structure(fpsDic, coeficient):
    dists = []
    
    fps = copy.deepcopy(list(fpsDic.values()))
    nfps = len(fps)

    if coeficient == "tanimoto":
        for i in range(0,nfps):
            sims = rdkit.DataStructs.BulkTanimotoSimilarity(fps[i],fps)
            dists.append(sims)
    elif coeficient == "dice":
        for i in range(0,nfps):
            sims = rdkit.DataStructs.BulkDiceSimilarity(fps[i],fps)
            dists.append(sims)

    return dists

def drugbank_id_atc_dictionary(file):
    tree = ET.parse(file)
    drugs = {}
    # dictionary with the namespaces
    ns = {'drugbank': 'http://www.drugbank.ca', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

    # iterate over all drugs - children of drugbank
    count = 0
    for drugtag in tree.getroot():
        ids = drugtag.findall('drugbank:drugbank-id', ns)
        primary = drugtag.find("drugbank:drugbank-id[@primary='true']", ns).text

        atc_codes = []
        atccodes = drugtag.find('drugbank:atc-codes', ns)
        for atccode in atccodes:
            #mm = atccode.find('drugbank:atc-code', ns)
            atc_code = atccode.attrib["code"]
            if atc_code!=None:
                atc_codes.append(atc_code)
        drugs[primary] = atc_codes
    return drugs