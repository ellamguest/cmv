#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:23:59 2017

@author: emg
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from prawini import *

params = get_params()
headers={'User-agent':params['user_agent']}

#for cmv
df = pd.read_csv('/Users/emg/Programming/GitHub/cmv/raw_data/current-mod-table.csv',
                 index_col=0)


#for TD
df = pd.read_csv('/Users/emg/Programming/GitHub/the_donald_project/raw_data/current-mod-table.csv',
                 index_col=0)

names = list((df[df['name']!='AutoModerator']['name']))
names.remove('AutoModerator')

def make_soup(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    return soup

d = {}
for name in names:
    print name
    url = 'https://www.reddit.com/user/{}'.format(name)
    soup = make_soup(url)
    try:
        table = soup.find('ul', {'id':'side-mod-list'})
        items = table.find_all('li')
        subs = []
        for item in items:
            subs.append(item.a['title'])
        d[name] = subs
    except:
        pass
    

values = list(set([x for y in d.values() for x in y]))
data = {}
for key in d.keys():
    data[key] = [True if value in d[key] else False for value in values ]

mod_subs = pd.DataFrame(data, index=values)
mod_subs = mod_subs.applymap(lambda x: 1 if x else 0)
counts = mod_subs.T.sum()

mod_subs.to_csv('/Users/emg/Programming/GitHub/the_donald_project/raw_data/current-sub-mod-matrix.csv')



# CREATE EDGELISTS FOR R VISUALS
df = mod_subs[mod_subs['count']>1]

sub_adj = mod_subs.dot(mod_subs.T)
sub_adj.to_csv('/Users/emg/Programmming/GitHub/R-mod-nets/cmv/data/sub_adj_matrix.csv', index=False)

mod_adj = mod_subs.T.dot(mod_subs)
mod_adj.to_csv('/Users/emg/Programmming/GitHub/R-mod-nets/cmv/data/mod_adj_matrix.csv', index=False)

edges = []
for keys, items in d.iteritems():
    for item in items:
        edges.append([keys, item])
        
mods = zip(*edges)[0]
subs = zip(*edges)[1]

edgelist = pd.DataFrame(data={'mod':mods,'sub':subs})
edgelist.to_csv('/Users/emg/Programmming/GitHub/R-mod-nets/t_d/data/edgelist.csv', index=False)

nodes = mods + subs
modes = [0] *len(mods) + [1]*len(subs)

nodelist = pd.DataFrame(data={'name':nodes, 'mode':modes}, columns=['name','mode'])
nodelist.drop_duplicates('name', inplace=True)
nodelist.to_csv('/Users/emg/Programmming/GitHub/R-mod-nets/t_d/data/nodelist.csv', index=False)




