#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from cairosvg import svg2pdf
from wand.image import Image as WImage
def svg_to_rasterize(res=200,path='test.svg',temp_seed=0):
    test_path="test%s.pdf"%temp_seed
    svg2pdf(file_obj=open(path, "rb"), write_to=test_path)
    display_im = WImage(filename=test_path,resolution=res)
    return display_im

