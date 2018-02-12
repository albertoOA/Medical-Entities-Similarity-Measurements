# !/usr/bin/env python3
import numpy 
import zipfile

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

def distance_to_similarity_matrix(matrix):
    n, m = matrix.shape
    max_val = numpy.max(matrix)
    min_val = numpy.min(matrix)
    sim_matrix = numpy.ones((n, m))
    for i in range(0, n):
        for j in range(0, m):
            sim_matrix[i,j] -= matrix[i,j] 
            
    return sim_matrix