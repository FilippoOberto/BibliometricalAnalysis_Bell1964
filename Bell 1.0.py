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

tokenizer = nltk.RegexpTokenizer(r"\w+")
ignore = set(stopwords.words('english))

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

#Funzione per Processare dati
def process_data(df, col_names, start, end, step, title_prefix, n=50):
    for y in range(start, end, step):
        df_y = df_yspan(df, y, y+step)
        for col in col_names:
            col_values = [str(i).lower() for i in list(df_y[col])]
            counter = Counter([x for x in col_values if x != 'nan'])
            plot_counter(counter, n, f'{title_prefix} più frequenti {y} - {y+step}', f'{col}_{y}_{y+step}.png')

#----------------------------------------------------------------------------------#
#-----------------------------------SCRIPT-----------------------------------------#
#----------------------------------------------------------------------------------#

#Lettura di CSV
df1 = pd.read_csv('bell_pre85.csv', sep=';', index_col=0)
df2 = pd.read_csv('bell_post85.csv').groupby('ID').first()

#Concatenazione dei dataframe
df1['Source] = 'pre85'
df2['Source] = 'post85'
df = pd.concat([df1, df2])

#Elaborazione per 'pre85'
process_data(df_pre85, ['au1', 'au2', 'au3', 'au4', 'au5'], 1964, 1975, 10, 'Autori')

process_data(df_pre85, ['so'], 1964, 1975, 10, 'Fonti')

process_data(df_pre85, ['Abstract', 'ti'], 1964, 1975, 10, 'Parole', n=50)

#pys = list(df['py'])
#plot_cit_by_year(pys, False, 'Citazioni per anno a Bell (1964) - pre 85', 'cit_per_year_pre85.png')
#plot_cit_by_year(pys, True, 'Citazioni cumulative a Bell (1964) - pre 85', 'cit_cumul_pre85.png')

# Elaborazione per 'post85'
df_post85 = df[df['Source'] == 'post85']

process_data(df_post85, ['AU'], 1985, 2011, 10, 'Autori')

process_data(df_post85, ['SO'], 1985, 2011, 10, 'Fonti')

process_data(df_post85, ['AB', 'TI'], 1985, 2011, 10, 'Parole', n=50)

pys_post = list(df['PY'])
plot_cit_by_year(pys_post, False, 'Citazioni per anno a Bell (1964) - post 85', 'cit_per_year_post85.png')
plot_cit_by_year(pys_post, True, 'Citazioni cumulative a Bell (1964) - post 85', 'cit_cumul_post85.png')
#pys_tot = pys + pys_post
#plot_cit_by_year(pys_tot, False, 'Citazioni per anno a Bell (1964) - tot', 'cit_per_year_tot.png', [1984.5])
#plot_cit_by_year(pys_tot, True, 'Citazioni cumulative a Bell (1964) - tot', 'cit_cumul_tot.png', [1984.5])
