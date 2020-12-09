# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 12:54:17 2020

@author: fiippooberto
"""

import pandas as pd
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import stopwords
import seaborn as sns

sns.set_style("whitegrid")

def plot_counter(c, n=10, title='plot', fname='plot.png'):
    c = c.most_common(n)
    plt.title(title)
    plt.bar(np.arange(n), [i[1] for i in c], tick_label = [i[0][0:25] for i in c])
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig(fname, dpi=300)
    plt.close()

def plot_cit_by_year(pys, cumul=False, title='cit_by_year', fname='cit_by_year.png', vl=[]):

    yspan = np.arange(min(pys), max(pys)+1)

    pys_c = Counter(pys)

    for i in yspan:
        if i not in pys_c:
            pys_c[i] = 0

    if cumul:
        for i in yspan:
            pys_c[i] += pys_c.get(i-1, 0)

    pys_c = OrderedDict(sorted(pys_c.items()))

    plt.title(title)
    plt.plot(list(pys_c.keys()), np.array(list(pys_c.values())), linewidth=2)
    for i in vl:
        plt.plot([i, i], [max(list(pys_c.values())), min(list(pys_c.values()))], linestyle='dashed', color='red')
    plt.xticks(list(pys_c.keys()), rotation=-90, fontsize='x-small')
    plt.tight_layout()
    plt.savefig(fname, dpi=300)
    plt.close()

    return pys_c

# -------------- #
# --- PRE 85 --- #
# -------------- #

df = pd.read_csv('bell_pre85.csv', sep=';', index_col=0)

# -------------------------------------------------------------------------------------- #
# years

pys = list(df['py'])

plot_cit_by_year(pys, False, 'Citazioni per anno a Bell (1964) - pre 85', 'cit_per_year_pre85.png')
plot_cit_by_year(pys, True, 'Citazioni cumulative a Bell (1964) - pre 85', 'cit_cumul_pre85.png')

# -------------------------------------------------------------------------------------- #
# sources

so = Counter([str(i).lower() for i in list(df['so'])])

del so['nan']

plot_counter(so, 30, 'Fonti più frequenti', 'so.png')

# -------------------------------------------------------------------------------------- #
# authors

aus = [str(i).lower() for au in ['au1','au2','au3','au4','au5'] for i in list(df[au])]

au = Counter([str(i).lower() for i in aus])

del au['nan']

plot_counter(au, 30, 'Autori più frequenti', 'au.png')

# -------------------------------------------------------------------------------------- #
# abstracts

tokenizer = nltk.RegexpTokenizer(r"\w+")

ignore = set(stopwords.words('english'))

abst = [tokenizer.tokenize(i.lower()) for i in list(df['Abstract'])]

tot = [item for sublist in abst for item in sublist]
tot = Counter(x for x in tot if x not in ignore)

plot_counter(tot, 50, 'Parole più frequenti negli abstracts', 'abst.png')

# -------------------------------------------------------------------------------------- #
# titles

tokenizer = nltk.RegexpTokenizer(r"\w+")

ignore = set(stopwords.words('english'))

tit = [tokenizer.tokenize(i.lower()) for i in list(df['ti'])]

tot = [item for sublist in tit for item in sublist]
tot = Counter(x for x in tot if x not in ignore)

plot_counter(tot, 30, 'Parole più freqenti nei titoli', 'ti.png')

# --------------- #
# --- POST 85 --- #
# --------------- #

df = pd.read_csv('bell_post85.csv').groupby('ID').first()

# -------------------------------------------------------------------------------------- #
# years

pys_post = list(df['PY'])

plot_cit_by_year(pys_post, False, 'Citazioni per anno a Bell (1964) - post 85', 'cit_per_year_post85.png')
plot_cit_by_year(pys_post, True, 'Citazioni cumulative a Bell (1964) - post 85', 'cit_cumul_post85.png')

pys_tot = pys + pys_post

plot_cit_by_year(pys_tot, False, 'Citazioni per anno a Bell (1964) - tot', 'cit_per_year_tot.png', [1984.5])
plot_cit_by_year(pys_tot, True, 'Citazioni cumulative a Bell (1964) - tot', 'cit_cumul_tot.png', [1984.5])

# -------------------------------------------------------------------------------------- #
# sources

so = Counter([str(i).lower() for i in list(df['SO'])])

del so['nan']

plot_counter(so, 30, 'Fonti più frequenti - post 85', 'so_post85.png')

# --------------------------------------------------------------------------------------- #

aus = [str(i).lower().split(';') for i in list(df['AU'])]

au = Counter([item for sublist in aus for item in sublist])

plot_counter(au, 30, 'Autori più frequenti - post 85', 'au_post85.png')

# --------------------------------------------------------------------------------------- #

af = [str(i).lower().replace('[','').replace(']','').split(';') for i in list(df['C1'].dropna())]

afs = []

for i in af:
    for j,x in enumerate(i):
        if j%2 != 0:
            afs.append(x.strip()) #.split(',')[0]

af_c = Counter(afs)

plot_counter(af_c, 30, 'Affiliazioni più frequenti - post 85', 'af_post85.png')

# --------------------------------------------------------------------------------------- #

# abstracts

#tokenizer = nltk.RegexpTokenizer(r"\w+")

#ignore = set(stopwords.words('english'))

#abst = [tokenizer.tokenize(i.lower()) for i in list(df['Abstract'])]

#tot = [item for sublist in abst for item in sublist]
#tot = Counter(x for x in tot if x not in ignore)

#plot_counter(tot, 50, 'Parole più frequenti negli abstracts', 'abst.png')
