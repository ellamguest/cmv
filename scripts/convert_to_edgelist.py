#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 12:00:37 2017

@author: emg
"""

import pandas as pd

s
df = pd.read_csv('/Users/emg/Programming/GitHub/the_donald_project/raw_data/all_sub_mods.csv',
                 index_col=0)

def get_lists(df):
    ''' return edgelist, nodelist from df with
        colums (moderator) 'name' and 'sub'
    '''
    edgelist = df[['name','sub']]
    nodelist = pd.DataFrame(list(set(df['name'])) + list(set(df['sub'])))
    modes = [0]*len(list(set(df['name']))) + [1]*len(list(set(df['sub'])))
    nodelist['type'] = modes
    nodelist['name']=nodelist[0].apply(lambda x: x.strip('r/'))
    return edgelist, nodelist

# limit to subs and mods w/ d > 1
sub_count = df.groupby('sub')['sub'].count()
repeats = sub_count[sub_count>1].index
subset = df[df['sub'].isin(repeats)]
mod_count = subset.groupby('name')['name'].count()
repeats = mod_count[mod_count>1].index
subset = subset[subset['name'].isin(repeats)]

edgelist, nodelist = get_lists(subset)

#edgelist.to_csv('/Users/emg/Programming/GitHub/cmv/tidy_data/edgelist_subset.csv', index=False)
#nodelist.to_csv('/Users/emg/Programming/GitHub/cmv/tidy_data/nodelist_subset.csv', index=False)

edgelist.to_csv('/Users/emg/Programming/GitHub/the_donald_project/tidy_data/edgelist_subset.csv', index=False)
nodelist.to_csv('/Users/emg/Programming/GitHub/the_donald_project/tidy_data/nodelist_subset.csv', index=False)

