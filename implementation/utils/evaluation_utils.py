# !/usr/bin/env python3
import scipy

def compute_similarity_between_pairs(drugids, sim_matrix, list_of_pairs):
    n = len(list_of_pairs)
    total_list = list()
    
    for i in range(0, n):
        aux_list = list()
        
        pair = list_of_pairs[i]
        drug1 = pair[0]
        drug2 = pair[1]
        pair_id = pair[3]
        
        if drug1 in drugids and drug2 in drugids:
            index1 = drugids.index(drug1)
            index2 = drugids.index(drug2)
        
            similarity = sim_matrix[index1, index2]
        else:
            similarity = -1
        
        aux_list.append(drug1)
        aux_list.append(drug2)
        aux_list.append(similarity)
        aux_list.append(pair_id)
        
        total_list.append(aux_list)
        
    return total_list

def ground_truth_evaluation_order(computed_sim, ground_truth_sim):
    n = len(computed_sim)
    x = list()
    y = list()
    
    for i in range(0, n):
        if not computed_sim[i][2] == -1:
            x.append(computed_sim[i][3])
            y.append(ground_truth_sim[i][3])
    
    return scipy.stats.pearsonr(x, y)

def ground_truth_evaluation_value(computed_sim, ground_truth_sim):
    n = len(computed_sim)
    x = list()
    y = list()
    
    for i in range(0, n):
        if not computed_sim[i][2] == -1:
            x.append(computed_sim[i][2])
            y.append(float(ground_truth_sim[i][2]))
    
    return scipy.stats.pearsonr(x, y)