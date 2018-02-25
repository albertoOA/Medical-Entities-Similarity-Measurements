# !/usr/bin/env python3
import networkx as nx
import numpy
from math import log
import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(HERE, ".."))

from classes.Classification import Classification


def build_classification_graph_from_list(drugs):
    graph = nx.Graph()
    for drug in drugs:
        cls = drug.classification
        if cls != None:
            graph.add_node(cls.kingdom)
            graph.add_node(cls.superclass)
            graph.add_edge(cls.kingdom, cls.superclass)

            graph.add_node(cls.class_type)
            graph.add_edge(cls.superclass, cls.class_type)

            graph.add_node(cls.subclass)
            graph.add_edge(cls.class_type, cls.subclass)

            if (cls.direct_parent!=cls.subclass):
                graph.add_node(cls.direct_parent)
                graph.add_edge(cls.subclass, cls.direct_parent)

            graph.add_node(drug.primary_id)
            graph.add_edge(cls.direct_parent, drug.primary_id)
    return graph

def calculate_dist_matrix(graph, drugids):
    n = len(drugids)
    graph_distance = numpy.zeros(shape=(n,n))

    sortedids = sorted(drugids)
    dict_sortedids = dict(enumerate(sortedids))
    for i in range(n):
        for j in range(i+1,n):
            try:
                shortest_path = nx.shortest_path_length(graph, dict_sortedids[i], dict_sortedids[j])
            except nx.NetworkXNoPath:
                shortest_path = -1
            except nx.NetworkXError:
                shortest_path = -1
            graph_distance[i,j] = shortest_path
            graph_distance[j,i] = shortest_path
        # print(i)
    return graph_distance

def build_classification_weighted_graph_from_list(drugs, weights=[1,10,20,25,50]):
    graph = nx.Graph()
    for drug in drugs:
        cls = drug.classification
        if cls != None:
            graph.add_node(cls.kingdom)
            graph.add_node(cls.superclass)
            graph.add_edge(cls.kingdom, cls.superclass, weight=weights[4])

            graph.add_node(cls.class_type)
            graph.add_edge(cls.superclass, cls.class_type,weight=weights[3])

            graph.add_node(cls.subclass)
            graph.add_edge(cls.class_type, cls.subclass,weight=weights[2])

            if (cls.direct_parent!=cls.subclass):
                graph.add_node(cls.direct_parent)
                graph.add_edge(cls.subclass, cls.direct_parent,weight=weights[1])

            graph.add_node(drug.primary_id)
            graph.add_edge(cls.direct_parent, drug.primary_id, weight=weights[0])
    return graph

def calculate_weighted_dist_matrix(graph, drugids):
    n = len(drugids)
    graph_distance = numpy.zeros(shape=(n,n))

    sortedids = sorted(drugids)
    dict_sortedids = dict(enumerate(sortedids))
    for i in range(n):
        for j in range(i+1,n):
            try:
                shortest_path = nx.dijkstra_path_length(graph, dict_sortedids[i], dict_sortedids[j])
            except nx.NetworkXNoPath:
                shortest_path = -1
            except nx.NetworkXError:
                shortest_path = -1
            graph_distance[i,j] = shortest_path
            graph_distance[j,i] = shortest_path
        # print(i)
    return graph_distance

def leakcock_chodorow_measure(matrix):
    for x in numpy.nditer(matrix, op_flags=['readwrite']):
        if(x==0):
            x[...] = 1
        elif(x==-1):
            x[...] = 0
        else:
            val = -log(x/10)
            if numpy.isnan(val):
                print(x)
            x[...] = val
    return matrix

def build_ATC_graph_from_list(drugs):
    graph = nx.Graph()
    for drug in drugs:
        codes = drug.atc_codes
        if codes != []:
            for code in codes:
                first = code[0:1]
                second = code[0:3]
                third = code[0:4]
                fourth =code[0:5]
                fifth = code

                graph.add_node(fifth)
                graph.add_node(fourth)
                graph.add_edge(fifth, fourth)

                graph.add_node(third)
                graph.add_edge(fourth, fifth)

                graph.add_node(second)
                graph.add_edge(third, second)

                graph.add_node(first)
                graph.add_edge(second, first)

                graph.add_node(drug.primary_id)
                graph.add_edge(first, drug.primary_id)
    return graph

def build_ATC_weighted_graph_from_list(drugs, weights=[1,10,20,25,50]):
    graph = nx.Graph()
    for drug in drugs:
        codes = drug.atc_codes
        if codes != []:
            for code in codes:
                first = code[0:1]
                second = code[0:3]
                third = code[0:4]
                fourth =code[0:5]
                fifth = code

                graph.add_node(fifth)
                graph.add_node(fourth)
                graph.add_edge(fifth, fourth, weight=weights[4])

                graph.add_node(third)
                graph.add_edge(fourth, fifth, weight=weights[3])

                graph.add_node(second)
                graph.add_edge(third, second, weight=weights[2])

                graph.add_node(first)
                graph.add_edge(second, first, weight=weights[1])

                graph.add_node(drug.primary_id)
                graph.add_edge(first, drug.primary_id,  weight=weights[0])
    return graph
