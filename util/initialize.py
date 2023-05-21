#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from .get_filelist import get_filelist
import os

def initialize(folder_list):
    for folder_name in folder_list:
        try:
            files=get_filelist(dir,folder_name)
            for file in files:
                os.remove(file)
        except: None
        try: os.mkdir(folder_name)
        except: None

