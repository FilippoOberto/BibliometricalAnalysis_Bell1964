# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:01:17 2020

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

#funzione Counter = conta numero occorrenze#
def plot_counter(c, n=30, title='plot', fname='plot.png'):
    c = c.most_common(n)
    plt.title(title)
    plt.bar(np.arange(n), [i[1] for i in c], tick_label = [i[0][0:25] for i in c])
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig(fname, dpi=300)
    plt.close()

#funzione per stampare i grafici delle citazioni anno per anno e citazioni cumulative#
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

#funzione per selezionare gli anni
def df_yspan(df, ymin, ymax):
    return df.query('PY >= {} and PY < {}'.format(ymin, ymax))

#----------------------------------------------------------------------------------#
#-----------------------------------SCRIPT-----------------------------------------#
#----------------------------------------------------------------------------------#


#1964-1985#

df = pd.read_csv('bell_pre85.csv', sep=';', index_col=0)
df.head()

#years

pys = list(df['PY'])

plot_cit_by_year(pys, False, 'Citazioni per anno a Bell (1964) - pre85', 'cit_per_year_pre85.png')
plot_cit_by_year(pys, True, 'Citazioni cumulative a Bell (1964) - pre85', 'cit_cumul_pre85.png')

#autori

for y in range (1964, 1975, 10):
    df_y = df_yspan(df, y, y+10)

    aus = [str(i).lower() for au in ['au1', 'au2', 'au3', 'au4', 'au5'] for i in list(df_y[au])]

    au = Counter([str(i).lower() for i in aus if str(i) != "nan"])

    plot_counter(au, 10, 'Autori più frequenti {} - {}'.format(y, y+10), 'au{}_{}.png'.format(y, y+10))

#sources

for y in range (1964, 1975, 10):
    df_y = df_yspan(df, y, y+10)

    so = Counter([str(i).lower() for i in list(df['so']) if str(i) != 'nan'])

    plot_counter(so, 10, 'Fonti più frequenti {} - {}'.format(y, y+10), 'so{}_{}.png'.format(y, y+10))

#Grafico Sources
df_t = df.pivot_table(index=['PY'], columns='so', aggfunc='size', fill_value=0).cumsum(axis=0)

df_t = df_t[df_t.columns[df_t.iloc[-1]>10]]

sns.lineplot(data=df_t, dashes=False)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.savefig('Sources.png', dpi=300, bbox_inches='tight')

#abstract, parole più frequenti

for y in range (1964, 1975, 10):
    df_y = df_yspan(df, y, y+10)

    tokenizer = nltk.RegexpTokenizer(r"\w+")

    ignore = set(stopwords.words('english'))

    abst = [tokenizer.tokenize(i.lower()) for i in list(df_y['Abstract'].dropna())]

    tot = [item for sublist in abst for item in sublist]
    tot = Counter(x for x in tot if x not in ignore)

    plot_counter(tot, 50, 'Parole più frequenti negli abstracts {} - {}'.format(y, y+10), 'abst{}_{}.png'.format(y, y+10))

#titoli, parole più frequenti

for y in range (1964, 1975, 10):
    df_y = df_yspan(df, y, y+10)

    tokenizer = nltk.RegexpTokenizer(r"\w+")

    ignore = set(stopwords.words('english'))

    abst = [tokenizer.tokenize(i.lower()) for i in list(df_y['ti'])]

    tot = [item for sublist in abst for item in sublist]
    tot = Counter(x for x in tot if x not in ignore)

    plot_counter(tot, 50, 'Parole più frequenti nei titoli {} - {}'.format(y, y+10), 'ti{}_{}.png'.format(y, y+10))

#1985-2020#

df = pd.read_csv('bell_post85.csv').groupby('ID').first()
df.head()

#years

pys_post = list(df['PY'])

plot_cit_by_year(pys_post, False, 'Citazioni per anno a Bell(1964) - post85', 'cit_per_year_post85.png')
plot_cit_by_year(pys_post, True, 'Citazioni cumulative a Bell(1964) - post85', 'cit_cumul_post85.png')

pys_tot = pys + pys_post

plot_cit_by_year(pys_tot, False, 'Citazioni per anno a Bell(1964) - tot', 'cit_per_year_tot.png')
plot_cit_by_year(pys_tot, True, 'Citazioni cumulative a Bell(1964) - tot', 'cit_cumul_tot.png')

#Autori

for y in range (1985, 2011, 10):
    df_y = df_yspan(df, y, y+10)

    aus = [str(i).lower().split(';') for i in list(df_y['AU'])]

    au = Counter([item for sublist in aus for item in sublist])

    plot_counter(au, 10, 'Autori più frequenti {} - {}'.format(y, y+10), 'au{}_{}.png'.format(y, y+10))

aus = [str(i).lower().split(';') for i in list(df.query('PY >= 2015 and PY <= 2020')['AU'])]

au = Counter([item for sublist in aus for item in sublist])

plot_counter(au, 10, 'Autori più frequenti 2015 - 2020', 'au2015_2020.png')

#Sources

for y in range (1985, 2011, 10):
    df_y = df_yspan(df, y, y+10)

    so = Counter([str(i).lower() for i in list(df['SO'])if str(i) != 'nan'])

    plot_counter(so, 10, 'Fonti più frequenti {} - {}'.format(y, y+10), 'so{}_{}.png'.format(y, y+10))
    
so = Counter([str(i).lower() for i in list(df.query('PY >= 2015 and PY <= 2020')['SO'])])

plot_counter(so, 10, 'Fonti più frequenti 2015 - 2020', 'so2015_2020.png')

#Grafico Sources

df_t = df.pivot_table(index=['PY'], columns='SO', aggfunc='size', fill_value=0).cumsum(axis=0)

df_t = df_t[df_t.columns[df_t.iloc[-1]>100]]

sns.lineplot(data=df_t, dashes=False)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.savefig('Sources_post85.png', dpi=300, bbox_inches='tight')

#abstract, parole più frequenti

for y in range (1985, 2011, 10):
    df_y = df_yspan(df, y, y+10)

    tokenizer = nltk.RegexpTokenizer(r"\w+")

    ignore = set(stopwords.words('english'))

    abst = [tokenizer.tokenize(i.lower()) for i in list(df_y['AB'].dropna())]

    tot = [item for sublist in abst for item in sublist]
    tot = Counter(x for x in tot if x not in ignore)

    plot_counter(tot, 50, 'Parole più frequenti negli abstracts {} - {}'.format(y, y+10), 'abst{}_{}.png'.format(y, y+10))

tokenizer = nltk.RegexpTokenizer(r"\w+")

ignore = set(stopwords.words('english'))

abst = [tokenizer.tokenize(i.lower()) for i in list(df.query('PY >= 2015 and PY <= 2020')['AB'].dropna())]

tot = [item for sublist in abst for item in sublist]
tot = Counter(x for x in tot if x not in ignore)

plot_counter(tot, 50, 'Parole più frequenti negli abstract 2015 - 2020', 'abst2015_2020.png')

#titoli, parole più frequenti

for y in range (1985, 2011, 10):
    df_y = df_yspan(df, y, y+10)

    tokenizer = nltk.RegexpTokenizer(r"\w+")

    ignore = set(stopwords.words('english'))

    abst = [tokenizer.tokenize(i.lower()) for i in list(df_y['TI'].dropna())]

    tot = [item for sublist in abst for item in sublist]
    tot = Counter(x for x in tot if x not in ignore)

    plot_counter(tot, 50, 'Parole più frequenti nei titoli {} - {}'.format(y, y+10), 'ti{}_{}.png'.format(y, y+10))

tokenizer = nltk.RegexpTokenizer(r"\w+")

ignore = set(stopwords.words('english'))

abst = [tokenizer.tokenize(i.lower()) for i in list(df.query('PY >= 2015 and PY <= 2020')['TI'].dropna())]

tot = [item for sublist in abst for item in sublist]
tot = Counter(x for x in tot if x not in ignore)

plot_counter(tot, 50, 'Parole più frequenti nei titoli 2015 - 2020', 'ti2015_2020.png')

#Affiliazioni

for y in range (1985, 2011, 10):
    df_y = df_yspan(df, y, y+10)

    af = [str(i).lower().replace('[','').replace(']','').split(';') for i in list(df['C1'].dropna())]

    afs = []

    for i in af:
        for j,x in enumerate(i):
            if j%2 != 0:
                afs.append(x.strip()) #.split(',')[0] #(Per lo switch università-Dipartimenti, attivare il commento)

    af_c = Counter(afs)

    plot_counter(af_c, 10, 'Affiliazioni più frequenti {} - {}'.format(y, y+10), 'af{}_{}.png'.format(y, y+10))