#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
def get_filelist(dir,path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for filename in files:

            if filename!=".DS_Store":
                Filelist.append(os.path.join(home, filename))

    return Filelist

import copy
def sort_list(exclude_list):
    exclude_sorted_list=copy.deepcopy(exclude_list)
    sort_index=[]

    for idx,i in enumerate(exclude_list):
        sort_index.append(i.split("-")[1].split(".")[0])

    for idx,i in enumerate(exclude_sorted_list):
        exclude_sorted_list[int(sort_index[idx])]=exclude_list[idx]
    
    return exclude_sorted_list