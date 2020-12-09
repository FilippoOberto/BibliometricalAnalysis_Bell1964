#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:28:44 2020

@author: filippooberto
"""
import matplotlib.pyplot as plt
import numpy as np
import json

#----------------------------------------------------------------------------#
#----------------------------- Funzioni -------------------------------------#
#----------------------------------------------------------------------------#

def groups_unpack(data, l=0):
    l = str(l)
    m = np.array(data[l]['p_tw_d']) #topic-document
    c = np.array(data[l]['p_td_d']) #cluster-document
    
    docs = dict()
    for i in range(m.shape[1]):
        if type(docs.get(i)) != dict:
            docs[i] = dict()
        docs[i]['topic_sorted'] = np.argsort(m[:,i])[::-1]
        docs[i]['topic_sorted_probs'] = np.sort(m[:,i])[::-1]
        docs[i]['cluster'] = np.argsort(c[:,i])[::-1][0]
    
    a = np.zeros((c.shape[0],m.shape[0])) #cluster-topic
    
    for i in range(m.shape[1]):
        a[docs[i]['cluster']] += m[:,i]
    
    clusters = dict()
    for i in range(a.shape[0]):
        a[i] = a[i] / a.sum(axis=1)[i]
        if type(clusters.get(i)) != dict:
            clusters[i] = dict()
        clusters[i]['topic_sorted'] = np.argsort(a[i])[::-1]
        clusters[i]['topic_sorted_probs'] = np.sort(a[i])[::-1]
    
    return (docs, clusters, m, c, a)

def plot_topics(data, l=0, savefile=True):
    l=str(l)
    for i in t_data[l]:
        t_w = [j[0] for j in t_data[l][i]]
        t_p = [j[1] for j in t_data[l][i]]
        plt.title("Topic {}, L={}".format(i, l))
        x = np.arange(len(t_w))
        plt.barh(x, t_p)
        plt.yticks(x, t_w)
        if savefile:
            plt.savefig('l{}t{}_w_distro.png'.format(l,i))
        else:
            plt.show()
        plt.close()
        
def plot_matrix(matrix, fname=None, cmap=plt.cm.Reds, dec=2, xt=None, yt=None):
    plt.figure(figsize = matrix.shape)
    plt.imshow(matrix, cmap=cmap)
    for i in np.arange(matrix.shape[1]):
        for j in np.arange(matrix.shape[0]):
            c = matrix[j,i]
            plt.text(i, j, str(np.around(c,dec)), va='center', ha='center')
    
    if xt:
        plt.xticks(xt)
    else:
        plt.xticks(np.arange(matrix.shape[1]))
    if yt:
        plt.yticks(yt)
    else:
        plt.yticks(np.arange(matrix.shape[0]))
    plt.tight_layout()
    if fname:
        plt.savefig(fname, dpi=600)
    else:
        plt.show()
    plt.close()
        
#----------------------------------------------------------------------------#
#------------------------------ Script --------------------------------------#
#----------------------------------------------------------------------------#
        
with open('pre85_groups.json') as json_file:
    g_data = json.load(json_file)
    
d, c, t_d, c_d, c_t = groups_unpack(g_data, 0)
#d: dictionary of documents
#c: dictionary of clusters
#t_d: topic-to-document matrix
#c_d: cluster-to-docuement matrix
#c_t: cluster-to-topic matrix
fname= 'cluster_to_topic_matrix'
plt.title("cluster-to-topic matrix L=0")
plt.imshow(c_t)
plt.savefig(fname, dpi=600)
plt.close()

with open('pre85_topics.json') as json_file:
    t_data = json.load(json_file)
    
plot_topics(t_data, 0)

plot_matrix(c_t, fname="c_t_Matrice")