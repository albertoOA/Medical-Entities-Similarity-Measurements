# !/usr/bin/env python3
import numpy 
import zipfile
import pickle
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def read_zip_file(filepath, filename):
    zfile = zipfile.ZipFile(filepath)
    ifile = zfile.open(filename)
    
    return ifile

def normalize_matrix(matrix):
    n, m = matrix.shape
    max_val = numpy.max(matrix)
    min_val = numpy.min(matrix)
    norm_matrix = numpy.zeros((n, m))
    for i in range(0, n):
        for j in range(0, m):
            norm_matrix[i,j] = (matrix[i,j] - min_val)/(max_val - min_val)
            
    return norm_matrix

def bidirectional_conversion_between_distance_and_similarity_matrix(matrix):
    n, m = matrix.shape
    max_val = numpy.max(matrix)
    min_val = numpy.min(matrix)
    sim_matrix = numpy.ones((n, m))
    for i in range(0, n):
        for j in range(0, m):
            sim_matrix[i,j] -= matrix[i,j] 
            
    return sim_matrix

def label_idx(labels, nclust):
    ret = dict()
    for c in range(nclust):
        l = []
        for i in range(len(labels)):
            if labels[i] == c:
                l.append(i)
        ret[c] = l
    return ret

def idx_to_id(idx, ids_dict):
    ret = []
    for i in idx:
        ret.append(ids_dict[i])
    return ret

def intersection_index(list_a, list_b):
    """
    Returns two lists containing the index of the elements in list_a found in list_b
    and the index of elements of list_b contained in list_a

    :param : two lists
    :rtype : object
    """
    int_index_ab = []
    int_index_ba = []
    for i in range(0, len(list_a)):
        j = 0
        found = False
        while j < len(list_b) and not found:
            if list_a[i] == list_b[j]:
                found = True
                int_index_ab.append(i)
                int_index_ba.append(j)
            j += 1
    return int_index_ab, int_index_ba

def save_obj(obj, path, filename):
    with open(path + filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path, filename):
    with open(path + filename + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_similarity_matrix(sim, path, filename):
    maxsim = 1

    fig = plt.figure()
    plt.tick_params(
        axis='both',
        labelleft='off',
        labelbottom='off')
    plt.imshow(sim, interpolation='nearest', vmin=0, vmax=maxsim)
    plt.colorbar().set_label('Similarity')
    plt.title(filename)
    plt.savefig(path+filename+'.png')

def save_similarity_matrix_ordered(sim, clusters_idx_ordered, path, filename):
    maxsim = 1

    fig = plt.figure()
    plt.tick_params(
        axis='both',
        labelleft='off',
        labelbottom='off')
    plt.imshow(sim[:, clusters_idx_ordered][clusters_idx_ordered],
           interpolation='nearest', vmin=0, vmax=maxsim)
    plt.colorbar().set_label('Similarity')
    plt.title(filename)
    plt.savefig(path+filename+'.png')