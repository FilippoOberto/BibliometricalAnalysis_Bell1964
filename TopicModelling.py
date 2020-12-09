#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:16:23 2020

@author: filippooberto
"""
import pandas as pd
import nltk
from nltk.corpus import stopwords
import graph_tool.all as gt
#import json
import numpy as np
#import sys

from sbmtm import sbmtm

def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type', type(obj))
    
#-----------------Setup Load a Corpus--------------------------------------#

path_data = ''

df = pd.read_csv('bell_pre85.csv', sep=';', index_col=0).dropna(subset=['Abstract'])

# Carico Lista Abstract

tokenizer = nltk.RegexpTokenizer(r"\w+")

ignore = set(stopwords.words('english'))

texts = [[j for j in tokenizer.tokenize(i.lower()) if j not in ignore] for i in list(df['Abstract'])]

titles = list(df['ti'])

#Controllo

i_doc = 0

print(titles[0])
print(texts[i_doc][:10])

#-----------------Fitting the Model--------------------------------------#

model = sbmtm()

model.make_graph(texts, documents=titles) #this line create the word-document network from corpus

gt.seed_rng(32) #seed for graph-tool's random number generator. Set the seed to get same result and replicate
model.fit(n_init=10) #n_init: iteration

#-----------------Plotting the Result--------------------------------------#

plot_tuple = model.plot(filename='tmpg.png', nedges=1000)

#-----------------Topic-Order on Visualization------------------------------#
pos_vertex_property_map_from_plot = plot_tuple[0]
level = 0
lo = model.getTopicOrderingForLevel(level,pos_vertex_property_map_from_plot)

print(lo)
#-----------------Plotting Clusters' Info as Json--------------------------------------#

"""prefix = 'model_output/pre85_'

orig_stdout = sys.stdout
f = open(path_data+prefix+'summary.txt', 'w')
sys.stdout = f
model.state.print_summary()
sys.stdout = orig_stdout
f.close()

with open(path_data+prefix+'summary.txt', 'a') as f:
    summary = '\n #word-nodes: {} \n #doc-nodes: {} \n #edges: {} \n mdl: {} \n'.format(model.get_V(), model.get_D(), model.get_N(), model.mdl)
    f.write(summary)

g = dict()
for i in range(1+model.L):
    g[i] = model.get_groups(l=i)

with open(path_data+prefix+'groups.json', 'w') as f:
    f.write(json.dumps(g, default=default, indent=4))
    
topics = dict()
for i in range(1+model.L):
    topics[i] = model.topics(l=i, n=10)

with open(path_data+prefix+'topics.json', 'w') as f:
    f.write(json.dumps(topics, default=default, indent=4))
    
clusters = dict()
for i in range(1+model.L):
    cl = dict()
    C = model.clusters(l=i, n=1)
    for c in C:
        cl[c] = model.clusters_query(c, l=i)
    clusters[i] = cl

with open(path_data+prefix+'clusters.json', 'w') as f:
    f.write(json.dumps(clusters, default=default, indent=4))
    
mix = dict()
pmi = dict()
for i in range(1+model.L):
    model.groups = [model.get_groups(l=i)]
    mix[i] = model.group_to_group_mixture(l=i)
    pmi[i] = model.pmi_td_tw(l=i)

with open(path_data+prefix+'group_mixture.json', 'w') as f:
    f.write(json.dumps(mix, default=default, indent=4))

with open(path_data+prefix+'pmi.json', 'w') as f:
    f.write(json.dumps(pmi, default=default, indent=4))

docs = dict()
for i in range(len(model.documents)):
    docs[i] = {'name' : model.documents[i]}
    for l in range(1+model.L):
        docs[i]['topics'] = model.topicdist(i, l=l)
        
with open(path_data+prefix+'documents.json', 'w') as f:
    f.write(json.dumps(docs, default=default, indent=4))"""
    