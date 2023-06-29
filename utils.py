import json
import networkx as nx
import xgi
import numpy as np
from itertools import combinations
from matplotlib import pyplot as plt
import pandas as pd
from scipy.stats import ks_2samp

def ks_sample_test(
        sample1:np.ndarray, 
        sample2:np.ndarray):
    return ks_2samp(
        sample1, 
        sample2).pvalue

def format_data(dict_cursor:list) -> list:
    interactions_list = []
    users_list = []
    for i in dict_cursor:
        users_list.append(i['USER_ID'])
        if i['REPLY_USERS'] != None:
            replies = json.loads(i['REPLY_USERS'])
            replies.append(i['USER_ID'])
            for j in replies:
                users_list.append(j)
            comb = list(set([tuple(sorted(i))
                                for i in 
                                combinations(replies,2)]))
            interactions_list += comb
    return interactions_list, list(set(users_list))

def build_network(data:list, roles:list, general:bool = False) -> nx.Graph:
    interactions_list, users_list = format_data(data)
    interactions_list = [i +  (len(list(filter(lambda interaction: interaction == i, interactions_list))),) for i in interactions_list]
    G = nx.Graph()
    G.add_nodes_from(users_list)
    G.add_weighted_edges_from(list(set(interactions_list)))
    attrs = {i['USER_ID']:{"POSITION": i['POSITION'], "ROLE": i['ROLE'], "JOB_CATEGORY": i['JOB_CATEGORY']}  for i in roles}
    nx.set_node_attributes(G, attrs)
    return G

def build_hypergraph(data:list, roles:list) -> xgi.Hypergraph:
    interactions = []
    attributes = []
    for row in data:
        interactions.append(list(set(json.loads(row['MEMBERS'].replace("\n ", "")))))
    for row in roles:
        attributes.append(
            (
                row['USER_ID'], {
                    'role': row['ROLE'],
                    'position': row['POSITION'],
                    'job_category': row['JOB_CATEGORY']
            })
        )
    H = xgi.Hypergraph(interactions)
    H.add_nodes_from(attributes)
    return H

def build_bipartate_network(data: list) -> nx.Graph:
    nodes = []
    channels = []
    edges = []

    for index, element in enumerate(data):
        if element['CHANNEL_ID']:
            users = list(set(json.loads(element['MEMBERS'].replace("\n ", ""))))
            nodes += users
            channels.append(element['CHANNEL_ID'])
            comb = [(element['CHANNEL_ID'], user) for user in users]
            edges += comb
        else:
            continue
    G = nx.Graph()
    G.add_nodes_from(list(set(channels)), bipartite=0)
    G.add_nodes_from(list(set(nodes)), bipartite=1)
    G.add_edges_from(list(set(edges)))
    return G

def centrality(G:nx.Graph, eigen_vector:bool = True) -> dict:
    if eigen_vector:
        centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06, nstart=None, weight=None) 
    else:
        centrality = nx.pagerank(G, alpha=0.85)
    return centrality

def normalise(mean:float, 
              var:float, 
              value: float) -> float:
    return (value - mean)/var

def significance(n1:int, 
                 n2:int, 
                 s1:float, 
                 s2:float, 
                 m1:float, 
                 m2:float, 
                 limit = 1.28) -> float:
    SE = np.sqrt((s1/n1) + (s2/n2))
    diff = m1 - m2 - 0
    Z = diff/SE

    if abs(Z) > limit:
        print('The difference is significant')
    else:
        print('The difference is NOT significant')
    return Z

def build_general_G(dict_cursor:list, roles:list , general:bool = False) -> nx.Graph:
    net_dir = lambda x: 'networks/general' if general else 'networks/product'
    nodes = []
    edges = []

    for index, element in enumerate(dict_cursor):
        users = list(set(json.loads(element['MEMBERS'].replace("\n ", ""))))
        nodes += users
        wheigt = np.round(1/np.log(len(users)),2)
        comb = [tuple(sorted(i)) for i in combinations(users,2)]
        edges += [i + (wheigt,1) for i in comb]

    nodes = list(set(nodes))
    edges = list(pd.DataFrame(edges).groupby([0,1]).agg({2:'sum', 3:'sum'}).reset_index().itertuples(index = False, name = None))
    edges = [(i[0], i[1], round(i[2]/i[3], 2)) for i in edges]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)
    attrs = {i['USER_ID']:{"POSITION": i['POSITION'], "ROLE": i['ROLE'], "JOB_CATEGORY": i['JOB_CATEGORY']}  for i in roles}
    nx.set_node_attributes(G, attrs)
    return G